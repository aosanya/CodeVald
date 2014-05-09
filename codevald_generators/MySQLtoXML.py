__author__ = 'Tony'

from codevald_generators import stringoperations


class MySQLtoXML:
    def __init__(self, a_script):
        self.script = a_script

    def openfile(self, filename):
        s = open(filename).read()
        return s

    def writefile(self, filename, data):
        f = open(filename, 'w')
        f.write(data)
        f.flush()
        f.close()

    def add_standard_code(self, data):
        data = '<?xml version="1.0" encoding="UTF-8"?>\n' + data
        return data

    def closetables(self, data):
        instances = stringoperations.string_instance(data, "<entity")
        for each_instance in reversed(instances):
            data = stringoperations.replacephrase(data, "(", ">", each_instance, 0)
            table_close = (self.find_closingbracket(data, each_instance))
            data = stringoperations.replacephrase(data, ")", "\n</entity>", table_close, 0)
        return data

    def clear_inter_entity(self, data):
        table_opens = stringoperations.string_instance(data, "<entity")
        table_closes = stringoperations.string_instance(data, "</entity>")
        curr_instance = len(table_closes)

        data = stringoperations.add_string(data, "\n<!--", table_closes[curr_instance-1] + len("</entity>"))
        data = stringoperations.add_string(data, "\n-->", len(data))
        if curr_instance > 1:
            for each_instance in reversed(table_closes):
                curr_instance -= 1
                succesor_entities = [x for x in table_opens if x > table_closes[curr_instance]]
                if len(succesor_entities) > 0:
                    data = stringoperations.add_string(data, "\n<!--\n", table_closes[curr_instance] + len("</entity>"))
                    next_entity = succesor_entities[0] + len("\n<!--\n")
                    data = stringoperations.add_string(data, "\n-->\n", next_entity)
        return data

    def settable_properties(self, data):
        instances = stringoperations.string_instance(data, "<entity")
        instances.sort()
        for each_instance in reversed(instances):
            entity_start = stringoperations.string_oneinstance(data, ">", each_instance)
            entity_close = stringoperations.string_oneinstance(data, "</entity>", each_instance)
            entity_end = stringoperations.string_oneinstance(data, ";", entity_close)
            if entity_start != -1 and entity_close != -1 and entity_end != -1:
                table_properties = data[entity_close+len("</entity>"):entity_end]
                newtable_properties = stringoperations.replacephrase(table_properties, "DEFAULT CHARACTER SET", "DEFAULT_CHARACTER_SET", 0)
                newtable_properties = stringoperations.replacephrase(newtable_properties, " ", "", 0)
                data = stringoperations.replacephrase(data, table_properties + ";", "", entity_close, 0)
                data = stringoperations.replacephrase(data, ">", newtable_properties + " >", entity_start, 0)
        return data

    def settable_schema(self, data):
        instances = stringoperations.string_instance(data, "<entity")
        instances.sort()
        for each_instance in reversed(instances):
            entity_start_end = stringoperations.string_oneinstance(data, ">", each_instance)
            entity_name = data[each_instance+len("<entity"):entity_start_end].strip()
            entity_name_split = entity_name.split(".")
            if len(entity_name_split) == 2:
                data = stringoperations.replacephrase(data, entity_name, "schema='" + entity_name_split[0].replace('`', '') + "' name=" + entity_name_split[1].replace('`', ''), each_instance, 0)
            else:
                data = stringoperations.replacephrase(data, entity_name, "name=" + entity_name.replace('`', '') + "'", each_instance, 0)

        return data

    def setcolumn_properties(self, data):
        instances = stringoperations.string_instance(data, "<entity")
        instances.sort()
        for each_instance in reversed(instances):
            entity_start = stringoperations.string_oneinstance(data, ">", each_instance)
            entity_close = stringoperations.string_oneinstance(data, "</entity>", each_instance)
            if entity_start != -1 and entity_close != -1:
                oldproperties = data[entity_start+1:entity_close]
                properties = data[entity_start+1:entity_close].split(",")
                new_properties = ""
                for each_property in properties:
                    new_properties = new_properties + "\n" + self.getpropertytab() + "<property " + each_property.strip() + "></property>"
                data = stringoperations.replacephrase(data, oldproperties, new_properties + "\n", entity_start, 1)
        return data

    def setproperty_name(self, data):
        instances = stringoperations.string_instance(data, "<property ")
        instances.sort()
        for each_instance in reversed(instances):
            property_name_end = stringoperations.string_oneinstance(data, " ", each_instance + len("<property "))
            if property_name_end != -1:
                property_name = data[each_instance + len("<property "):property_name_end]
                new_property_name = property_name
                new_property_name = new_property_name.replace("`", "")
                data = stringoperations.replacephrase(data, property_name, "name='" + new_property_name.strip() + "' ", each_instance, 1)
        return data

    def setprimarykeys_properties(self, data):
        instances = stringoperations.string_instance(data, "<property PRIMARY KEY")
        instances.sort()
        for each_instance in reversed(instances):
            property_close = stringoperations.string_oneinstance(data, "</property>", each_instance)
            if property_close != -1:
                primarykey = data[each_instance + len("<property PRIMARY KEY"):property_close]
                new_primarykey = data[each_instance + len("<property PRIMARY KEY"):property_close]
                new_primarykey = new_primarykey.replace("(", "")
                new_primarykey = new_primarykey.replace(")", "")
                new_primarykey = new_primarykey.replace(">", "")
                new_primarykey = new_primarykey.replace("`", "")
                data = stringoperations.replacephrase(data, primarykey, "column=\'" + new_primarykey.strip() + "\'", each_instance, 1)
                data = stringoperations.replacephrase(data, "<property PRIMARY KEY", "<primarykey ", each_instance, 1)
                data = stringoperations.replacephrase(data, "</property>", "</primarykey>", each_instance, 1)
        return data

    def setindices(self, data):
        instances = stringoperations.string_instance(data, "<property INDEX")
        instances.sort()
        for each_instance in reversed(instances):
            property_close = stringoperations.string_oneinstance(data, "</property>", each_instance)
            if property_close != -1:
                index_name_end = stringoperations.string_oneinstance(data, "(", each_instance)
                if index_name_end != -1:
                    index_name = data[each_instance + len("<property INDEX"):index_name_end]
                    new_index_name = index_name
                    new_index_name = new_index_name.replace("`", "")

                    data = stringoperations.replacephrase(data, index_name, "name=\'" + new_index_name.strip() + "\' ", each_instance, 1)

                data = stringoperations.replacephrase(data, "<property INDEX", "<index ", each_instance, 1)
                data = stringoperations.replacephrase(data, "</property>", "</index>", each_instance, 1)

        data = self.setindices_column(data)

        return data

    def setindices_column(self, data):
        instances = stringoperations.string_instance(data, "<index")
        instances.sort()
        for each_instance in reversed(instances):
            property_close = stringoperations.string_oneinstance(data, "</index>", each_instance)
            if property_close != -1:
                index_column_start = stringoperations.string_oneinstance(data, "(", each_instance)
                index_name_end = stringoperations.string_oneinstance(data, ")", each_instance)
                if index_column_start != -1 and index_name_end != -1 and index_column_start < property_close and index_name_end < property_close:
                    index_name = data[index_column_start:index_name_end + 1]
                    new_index_name = index_name
                    new_index_name = new_index_name.replace(" ASC)", " order='ASC')")
                    new_index_name = new_index_name.replace(" DESC)", " order='DESC')")
                    new_index_name = new_index_name.replace(")", "")
                    new_index_name = new_index_name.replace("(", "")
                    new_index_name = new_index_name.replace("`", "")

                    data = stringoperations.replacephrase(data, index_name, "column=" + new_index_name.strip(), each_instance, 1)


        return data

    def covert(self, data, search_start, search_end, subsearch_start, subsearch_end, newname, substart_replace = "", subend_replace = ""):
        instances = stringoperations.string_instance(data, search_start)
        instances.sort()
        for each_instance in reversed(instances):
            property_close = stringoperations.string_oneinstance(data, search_end, each_instance)
            if property_close != -1:
                index_column_start = stringoperations.string_oneinstance(data, subsearch_start, each_instance)
                index_name_end = stringoperations.string_oneinstance(data, subsearch_end, each_instance)
                if index_column_start != -1 and index_name_end != -1 and index_column_start < property_close and index_name_end < property_close:
                    index_name = data[index_column_start:index_name_end + 1]
                    new_index_name = index_name
                    new_index_name = new_index_name.replace(subsearch_start, substart_replace)
                    new_index_name = new_index_name.replace(subsearch_end, subend_replace)
                    new_index_name = new_index_name.replace("`", "'")

                    data = stringoperations.replacephrase(data, index_name,  newname + "=" + new_index_name.strip(), each_instance, 1)

        return data

    def setconstraint_properties(self, data):
        instances = stringoperations.string_instance(data, "<property CONSTRAINT")
        instances.sort()
        for each_instance in reversed(instances):
            property_close = stringoperations.string_oneinstance(data, "</property>", each_instance)
            if property_close != -1:
                index_name_end = stringoperations.string_oneinstance(data, "FOREIGN KEY", each_instance)
                if index_name_end != -1:
                    constraint_name = data[each_instance + len("<property CONSTRAINT"):index_name_end]
                    new_constraint_name = constraint_name
                    new_constraint_name = new_constraint_name.replace("`", "'")
                    data = stringoperations.replacephrase(data, constraint_name, "name=" + new_constraint_name.strip() + " ", each_instance, 1)

                data = stringoperations.replacephrase(data, "<property CONSTRAINT", "<constraint ", each_instance, 1)
                data = stringoperations.replacephrase(data, "</property>", "</constraint>", each_instance, 1)

        data = data.replace("ON DELETE RESTRICT", "ondelete='restrict'")
        data = data.replace("ON DELETE CASCADE", "ondelete='cascade'")
        data = data.replace("ON UPDATE CASCADE", "onupdate='cascade'")
        data = data.replace("ON UPDATE CASCADE", "onupdate='cascade'")

        return data

    def getpropertytab(self):
        return "".ljust(1, '\t')

    def comment_info(self, data):
        instances = stringoperations.string_instance(data, "SET @")
        instances.sort()
        for each_instance in reversed(instances):
            data = stringoperations.add_string(data, "<!--", each_instance)
            set_end = data.index(";", each_instance)
            data = stringoperations.add_string(data, "-->", set_end+1)
        return data

    def setdefaults(self, data):
        instances = stringoperations.string_instance(data, " DEFAULT ")
        instances.sort()
        for each_instance in reversed(instances):
            default_start = data.index(" ", each_instance + 1)
            default_val = ""
            if self.IsString(data, default_start):
                default_val = stringoperations.getstring(data, default_start)
            else:
                default_val = stringoperations.getnonstring(data, default_start)
            data = stringoperations.replacephrase(data, "DEFAULT " + default_val, "default=" + default_val, each_instance, 0)
        return data

    def IsString(self, data, curr_pos):
        try:
            string_start = data.index("'", curr_pos)
        except:
            string_start = -1

        if string_start > -1:
            if data[curr_pos:string_start+1].strip() == "'":
                return True

        try:
            string_start = data.index('"', curr_pos)
        except:
            string_start = -1

        if string_start > -1:
            if data[curr_pos:string_start+1].strip() == '"':
                return True

        return False

    def setprecision(self, data):
        datatypes = ["VARCHAR"]
        for each_datatype in datatypes:
            instances = stringoperations.string_instance(data, each_datatype)
            for each_instance in reversed(instances):
                precision = self.getprecision(data, each_datatype, each_instance)
                if precision != "":
                    data = stringoperations.replacephrase(data, ")", "", each_instance, 1)
                    data = stringoperations.replacephrase(data, precision, "", each_instance, 1)
                    data = stringoperations.replacephrase(data, "(", " precision='" + precision + "'", each_instance, 1)

        return data

    def getprecision(self, data, datatype, beg):
        try:
            open_bracket_pos = data.index("(", beg)
        except:
            open_bracket_pos = -1
        if open_bracket_pos > -1:
            has_precision = data[beg:open_bracket_pos+1].replace(" ", "") == datatype.replace(" ", "") + "("
            if has_precision:
                precision_close = (self.find_closingbracket(data, open_bracket_pos+1))
                if precision_close > -1:
                    return data[open_bracket_pos+1:precision_close]
                else:
                    return ""
            else:
                return ""
        else:
            return ""

    def SetDataTypes(self, data):
        datatypes = ["SMALLINT", "INT", "VARCHAR", "TINYINT", "BLOB", "TIMESTAMP"]
        for each_datatype in datatypes:
            data = stringoperations.replacephrase(data, " " + each_datatype, " type='" + each_datatype.lower() + "'", 0)
        return data

    def find_closingbracket(self, data, beg):
        open_count = 0
        curr_pos = beg

        try:
            hasclose = data.index(")", curr_pos) > -1
        except:
            hasclose = False

        while hasclose:
            close_pos = data.index(")", curr_pos)
            try:
                open_pos = data.index("(", curr_pos)
            except:
                open_pos = -1
            '''
            print("open " + open_pos.__str__() + ":" "close " + close_pos.__str__())
            print(data[curr_pos:curr_pos+10])
            print(data[open_pos:open_pos+10])
            print(data[close_pos-10:close_pos+10])

            print("open " + open_pos.__str__() + ":" "close " + close_pos.__str__())
            print("open count " + open_count.__str__())
            '''
            if open_pos > -1:
                if open_pos < close_pos:
                    curr_pos = open_pos + 1
                    open_count += 1
                else:
                    if open_count > 0:
                        open_count -= 1
                        curr_pos = close_pos+1
                    else:
                        return close_pos
            else:
                if open_count > 0:
                    open_count -= 1
                    curr_pos = close_pos+1
                else:
                    return close_pos

            try:
                hasclose = data.index(")", curr_pos) > -1
            except:
                return -1

    def GetXML(self):
        xml = self.script
        xml = stringoperations.inplace_change(xml, "\n\n\n", "\n\n")

        xml = stringoperations.inplace_change(self.script, "\n--", "")
        xml = stringoperations.inplace_change(xml, "  ", " ")
        xml = stringoperations.inplace_change(xml, "CREATE TABLE", "<entity")
        xml = stringoperations.inplace_change(xml, "IF NOT EXISTS", "")
        xml = stringoperations.inplace_change(xml, "NOT NULL", "nullable='false'")
        #set the defaults
        #xml = inplace_change(xml, "DEFAULT NULL", "default=null")
        #xml = inplace_change(xml, "AUTO_INCREMENT", "default=CURRENT_TIMESTAMP")

        xml = stringoperations.inplace_change(xml, " NULL ", " nullable='true' ")
        xml = stringoperations.inplace_change(xml, "UNSIGNED", "unsigned='false'")
        xml = stringoperations.inplace_change(xml, "AUTO_INCREMENT", "auto_increment='true'")

        xml = self.closetables(xml)
        xml = self.settable_properties(xml)
        xml = self.settable_schema(xml)

         # Set the Default Values
        xml = self.setdefaults(xml)

        xml = self.setcolumn_properties(xml)
        # Set the Data Types
        xml = self.setprecision(xml)
        xml = self.SetDataTypes(xml)


        # Set Clean/Give Up
        xml = self.clear_inter_entity(xml)

        xml = self.setprimarykeys_properties(xml)

        xml = self.setconstraint_properties(xml)
        xml = self.setindices(xml)
        xml = self.covert(xml, "<constraint ", "</constraint>", "FOREIGN KEY (", ")", "columns")
        xml = self.covert(xml, "REFERENCES ", "</constraint>", "(", ")", "  cols_referenced")
        xml = self.covert(xml, "REFERENCES ", "</constraint>", "REFERENCES ", " ", "schema_referenced")
        xml = self.covert(xml, "schema_referenced", "</constraint>", "schema_referenced=", " ", "schema_referenced")
        xml = self.covert(xml, "schema_referenced", "</constraint>", ".", " ", " tbl_referenced")

        xml = self.setproperty_name(xml)
        #xml = stringoperations.inplace_change(xml, "\nENGINE=InnoDB\n", " ENGINE=InnoDB ")
        #add_standard_code
        xml = self.add_standard_code(xml)

        xml = self.comment_info(xml)

        return xml