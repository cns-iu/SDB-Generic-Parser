#!/usr/bin/env python
# import os
# import sys
# import re
# import resource
# import time
from lxml import etree
from optparse import OptionParser

# TODO: The parser fails if there are comments or namespaces in the root. How do I fix this?
# TODO: Finish this. For some reason, the arguments are not being taken
parser = OptionParser()
parser.add_option(
        '-d', '--data_file',
        action='store', type='string', dest='data_file',
        help='file name and path of the XML file to be processed. Default: \'test1.xml\'')
parser.add_option(
        '-i', '--unique_identifier',
        action='store', type='string', dest='unique_identifier',
        help='I dont know how to word this. Default: \'UID\'')
parser.add_option(
        '-o', '--output_file',
        action='store', type='string', dest='output_file',
        help='the name and relative path of the file to write to. Default: \'queries.txt\'')
parser.add_option(
        '-p', '--parent_tag',
        action='store', type='string', dest='parent_tag',
        help='the top-most element of the XML. Default: \'records\'')
parser.add_option(
        '-r', '--record_tag',
        action='store', type='string', dest='record_tag',
        help='the identifier to distinguish records. Default: \'REC\'')
parser.add_option(
        '-s', '--schema_file',
        action='store', type='string', dest='schema_file',
        help='file name and path of the XML schema file. Default: \'schema.xml\'')

(options, args)     = parser.parse_args()
data_file           = options.data_file         or 'sample1.xml'
schema_file         = options.schema_file       or 'schema.xml'
parent_tag          = options.parent_tag        or 'records'
output_file_name    = options.output_file       or 'queries.txt'
record_tag          = options.record_tag        or 'REC'
id_tag              = options.unique_identifier or 'UID'
delimiter           = ':'
table_tag           = 'table'
id_list             = []
reserved_keys       = [table_tag]
table_list          = dict()
temp_tables         = dict()

class Table():
    def __init__(self, table_name, fields, values):
        self.table_name = table_name
        self.fields     = fields
        self.values     = values
        self.storage    = []
    def add(self, obj):
        for key, val in obj.iteritems():
            self.fields.append(key)
            self.values.append(val)
        return self
    def clear(self):
        self.fields = []
        self.values = []
        return self
    def store(self):
        self.storage.append(Table(self.table_name, self.fields, self.values))
        return self.clear()
    def stringify(self, coll):
        str = ''
        for item in coll:
            temp_item = item.strip()
            if (temp_item == ""):
                pass
            else:
                str += '"' + item.strip() + '",'
        return str
    def sqlify(self, *args):
        fieldstr = self.stringify(self.fields)
        valuestr = self.stringify(self.values)
        fieldstr = fieldstr[:-1]
        valuestr = valuestr[:-1]
        try:
            assert len(self.fields) == len(self.values)
        except:
            print self.fields
            print self.values
            raise Exception('Length mismatch. Field(' + str(len(self.fields)) + ') !== value(' + str(len(self.values)) + ')')
        if len(args) > 0:
            return 'DELETE FROM "' + self.table_name + '" WHERE (' + id_tag + ' = ' + args[0] + ');\n'
        else:
            return 'INSERT INTO "' + self.table_name + '" (' + fieldstr + ') VALUES (' + valuestr + ');\n'
def find_table(tblstr):
    if tblstr in table_list:
        pass
    else:
        table_list[tblstr] = Table(tblstr, [], [])
    try:
        assert table_list[tblstr] is not None
    except:
        raise Exception(tblstr + ' is not in table_list. WHATD YOU DO?!')
    return table_list[tblstr]

# def parse(fp, source, schema):
def parse(source, schema):
    with open(output_file_name, 'w') as output_file:
        context = etree.iterparse(source, events=('start', 'end'))
        path = []
        curr_table = None
        schema_match = None
        primary_key = None
        for event, elem in context:
