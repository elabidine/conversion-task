


def mod_data(data, **kwargs):
    """ Returns a copy of the object/data provided, with some values updated based on the key/value pairs provided in the kwargs.
    - Values for keys already present in the object/data are updated,
    - New keys are added,
    - Existing keys not provided in the kwargs are left unchanged.
    - If not kwargs are provided, a copy of original object/data is returned.
    """
    # print(kwargs)
    new_data = data.copy()
    for key, val in kwargs.items():
        new_data[key] = val
    return new_data
