import itertools

my_list = [0,1,2]
for tuple_ in itertools.product(my_list, repeat=5):
    # foo(*pair)
    print(tuple_)