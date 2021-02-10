import timeit

testcode = '''
def list_remove():
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    list.remove(8)
'''

testcode2 = '''
def list_comprehension():
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    remove=[8]
    new_list = [x for x in List if x not in remove]
'''

print(timeit.timeit(stmt=testcode, number=2000000))
print(timeit.timeit(stmt=testcode2, number=2000000))
#print(timeit.timeit('[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].remove(8)'))
