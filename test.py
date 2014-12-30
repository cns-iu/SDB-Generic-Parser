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
        '-d', '--datafile',
        action='store', type='string', dest='data_file',
        help='file name and path of the XML file to be processed. ex: data_file_name.xml')
parser.add_option(
        '-s', '--schemafile', 
        action='store', type='string', dest='schema_file',
        help='file name and path of the XML schema file. ex: data_file_name.xml')
parser.add_option(
        '-r', '--root', 
        action='store', type='string', dest='root_str',
        help='the top-most element of the XML. ex: REC')

(options, args)     = parser.parse_args()
data_file           = 'sample1.xml'
schema_file         = 'test.xml'
output_file_name    = 'out.txt'
parent_tag          = 'records'
record_tag          = 'REC'
delimiter           = ':'
id_tag              = 'UID'
table_tag           = 'table'
id_list             = []
reserved_keys       = [table_tag]
table_list          = dict()
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

class Table():
    def __init__(self, table_name, fields, values):
        self.table_name = table_name
        self.fields = fields
        self.values = values
    def add(self, obj):
        for key, val in obj.iteritems():
            assert key not in self.fields
            self.fields.append(key)
            self.values.append(val)
        return self
    def sqlify(self, *args):
        fieldstr = ''
        valuestr = ''

        for field in self.fields:
            fieldstr += '"' + field.strip() + '",'
        for value in self.values:
            valuestr += '"' + value.strip() + '",'
        #Remove trailing commas
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
    
def parse(fp, source, schema):
    with open(output_file_name, 'w') as output_file:
        context = etree.iterparse(source, events=('start', 'end'))
        path = []
        curr_table = None
        schema_match = None
        primary_key = None
        for event, elem in context:
            if event == 'start':
                if elem.tag == id_tag:
                    primary_key = elem.text
                path.append(elem)
                try:
                    schema_match = schema.find('/'.join([str(x.tag) for x in path[1:]])[len(record_tag):])
                    table_something = schema_match.get(table_tag)
                    if table_something is not None:
                        curr_table = find_table(table_something)
                except:
                    pass
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
                        if delete:
                            to_reverse_then_write.append(curr_table.sqlify(primary_key))
                        to_write.append(curr_table.add({id_tag:primary_key}).sqlify())
                    #TODO: What's with these .strip()pers?
                    for x in reversed(to_reverse_then_write):
                        output_file.write(x.encode('utf-8'))
                    for x in to_write:
                        output_file.write(x.encode('utf-8'))
                    table_list.clear()

            if schema_match is not None:
                attrib_table = None
                attrib_field = None
                if elem.attrib.items():
                    for key, value in elem.attrib.items():
                        schema_attrib = schema_match.get(key)
                        try:
                            if delimiter in schema_attrib:
                                attrib_split = schema_attrib.split(delimiter)
                                assert len(attrib_split) == 2
                                find_table(attrib_split[0]).add({attrib_split[1]: value})
                        except TypeError:
                            pass
                        except AssertionError:
                            #TODO: What to do here?
                            pass
                        #SUB1
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
parse(InfiniteXML(), data_file, etree.parse(schema_file))


