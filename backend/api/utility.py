def get_from_dict_by_path(dict, keys):
    try:
        for key in keys:
            dict = dict[key]
        return dict
    except KeyError:
        return {}


def set_in_dict_by_path(dict, keys, value):
    for key in keys[:-1]:
        dict = dict.setdefault(key, {})
    dict[keys[-1]] = value


def remove_from_dict_by_path(dict, keys):
    del get_from_dict_by_path(dict, keys[:-1])[keys[-1]]


def remove_empty_pair_from_dict_by_path(dict, keys):
    if len(keys) == 1:
        del dict[keys[0]]
        return
    if get_from_dict_by_path(dict, keys) == {}:
        del get_from_dict_by_path(dict, keys[:-1])[keys[-1]]
        remove_empty_pair_from_dict_by_path(dict, keys[:-1])
