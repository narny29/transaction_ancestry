from block_transactions import BlockTransactions


block = BlockTransactions(block_height="680001")
print(block.get_top_ancestry_count_transactions(10))



block = BlockTransactions(block_height="680000")
print(block.get_top_ancestry_count_transactions(10))
