
# def swap(my_list2):
#     temp = my_list2[0]
#     my_list2[0] = my_list2[1]
#     my_list2[1] = temp
#     return my_list2
#
#
# my_list = [[1, 1, 1], [2, 2, 2]]
#
# swap(my_list)
# print(my_list)
#
priorities = [5, 4, 3, 2, 1]


def swap(idx_1, idx_2, priorities):
    priorities[idx_1], priorities[idx_2] = priorities[idx_2], priorities[idx_1]


for j in range(0, len(priorities) - 1):
    for i in range(0, len(priorities) - 1):
        if priorities[i] > priorities[i + 1]:
            swap(i, i + 1, priorities)

print(priorities)

for i in range(0, len(priorities)):
    print(i)
