__author__ = 'Tony'
from bs4 import BeautifulSoup

from codevald_generators import stringoperations

strComma = "$$5!#%#@@!!!!1"
strToSubProperty_Start = "$$5!#%#@@!!!!2.1"
strToSubProperty_End = "$$5!#%#@@!!!!2.2"

strReference_Col_Start = "$$5!#%#@@!!!!3.1"
strReference_Col_End = "$$5!#%#@@!!!!3.2"

strReference_Ref_Start = "$$5!#%#@@!!!!4.1"
strReference_Ref_End = "$$5!#%#@@!!!!4.2"

strReferenced_tbl_Start = "$$5!#%#@@!!!!5.1"
strReferenced_tbl_End = "$$5!#%#@@!!!!5.2"

strReferenced_Pri_Start = "$$5!#%#@@!!!!6.1"
strReferenced_Pri_End = "$$5!#%#@@!!!!6.2"


class MySQLtoXML:

    datatypes = ["SMALLINT", "INT", "MEDIUMINT", "INTEGER", "BIGINT", "FLOAT", "DOUBLE",
                 "CHAR", "VARCHAR", "TINYINT", "TIMESTAMP", "DECIMAL", "DEC", "NUMERIC",
                 "SERIAL", "TYPE", "ZEROFILL", "DATETIME", "DATE", "TIMESTAMP", "TIME",
                 "YEAR", "BINARY", "VARBINARY", "BLOB", "TINYBLOB", "MEDIUMBLOB", "LONGBLOB",
                 "SET", "ENUM", "BIT", "TINYTEXT", "TEXT", "MEDIUMTEXT", "LONGTEXT"]

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

        data = self.covert(data, " ENUM(", ")", "ENUM(", ")", "", "enum=\"", "\"")
        data = self.covert(data, " SET(", ")", "SET(", ")", "", "set=\"", "\"")

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

            temp_entity_close = stringoperations.string_oneinstance(data, "PRIMARY KEY", each_instance)
            if temp_entity_close < entity_close and temp_entity_close != -1:
                entity_close = temp_entity_close

            temp_entity_close = stringoperations.string_oneinstance(data, "INDEX ", each_instance)
            if temp_entity_close < entity_close and temp_entity_close != -1:
                entity_close = temp_entity_close

            temp_entity_close = stringoperations.string_oneinstance(data, "CONSTRAINT ", each_instance)
            if temp_entity_close < entity_close and temp_entity_close != -1:
                entity_close = temp_entity_close

            if entity_start != -1 and entity_close != -1:
                oldproperties = data[entity_start+1:entity_close]
                properties = data[entity_start+1:entity_close].split(",")
                new_properties = ""
                for each_property in properties:
                    new_properties = new_properties + "\n" + self.getpropertytab() + "<property " + each_property.strip() + "></property>"
                data = stringoperations.replacephrase(data, oldproperties, new_properties + "\n", entity_start, 1)
        data = data.replace("<property ></property>\n", "")
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
                new_property_name = new_property_name.replace("'", "")
                data = stringoperations.replacephrase(data, property_name, "name='" + new_property_name.strip() + "' ", each_instance, 1)
        return data

    def setprimarykeys_properties(self, data):
        data = self.covert(data, "PRIMARY KEY (", ")", "PRIMARY KEY (", ")", "", "<primarykey " + strToSubProperty_Start, strToSubProperty_End + "></primarykey>")

        #clean up
        data = data.replace('</primarykey>,', '</primarykey>')
        data = self.makesubproperty(data, "primarykey", "column")
        #tempxml = self.covert(data, "<primarykey", "</primarykey>", ",", "</primarykey>", "column", "</primarykey>\n\t<primarykey ", "></primarykey>")
        #while tempxml != data:
        #    data = tempxml
        #    tempxml = self.covert(data, "<primarykey", "</primarykey>", ",", "</primarykey>", "column", "</primarykey>\n\t<primarykey ", "></primarykey>")

        return data

    def setindices(self, data):
        data = self.covert(data, "UNIQUE INDEX ", ")", "UNIQUE INDEX ", ")", "name", "<uniqueindex1 ", ")</uniqueindex1>")
        data = self.covert(data, "<uniqueindex1 ", ")", "(", ")", "", strToSubProperty_Start, strToSubProperty_End + ">")

        data = self.covert(data, "FULLTEXT INDEX ", ")", "FULLTEXT INDEX ", ")", "name", "<fulltextindex2 ", ")</fulltextindex2>")
        data = self.covert(data, "<fulltextindex2 ", ")", "(", ")", "", strToSubProperty_Start, strToSubProperty_End + ">")

        data = self.covert(data, "INDEX ", ")", "INDEX ", ")", "name", "<index3 ", ")</index3>")
        data = self.covert(data, "<index3 ", ")", "(", ")", "", strToSubProperty_Start, strToSubProperty_End + ">")
        #clean up
        data = data.replace('</uniqueindex1>,', '</uniqueindex1>')
        data = data.replace('</fulltextindex2>,', '</fulltextindex2>')
        data = data.replace('</index3>,', '</index3>')

        data = self.makesubproperty(data, "uniqueindex1", "column")
        data = self.makesubproperty(data, "fulltextindex2", "column")
        data = self.makesubproperty(data, "index3", "column")
        return data

    def formatindices(self, data):
        data = self.covert(data, "<index", ")", "(", ")", "column", "", ")")
        data = self.covert(data, "<index3", ")", " ASC", ")", " order", "", "", "'ASC'")
        data = self.covert(data, "<index3", ")", " DESC", ")", " order", "", "", "'DESC'")

        data = self.covert(data, "<uniqueindex1", ")", " ASC", ")", " order", "", "", "'ASC'")
        data = self.covert(data, "<uniqueindex1", ")", " DESC", ")", " order", "", "", "'DESC'")
        #data = self.setindices_column(data)

        return data

    def setindices_column2(self, data):
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

    def makesubproperty(self, data, tagname, propertyname):
        instances = stringoperations.string_instance(data, "<" + tagname)
        instances.sort()
        for each_instance in reversed(instances):
            entity_start = stringoperations.string_oneinstance(data, strToSubProperty_Start, each_instance)
            entity_end = stringoperations.string_oneinstance(data, strToSubProperty_End, each_instance)
            property_close = stringoperations.string_oneinstance(data, "</" + tagname + ">", each_instance)
            if entity_start != -1 and entity_start < property_close and entity_end != -1 and entity_end < property_close:
                property = data[entity_start:entity_end + len(strToSubProperty_End)]
                newproperty = property.replace(strToSubProperty_Start, "")
                newproperty = newproperty.replace(strToSubProperty_End, "")
                tempproperty = []
                tempproperty = newproperty.split(",")
                newproperty = ""
                for each_property in tempproperty:
                    newproperty = newproperty + "\n\t\t<" + propertyname + " name=" + each_property.strip(" ") + "></" + propertyname + ">"

                newproperty = newproperty + "\n\t"
                data = stringoperations.replacephrase(data, property, "", entity_start, 1)
                data = stringoperations.replacephrase(data, "></" + tagname + ">", ">" + newproperty + "</" + tagname + ">", entity_start, 1)
        return data

    def secure_object_brackets(self, data, object_tag, content_start, content_end):
        instances = stringoperations.string_instance(data, "<" + object_tag)
        instances.sort()
        for each_instance in reversed(instances):
            entity_start = stringoperations.string_oneinstance(data, ">", each_instance)
            entity_close = stringoperations.string_oneinstance(data, "</" + object_tag, entity_start)
            entity_end = stringoperations.string_oneinstance(data, ";", entity_close)
            if entity_start != -1 and entity_close != -1 and entity_end != -1:
                table_properties = data[entity_start + 1:entity_close]
                newtable_properties = self.secure_brackets(table_properties, content_start, content_end)
                data = stringoperations.replacephrase(data, table_properties, newtable_properties, entity_start)
        return data

    def secure_brackets(self, data, content_start, content_end):
        instances = stringoperations.string_instance(data, content_start)
        instances.sort()
        for each_instance in reversed(instances):
            index_bracket_close = stringoperations.string_oneinstance(data, content_end, each_instance)
            if index_bracket_close != -1:
                bracket_content = data[each_instance:index_bracket_close + 1]
                new_bracket_content = bracket_content
                new_bracket_content = new_bracket_content.replace(",", strComma)
                data = stringoperations.replacephrase(data, bracket_content, new_bracket_content, each_instance, 1)
        return data

    def covert(self, data, search_start, search_end, subsearch_start, subsearch_end, newname, substart_replace = "", subend_replace = "", value = ""):
        instances = stringoperations.string_instance(data, search_start)
        instances.sort()
        for each_instance in reversed(instances):
            property_close = stringoperations.string_oneinstance(data, search_end, each_instance)
            if property_close != -1:
                index_column_start = stringoperations.string_oneinstance(data, subsearch_start, each_instance)
                index_name_end = stringoperations.string_oneinstance(data, subsearch_end, each_instance)
                if index_column_start != -1 and index_name_end != -1 and index_column_start <= property_close and index_name_end <= property_close:
                    index_name = data[index_column_start:index_name_end + 1]
                    new_index_name = index_name
                    if newname != "":
                        new_index_name = new_index_name.replace(subsearch_start, substart_replace + newname + "=" + value)
                    else:
                        new_index_name = new_index_name.replace(subsearch_start, substart_replace)

                    new_index_name = new_index_name.replace(subsearch_end, subend_replace)
                    new_index_name = new_index_name.replace("`", "'")

                    data = stringoperations.replacephrase(data, index_name, new_index_name, each_instance, 1)
        return data

    def setreferences(self, data):
        instances = stringoperations.string_instance(data, "<constraint")
        instances.sort()
        for each_instance in reversed(instances):
            column_start = stringoperations.string_oneinstance(data, strReference_Col_Start, each_instance)
            column_end = stringoperations.string_oneinstance(data, strReference_Col_End, each_instance)

            reference_start = stringoperations.string_oneinstance(data, strReference_Ref_Start, each_instance)
            refence_end = stringoperations.string_oneinstance(data, strReference_Ref_End, each_instance)

            if column_start != -1 and column_end != -1 and reference_start != -1 and refence_end != -1:
                columns = data[column_start:column_end + len(strReference_Col_End)]
                references = data[reference_start:refence_end + len(strReference_Ref_End)]

                newcolumns = columns.replace(strReference_Col_Start, "")
                newcolumns = newcolumns.replace(strReference_Col_End, "")

                newreferences = references.replace(strReference_Ref_Start, "")
                newreferences = newreferences.replace(strReference_Ref_End, "")

                splitcolumns = newcolumns.split(",")
                splitreferences = newreferences.split(",")

                reference = ""
                if len(splitcolumns) == len(splitreferences):
                    for i in range(len(splitcolumns)):
                        reference = reference + "\n\t\t<reference column=" + splitcolumns[i] + " referenced=" + splitreferences[i] + "></reference>"

                reference = reference + "\n\t"
                data = stringoperations.replacephrase(data, columns, "", column_start, 1)
                data = stringoperations.replacephrase(data, references, "", column_start, 1)

                data = stringoperations.replacephrase(data, "></constraint>", ">" + reference + "</constraint>", column_start, 1)
        return data

    def setconstraint_properties(self, data):
        data = self.covert(data, "FOREIGN KEY ", "<", "(", ")", "", strReference_Col_Start, strReference_Col_End)

        data = self.covert(data, "CONSTRAINT ", "<", "CONSTRAINT ", ")", "name", "\n<constraint ", ")")

        data = self.covert(data, "REFERENCES ", "<", "(", ")", "", strReferenced_tbl_End + strReference_Ref_Start, strReference_Ref_End)

        data = self.covert(data, "REFERENCES ", "<", "REFERENCES ", strReference_Ref_End, " schema_referenced", "", strReference_Ref_End)

        data = self.covert(data, "schema_referenced", "<", ".", strReferenced_tbl_End, " tbl_referenced", "")

        data = self.covert(data, "constraint", "<", "<", "<", "", "></constraint><", "<")

        data = data.replace("ON DELETE RESTRICT", "ondelete='restrict'")

        data = data.replace("ON DELETE CASCADE", "ondelete='cascade'")

        data = data.replace("ON UPDATE CASCADE", "onupdate='cascade'")

        data = data.replace("ON UPDATE CASCADE", "onupdate='cascade'")

        data = data.replace("FOREIGN KEY", "")

        data = data.replace("REFERENCES", "")

        data = self.setreferences(data)
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

    def cleanup(self, data):
        data = data.replace('</uniqueindex1>', '</uniqueindex>')
        data = data.replace('</fulltextindex2>', '</fulltextindex>')
        data = data.replace('</index3>', '</index>')
        data = data.replace('<uniqueindex1 ', '<uniqueindex ')
        data = data.replace('<fulltextindex2 ', '<fulltextindex ')
        data = data.replace('<index3 ', '<index ')
        data = data.replace(strComma, ",")
        data = data.replace("\n>", ">")
        data = data.replace(strReferenced_tbl_End, "")

        soup = BeautifulSoup(data)
        soup.prettify()
        data = soup.__str__()

        data = data.replace("<property", "\t<property")
        data = data.replace("<primarykey", "\t<primarykey")
        data = data.replace("</primarykey", "\t</primarykey")
        data = data.replace("<index", "\t<index")
        data = data.replace("</index", "\t</index")
        data = data.replace("<column", "\t\t<column")
        data = data.replace("<constraint", "\t<constraint")
        data = data.replace("</constraint", "\t</constraint")
        data = data.replace("<reference", "\t\t<reference")
        data = data.replace("></entity>", ">\n</entity>")
        data = data.replace("<uniqueindex", "\t<uniqueindex")
        data = data.replace("</uniqueindex", "\t</uniqueindex")
        data = data.replace(",=\"\"", "")
        data = data.replace(",=\"\" ", "")
        data = data.replace("'=\"\" ", "")


        newdata = data.replace("\n\n", "\n")
        while data != newdata:
            data = newdata
            newdata = data.replace("\n\n", "\n")

        return data

    def SetDataTypes(self, data):

        for each_datatype in self.datatypes:
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

        for each_datatype in self.datatypes:
            xml = self.secure_object_brackets(xml, "entity", each_datatype + "(", ")")

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

        xml = self.formatindices(xml)

        xml = self.setproperty_name(xml)
        #xml = stringoperations.inplace_change(xml, "\nENGINE=InnoDB\n", " ENGINE=InnoDB ")
        #add_standard_code
        xml = self.add_standard_code(xml)

        xml = self.comment_info(xml)

        xml = self.cleanup(xml)
        return xml

