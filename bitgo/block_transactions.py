'''
first get transaction_count
get all the transactions
run algorithm
'''


import requests
from constants import BLOCKSTREAM_BLOCK_INFO_URL



class BlockTransactions:
    def __init__(self, block_id):
        self.block_id = block_id

    def get_block_details(self):
        block_details = requests.get(BLOCKSTREAM_BLOCK_INFO_URL + self.block_id)
        block_status_code = block_details.status_code
        if block_status_code!=200:
            raise Exception("Api call failed")
        print(block_details.content)


block = BlockTransactions("000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732")
block.get_block_details()
