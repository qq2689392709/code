
def list_of_groups(init_list, childern_list_len):

    list_of_group = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list

l = [x for x in range(100)]
print(list_of_groups(l,15))
