if BEGIN:
    costs = {}
    total = {}
if FNR == NR:
    costs[F[1]] = F[2]
    NEXT

if F[1] not in total: total[F[1]] = 0
total[F[1]] += costs[F[2]] * F[3]

if END: print(f"Total: {total}")
