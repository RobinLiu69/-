
n = int(input())
num = []
k = [0, 0, 0]
for i in range(n):
    num.append(int(input()))
for i in num:
    if i % 3 == 0:
        k[0] += 1
    if i % 3 == 1:
        k[1] += 1
    if i % 3 == 2:
        k[2] += 1
print(" ".join(map(str, k)))
