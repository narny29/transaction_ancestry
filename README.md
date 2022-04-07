This repository gets N transactions with the maximum ancestory count in a given block.

Few points to note:
Only those ancestors are counted which are present in the given block.
The transactions are queried once and then stored in locale so that subsequent requests dont take too much time.
There can be more than one transaction with the same ancestor count. So the number of transactions shown can be more than the given count.


Steps to run:
Edit the file transactions_ancestry.py. You can refer to the given example in the repository or can add a block <br>
    `block = BlockTransactions(block_height="680005")` <br>
    `print(block.get_top_ancestry_count_transactions(15))`
    
    or
    
    `block = BlockTransactions(block_id="000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732")
    print(block.get_top_ancestry_count_transactions(20))`

run the file using the command `python3 transactions_ancestry.py`
