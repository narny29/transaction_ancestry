import requests
import json
from os.path import exists
from common.http_req import HttpReq
from constants import BLOCKSTREAM_BLOCK_INFO_URL, BLOCKSTREAM_TRANSACTIONS_FOR_BLOCK_URL, \
                        BLOCKSTREAM_BLOCK_HEIGHT_TO_BLOCK_HASH_URL, BLOCK_TRANSACTIONS_FILE_NAME



class BlockTransactions:
    http_req = HttpReq()

    def __init__(self, block_height=None, block_id=None):
        self.block_height = block_height
        self.block_id = block_id
        self.transaction_count = None
        self.transactions = None
        self.transaction_ids = set()
        self.get_block_details()


    def get_block_details(self):
        if not (self.block_id or self.block_height):
            raise Exception("BlockTransactions class not initiated with proper values")

        if not self.block_id:
            self.block_id = self.http_req.get(url=BLOCKSTREAM_BLOCK_HEIGHT_TO_BLOCK_HASH_URL.format(block_height=self.block_height))

        self.block_details = self.http_req.get(url=BLOCKSTREAM_BLOCK_INFO_URL.format(block_id=self.block_id),
                                                is_json_body=True)

    def get_transactions_count(self):
        if self.transaction_count: return self.transaction_count

        if not self.block_details:
            print("block_details is empty for the given id")

        self.transaction_count = self.block_details.get("tx_count", None)
        return self.transaction_count

    def is_transactions_exist(self):
        return exists(BLOCK_TRANSACTIONS_FILE_NAME.format(block_id=self.block_id))

    def write_transactions_to_local(self, transactions):
        with open(BLOCK_TRANSACTIONS_FILE_NAME.format(block_id=self.block_id), 'w') as f:
            json.dump(transactions, f)

    def get_transaction_ids(self):
        if self.transaction_ids: return self.transaction_ids

        transactions = self.get_transactions()
        for transaction in transactions.values():
            self.transaction_ids.add(transaction.get("txid", None))

        return self.transaction_ids

    def get_transactions(self):
        if self.transactions: return self.transactions

        if self.is_transactions_exist():
            with open(BLOCK_TRANSACTIONS_FILE_NAME.format(block_id=self.block_id), 'r') as f:
                transactions = json.load(f)
            self.transactions = transactions
            return transactions

        combined_transactions = {}
        ind = 0
        transaction_count = self.get_transactions_count()
        while ind<transaction_count:
            transactions = self.http_req.get(url=BLOCKSTREAM_TRANSACTIONS_FOR_BLOCK_URL.format(block_id=self.block_id,
                                                transaction_init_count=ind), is_json_body=True)
            for i in range(len(transactions)):
                temp = ind+i
                tx_id = transactions[i].get("txid")
                if temp:
                    combined_transactions[tx_id] = transactions[i]
            ind+=i+1

        self.transactions = combined_transactions
        self.write_transactions_to_local(combined_transactions)

        return combined_transactions

    def get_transactions_ancestry_count(self):
        ad_matrix = {tx_id: set() for tx_id in self.get_transaction_ids()}
        if not self.transactions:
            self.get_transactions()
        for transaction in self.transactions.values():
            tx_id = transaction.get("txid", None)
            for in_transaction in transaction.get("vin", []):
                in_tx_id = in_transaction.get("txid", None)
                ad_matrix[tx_id].add(in_tx_id)


        transactions_ancestry_count = {}
        for tx_id in self.get_transaction_ids():
            visited = {tx_id: False for tx_id in self.get_transaction_ids()}
            ancestors = 0
            curr = ad_matrix.get(tx_id, [])
            while len(curr):
                nxt = []
                for curr_tx_id in curr:
                    if not visited.get(curr_tx_id, True):
                        visited[curr_tx_id] = True
                        ancestors += 1
                        nxt += list(ad_matrix.get(curr_tx_id, set()))
                curr = nxt
            transactions_ancestry_count[tx_id] = ancestors

        return transactions_ancestry_count

    def get_top_ancestry_count_transactions(self, n):
        transactions_ancestry_count = self.get_transactions_ancestry_count()

        transactions_ancestry_count_to_txid = {val: set() for val in set(transactions_ancestry_count.values())}

        for tx_id in transactions_ancestry_count:
            ancestors = transactions_ancestry_count.get(tx_id)
            transactions_ancestry_count_to_txid[ancestors].add(tx_id)

        tx_count = 0
        values_list = sorted(set(transactions_ancestry_count.values()), reverse=True)
        values_ind = 0
        top_ancestry_count_transactions = []
        while tx_count<n:
            current_ancestor_count = values_list[values_ind]
            for tx_id in transactions_ancestry_count_to_txid.get(current_ancestor_count, []):
                top_ancestry_count_transactions.append([tx_id, current_ancestor_count])
            tx_count += len(transactions_ancestry_count_to_txid.get(current_ancestor_count, []))
            values_ind += 1

        return top_ancestry_count_transactions



block = BlockTransactions(block_height="680001")
print(block.get_top_ancestry_count_transactions(19))
