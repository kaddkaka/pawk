Process textfiles in an awk-like manner, but with python syntax.

Supported variables:
* `BEGIN` (True on first record in file)
* `END` (True on last entry in file)
* `NR` (current record number)
* `F` (the fields of current record)

# Fruit examples
These examples operate on `examples/fruit_prices.txt` with this content:
```
Banana 150
Apple 10
Citrus 200
Blueberries 30
Strawberries 30
```

* Add a running line number to each line:
```console
$ pawk -t 'print(NR, F[0])' examples/fruit_prices.txt
1 Banana 150
2 Apple 10
3 Citrus 200
4 Blueberries 30
5 Strawberries 30
```

* Calculate the sum of a specific column:
With a program file like this:
```console
$ cat examples/*.py
if BEGIN: s=0
s+=F[2]
if END: print(f"Total: {s}")
```

Supply the above script to pawk:
```console
$ pawk -f examples/total_sum.py examples/fruit_prices.txt
Total: 420
```