# *********************************************************
#   XML event catchers.
# *********************************************************
            # *********************************************************
            #   Start event.
            #   When a new tag opens, try to match the schema to the
            #   data.
            # *********************************************************
            if event == 'start':
                if elem.tag == id_tag:
                    primary_key = elem.text
                path.append(elem)
                try:
                    schema_match = schema.find('/'.join([str(x.tag) for x in path[1:]])[len(record_tag):])
                    # schema_match = schema.find('/'.join([str(x.tag) for x in path[1:]])[len(record_tag):])
                    # table_something = schema_match.get(table_tag)
                    # if table_something is not None:
                    #     curr_table = find_table(table_something)
                except SyntaxError:
                    pass
            # *********************************************************
            #   End event.
            #   When an open tag closes, build strings from each table
            #   built through the parsing.
            # *********************************************************
            else:
                assert event == 'end'
                path.pop()
                if elem.tag == record_tag:
                    assert primary_key is not None
                    delete = False
                    if primary_key in id_list:
                        delete = True
                    to_write = []
                    to_reverse_then_write = []
                    for table in table_list:
                        id_list.append(primary_key)
                        curr_table = find_table(table)
                        for stored in curr_table.storage:
                            if len(stored.fields) > 0:
                                to_write.append(stored.add({id_tag: primary_key}).sqlify())
                        if delete:
                            if len(stored.fields) > 0:
                                to_reverse_then_write.append(curr_table.sqlify(primary_key))
                        if len(curr_table.fields) > 0:
                            to_write.append(curr_table.add({id_tag: primary_key}).sqlify())
                    for x in reversed(to_reverse_then_write):
                        output_file.write(x.encode('utf-8'))
                    for x in to_write:
                        output_file.write(x.encode('utf-8'))
                    table_list.clear()
# *********************************************************
#   XML parser.
# *********************************************************
            if schema_match is not None:
                attrib_table = None
                attrib_field = None
                # *********************************************************
                #   Tag attribute items. Ex: <tag attribute="attribute value">
                #       Match the schema tag to the data tag. Use the
                #       value from the schema to map the value from
                #       the data. The schema attribute item values
                #       usually include the table as well. That is
                #       handled by splitting a string if the delimiter
                #       exists.
                # *********************************************************
                if elem.attrib.items() and schema_match.attrib.items():
                    for key, value in elem.attrib.items():
                        schema_attrib = schema_match.get(key)
                        try:
                            if delimiter in schema_attrib:
                                attrib_split = schema_attrib.split(delimiter)
                                assert len(attrib_split) == 2
                                if schema_match.attrib.get('table') is not None:
                                    find_table(attrib_split[0]).store()
                                find_table(attrib_split[0]).add({attrib_split[1]: value})
                        except TypeError, e:
                            #TODO: What to do here?
                            pass
                        except AssertionError, e:
                            #TODO: What to do here?
                            pass
                        #SUB1
                # *********************************************************
                #   Tag element text. Ex: <tag>tag element text
                #       Match the schema text to the data text. Use the
                #       text from the schema to map the text from
                #       the data. The schema text is usually include the
                #       table as well. That is handled by splitting a
                #       string if the delimiter exists.
                # *********************************************************
                if elem.text and schema_match.text:
                    if delimiter in schema_match.text:
                        attrib_split = schema_match.text.split(delimiter)
                        attrib_table = find_table(attrib_split[0])
                        attrib_field = attrib_split[1]
                    elif curr_table is not None:
                        attrib_table = curr_table
                        attrib_field = schema_match.text
                    else:
                        #TODO: What to do here?
                        pass
                attrib_value = elem.text
                try:
                    if len(attrib_field.strip()) > 0:
                        attrib_table.fields.append(attrib_field)
                        attrib_table.values.append(attrib_value)
                except AttributeError:
                    pass
            # except SyntaxError as syntax:
            #   # raise Exception('Data does not fit with schema')
            #   pass
            elem.clear()
            # delete previous siblings
            while elem.getprevious() is not None:
                del elem.getparent()[0]

# Based on http://stackoverflow.com/questions/9809469/python-sax-to-lxml-for-80gb-xml
class InfiniteXML (object):
    def __init__(self):
        self._root = True
    def read(self, len=None):
        if self._root:
            self._root=False
            return '<?xml version="1.0" encoding="UTF-8" ?>\n'
        else:
            # TODO: What should I do with this?
            return ''

# parse(InfiniteXML(), data_file, etree.parse(schema_file))
parse(data_file, etree.parse(schema_file))


