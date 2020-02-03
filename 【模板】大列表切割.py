
def list_of_groups(init_list, childern_list_len):
    from math import floor
    if isinstance(childern_list_len,float):
        l = len(init_list)
        childern_list_len = floor(l * childern_list_len) if floor(l * childern_list_len) != 0 else 1
        list_of_group = zip(*(iter(init_list),) * childern_list_len)

    elif isinstance(childern_list_len,int):
        list_of_group = zip(*(iter(init_list),) * childern_list_len)

    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list

l = [x for x in range(100)]
print(list_of_groups(l,0.1))
