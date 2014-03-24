__author__ = 'Tony'


def inplace_change(data, old_string, new_string):
        data = str(data)
        if old_string in data:
            data = data.replace(old_string, new_string)
            return data


def getnonstring(data, curr_pos):
    retval = ""

    try:
        start_pos = data.index(" ", curr_pos)
    except:
        start_pos = -1

    if start_pos == -1:
        retval = ""
        return retval

    start_pos += 1

    possible_ends = [',', " ", ")"]
    for each_end in possible_ends:
        try:
            end_pos = data.index(each_end, start_pos)
        except:
            end_pos = -1
        if end_pos > -1:
            break

    retval = data[start_pos:end_pos]

    return retval


def getstring(data, curr_pos):
    retval = ""

    try:
        single_pos = data.index("'", curr_pos)
    except:
        single_pos = -1

    try:
        double_pos = data.index('"', curr_pos)
    except:
        double_pos = -1

    quote_type = ""
    if single_pos == -1 and double_pos == -1:
        return retval
    elif double_pos == -1:
        quote_type = "'"
        start_pos = single_pos
    elif single_pos == -1:
        quote_type = '"'
        start_pos = double_pos
    elif single_pos < double_pos:
        quote_type = "'"
        start_pos = single_pos
    else:
        quote_type = '"'
        start_pos = double_pos

    keepsearching = True

    start_pos += 1

    search_pos = start_pos
    while keepsearching:
        try:
            end_pos = data.index(quote_type, search_pos)
        except:
            end_pos = -1

        if end_pos == -1:
            keepsearching = False

        if data[end_pos] == quote_type and data[end_pos-1] != "\\":
            keepsearching = True
            search_pos = end_pos + 1
        else:
            retval = quote_type + data[start_pos:end_pos] + quote_type
            keepsearching = False

    return retval


def replacephrase(data, findstr, replacement, beg, count=-1):
    if count == -1:
        data = data.replace(findstr, replacement)
    else:
        try:
            str_pos = data.index(findstr, beg)
            data = data[:str_pos] + replacement + data[str_pos + len(findstr):]
        finally:
            return data
    return data


def replace_between(data, opentag, closetag, new_string):
    try:
        start = data.index(opentag) + 1
    except:
        start = -1

    try:
        end = data.index(closetag)
    except:
        end = -1

    if start != -1 and end != -1:
        data = data[:start] + new_string + data[end:]

    return data


def add_string(data, str_to_add, pos):
    data = data[:pos] + str_to_add + data[pos:]
    return data


def string_instance(data, findstr, start=0):
    instance_pos = []
    curr_pos = start
    instance_count = 0
    try:
        while data.index(findstr, curr_pos) > -1:
            instance_count += 1
            curr_pos = data.index(findstr, curr_pos)
            instance_pos.append(curr_pos)
            curr_pos += 1
    finally:
        return instance_pos

    return instance_pos


def string_oneinstance(data, findstr, start=0):
    curr_pos = start
    try:
        found = data.index(findstr, curr_pos)
    except:
        return -1

    return found