# group0 = []
#
# num = input("Enter how many elements you want:")
# print('Enter numbers in array: ')
# for i in range(int(num)):
#     n = input("num :")
#     group0.append(float(n))
#
# print(*group0)
group0 = [10.75, 26.5, 28.75, 18.25, 18.5, 21.25, 31.25, 20.5, 23.5, 23.75]

group0.sort()

group1 = list()

while sum(group1) < sum(group0):
    num = group0[0]
    group0.remove(num)
    group1.append(num)


for i in range(100):
    target = (sum(group0) - sum(group1)) / 2
    if all(x > target for x in group0) and all(x < target for x in group1):
        break

    # print(target)
    options = [x for x in group0 if x <= target]
    if options.__len__() > 0:
        group0.remove(options[-1])
        group1.append(options[-1])
        continue

    options = [x for x in group1 if x >= target]
    if options.__len__() > 0:
        group1.remove(options[0])
        group0.append(options[0])
        continue

    break

print(*group0)
print(*group1)
print(abs(sum(group0) - sum(group1)))
