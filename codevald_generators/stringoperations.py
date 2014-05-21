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
    data = data.lower()
    findstr = findstr.lower()
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
    data = data.lower()
    try:
        findstr = findstr.lower()
    except:
        findstr = findstr

    curr_pos = start
    try:
        found = data.index(findstr, curr_pos)
    except:
        return -1

    return found

def highlight(data, findstr, color, start=0):
    data = data.replace(findstr, "<span color=" + color + ">" + findstr + "</span>")
    #data = data.replace(findstr, "<b>" + findstr + "</b>")

    return data

def startswith(strVal, lstCompare):
    for each_Compare in lstCompare:
        tocompare = strVal.strip()
        tocompare = tocompare.strip("\t")
        tocompare = tocompare.strip("\n")
        if strVal.strip()[:len(each_Compare)] == each_Compare:
            return True

    return False

def IsList(self, data, position, separator = ",", opening = "(", closing = ")"):
    return GetList(self, data, position, separator, opening, closing).__len__() == 2

def GetList(self, data, position, separator = ",", opening = "(", closing = ")"):
    To_Close = True
    To_Open = True
    Closed = False
    Opened = False

    prev_obj = ""
    for each_obj in data:
        if prev_obj == each_obj:
            print(each_obj)
        prev_obj = each_obj

    Close_Pos = position
    Open_Pos = position
    TheList = []
    OpenQuotes = 0
    OpenSingleQuotes = 0
    NewItem = False

    while Open_Pos >= 0 and not Opened:
        currdata = data[Open_Pos]
        try:
            digitdata = int(currdata)
        except:
            digitdata = ""

        if currdata == "'":
            try:
                prevpos_2 = data[Open_Pos -1]
            except:
                prevpos_2 = ""

            try:
                prevpos_2 = data[Open_Pos -2]
            except:
                prevpos_2 = ""

            #IsSingleQuote = (prevpos_2 != "\\")

            #if IsSingleQuote:
            if To_Open:
                OpenSingleQuotes = OpenSingleQuotes + 1
            elif not To_Open:
                OpenSingleQuotes = OpenSingleQuotes - 1

        if digitdata != "" and not To_Open:
            To_Open = True
        elif data[Open_Pos] == opening and To_Open:
            Opened = True
            TheList.append(Open_Pos)
        elif data[Open_Pos] == separator:
            To_Open = False

        Open_Pos = Open_Pos - 1

    if OpenSingleQuotes > 0:
        To_Close = False


    Close_Pos = Close_Pos + 1

    while Close_Pos <= data.__len__()-1 and not Closed:
        currdata = data[Close_Pos]
        try:
            digitdata = int(currdata)
        except:
            digitdata = ""

        IsSingleQuote = False
        if currdata == "'":
            try:
                prevpos_1 = data[Close_Pos - 1]
            except:
                prevpos_1 = ""

            try:
                prevpos_2 = data[Close_Pos - 2]
            except:
                prevpos_2 = ""

            IsSingleQuote = (prevpos_2 != '\'')
            if IsSingleQuote:
                if To_Close:
                    OpenSingleQuotes = OpenSingleQuotes + 1
                elif not To_Close and OpenSingleQuotes > 0:
                    OpenSingleQuotes = OpenSingleQuotes - 1
                    if OpenSingleQuotes == 0:
                        To_Close = True
                else:
                    OpenSingleQuotes = OpenSingleQuotes + 1

        if digitdata != "" and not To_Close and OpenSingleQuotes == 0:
            To_Close = True
        elif data[Close_Pos] == closing and To_Close:
            Closed = True
            TheList.append(Close_Pos)
        elif data[Close_Pos] == separator and To_Close:
            To_Close = False
        elif currdata == " " or IsSingleQuote or currdata == '"':
            To_Close = To_Close
        else:
            To_Close = False

        if currdata == separator and OpenSingleQuotes > 0:
            Closed = True

        Close_Pos = Close_Pos + 1

    if OpenSingleQuotes != 0:
        TheList = []

    return TheList