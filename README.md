Process textfiles in an awk-like manner, but with python syntax.

Supported variables:
* `BEGIN` (True on first record in first file)
* `END` (True on last record in last file)
* `FNR` (current record number in current file, restarts at 1 for each file)
* `NR` (current record number, total running number)
* `F` (the fields of current record)

Keywords:
* `NEXT` is used to skip to next line (matches `next` in awk)

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

## Multiple files example
Using a second input file:
```
David Banana 1
David Strawberries 5
Monica Citrus 3
```

And combine it using this script:
```py
if BEGIN:
    costs = {}
    total = {}
if FNR == NR:
    costs[F[1]] = F[2]
    NEXT

if F[1] not in total: total[F[1]] = 0
total[F[1]] += costs[F[2]] * F[3]

if END: print(f"Total: {total}")
```

To calculate the total cost per person:
```console
$ pawk -f examples/total_order_cost.py examples/fruit_prices.txt examples/fruit_orders.txt
Total: {'David': 300, 'Monica': 600}
```
