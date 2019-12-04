count = 0

for i in range(146810, 612564):
    s = str(i)

    decrease = False
    no_pairs = True

    for j in range(len(s)-1):
        if s[j] > s[j+1]:
            decrease = True
            break
        if s[j] == s[j+1] and s[j] * 3 not in s:
            no_pairs = False

    if decrease:
        continue

    if no_pairs:
        continue

    count+=1

    print(s, count)
