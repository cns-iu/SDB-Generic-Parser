#!/usr/bin/env python
# import os
# import sys
# import re
# import resource
# import time
from lxml import etree
from optparse import OptionParser
import unittest
# TODO: The parser fails if there are comments or namespaces in the root. How do I fix this?
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
        '-m', '--master_table',
        action='store', type='string', dest='master_table',
        help='the name of the master table. When checking for a duplicate record, what table should we delete from to trigger the cascade delete. Default: \'wos:master\'')
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
parser.add_option(
        '-v', '--verbose',
        action='store', type='string', dest='verbose',
        help='boolean to determine whether exceptions should be displayed. Default: True')
(options, args)     = parser.parse_args()
data_file           = options.data_file         or 'data_files/sample1.xml'
schema_file         = options.schema_file       or 'data_files/wos_config.xml'
parent_tag          = options.parent_tag        or 'records'
output_file_name    = options.output_file       or 'queries.txt'
# TODO: Use table in record tag
record_tag          = options.record_tag        or 'REC'
id_tag              = options.unique_identifier or 'UID'
verbose             = options.verbose           or False
delimiter           = ':'
table_tag           = 'table'
counter_tag         = 'ctr_id'
reserved_keys       = [table_tag]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Table():
    def __init__(self, table_name, fields, values, counter):
        self.table_name = table_name
        self.fields     = fields
        self.values     = values
        self.storage    = []
        self.counter    = 0
    def add(self, obj):
        for key, val in obj.iteritems():
            if key is not id_tag:
                self.fields.append(key)
                self.values.append(val)
        return self
    def clear(self):
        self.fields = []
        self.values = []
        self.counter = 0
        return self
    def increment_counter(self):
        self.counter += 1
    def reset_counter(self):
        self.counter = 0
    def store(self):
        self.storage.append(Table(self.table_name, self.fields, self.values, self.counter))
        return self.clear()
    def stringify(self, coll, quote_type):
        str = ''
        for item in coll:
            temp_item = item.strip()
            if (temp_item == ""):
                pass
            else:
                str += quote_type + item.strip() + quote_type + ','
        return str[:-1]
    def sqlify(self, id):
        fieldstr = self.stringify(self.fields, '"')
        valuestr = self.stringify(self.values, "'")
        try:
            assert len(self.fields) == len(self.values)
        except:
            print self.fields
            print self.values
            raise Exception('Length mismatch. Field(' + str(len(self.fields)) + ') !== value(' + str(len(self.values)) + ')')
        try:
            assert id_tag not in self.fields
            assert len(self.fields) > 0
            if (delimiter in id):
                curr_id = id.split(delimiter)[1]
            else:
                curr_id = id
            useQuotes = "'"
            if is_number(curr_id):
                useQuotes = ""
                curr_id = str(int(curr_id))
            return 'INSERT INTO "' + self.table_name + '" (' + '"id",' + fieldstr + ') VALUES (' + (useQuotes + curr_id + useQuotes) + ',' + valuestr + ');\n'
        except Exception, e:
            pass
def find_table(table_list, tblstr):
    if tblstr in table_list:
        pass
    else:
        table_list[tblstr] = Table(tblstr, [], [], 0)
    return table_list[tblstr]
def find_parent_table(schema, path, table_list):
    curr_tag = None
    i = -1
    while curr_tag is None:
        xpath_string = ('/'.join([str(x.tag) for x in path[1:i]]))
        parent_search = schema.find(xpath_string)
        try:
            curr_tag = parent_search.get(table_tag)
        except:
            pass
        i -= 1
    return find_table(table_list, curr_tag)
def verbose_exceptions(ex):
    if verbose:
        print ex
def create_schema_order(source):
    context = etree.iterparse(source, events=('start', 'end',), remove_comments=True)
    arr = []
    for event, elem in context:
        if event == 'start':
            if elem.attrib.get(table_tag) is not None:
                arr.append(elem.attrib.get(table_tag))
    return arr
def find_counters(schema, path, table_list):
    i = 0
    list = []
    for x in path:
        xpath_string = ('/'.join([str(x.tag) for x in path[1:i]]))
        i -= 1
        try:
            parent_search = schema.find(xpath_string)
            if parent_search.get(counter_tag) is not None:
                print parent_search.get(counter_tag)
        except Exception, e:
            print e
            pass


def sort_statements(schema_order, table_list):
    ordered_list = []
    for x in schema_order:
        if x in table_list:
            ordered_list.append(x)
    return ordered_list
# def parse(fp, source, schema):
def parse(source, schema):
    ordered_schema = create_schema_order(schema_file)
    with open(output_file_name, 'w') as output_file:
        context = etree.iterparse(source, events=('start', 'end',), remove_comments=True)
        path = []
        primary_key = None
        schema_match = None
        table_list = dict()
        open_tables = []
        record_table = None
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
                path.append(elem)
                if elem.tag == id_tag:
                    primary_key = elem.text
                try:
                    schema_match = schema.find('/'.join([str(x.tag) for x in path[1:]]))
                except SyntaxError, e:
                    verbose_exceptions(e)
                if schema_match is not None:
                    if schema_match.get(table_tag) is not None:
                        open_tables.append(schema_match.get(table_tag))
                    else:
                        open_tables.append(None)
                else:
                    open_tables.append(None)
    # *********************************************************
    #   End event.
    #   When an open tag closes, build strings from each table
    #   built through the parsing.
    # *********************************************************
            if event == 'end':
                path.pop()
                open_tables.pop()
                try:
                    assert primary_key is not None
                except AssertionError:
                    raise Exception('Cannot find a primary key. Make sure the id_tag value ["' + id_tag + '"] matches the primary key tag in the data.')
                if elem.tag == record_tag:
                    find_counters(schema, path, table_list)
                    to_write = []
                    ordered_table_list = sort_statements(ordered_schema, table_list)
                    for table in ordered_table_list:
                        # I know how stupid this is. But I'm getting an error trying to add another statement to my loop
                        curr_table = find_table(table_list, table)
                        curr_table.storage = curr_table.storage[::-1]
                        while len(curr_table.storage) > 0:
                            to_write.append(curr_table.storage[-1].add({id_tag: primary_key}).sqlify(primary_key))
                            curr_table.storage.pop()
                        curr_table.storage = []
                        to_write.append(curr_table.add({id_tag: primary_key}).sqlify(primary_key))
                    curr_table.storage = []
                    output_file.write('--------------------------------------------\n')
                    output_file.write('BEGIN;\n')
                    output_file.write('\tDO\n')
                    output_file.write('\t$do$\n')
                    output_file.write('\t\tBEGIN\n')
                    # TODO: Notify Daniel of updated quotes on primary key and ask if file_number needs quotes
                    output_file.write('\t\t\tIF EXISTS(SELECT 1 FROM "wos_master" WHERE "wos_uid" = \'' + primary_key + '\' AND \'file_number\' <= 1)\n')
                    output_file.write('\t\t\t\tTHEN\n')
                    output_file.write('\t\t\t\t\tDELETE FROM "wos_master" WHERE "wos_uid" = \'' + primary_key + '\';\n')
                    output_file.write('\t\t\tEND IF;\n')
                    output_file.write('\t\t\tIF NOT EXISTS(SELECT 1 FROM "wos_master" WHERE "wos_uid" = \'' + primary_key + '\' AND \'file_number\' > 1) \n')
                    output_file.write('\t\t\t\tTHEN\n')

                    for x in [y.encode('utf-8') for y in to_write if y is not None]:
                        output_file.write('\t\t\t\t\t' + x)

                    output_file.write('\t\t\tEND IF;\n')
                    output_file.write('\t\tEND \n')
                    output_file.write('\t$do$;\n')
                    output_file.write('COMMIT;\n')
                    table_list.clear()
# *********************************************************
#   XML parser.
# *********************************************************
            if schema_match is not None:
                if schema_match.get(table_tag) in open_tables:
                    find_table(table_list, schema_match.get(table_tag)).store()

    # *********************************************************
    #   Tag attribute items. Ex: <tag attribute="attribute value">
    #       Match the schema tag to the data tag. Use the
    #       value from the schema to map the value from
    #       the data. The schema attribute item values
    #       usually include the table as well. That is
    #       handled by splitting a string if the delimiter
    #       exists.
    # *********************************************************
                if elem.tag != record_tag:
                    for key, value in elem.attrib.items():
                        attrib_table = None
                        attrib_field = None
                        attrib_value = None
                        if schema_match.get(table_tag) is not None:
                            attrib_table = schema_match.get(table_tag)
                            if schema_match.get(counter_tag) is not None:
                                find_table(table_list, attrib_table).increment_counter()
                        else:
                            if schema_match.get(key) is not None:
                                if delimiter in schema_match.get(key):
                                    attrib_split = schema_match.get(key).split(delimiter)
                                    attrib_table = attrib_split[0]
                                    attrib_field = attrib_split[1]
                                else:
                                    attrib_table = key
                                    attrib_field = schema_match.get(table_tag)
                                attrib_value = value
                                if attrib_table is None:
                                    attrib_table = find_parent_table(schema, path, table_list).table_name
                                find_table(table_list, attrib_table).add({attrib_field: attrib_value})

    # *********************************************************
    #   Tag element text. Ex: <tag>tag element text
    #       Match the schema text to the data text. Use the
    #       text from the schema to map the text from
    #       the data. The schema text is usually include the
    #       table as well. That is handled by splitting a
    #       string if the delimiter exists.
    # *********************************************************
                    if elem.text:
                        text_table = None
                        text_field = None
                        text_value = None
                        if elem.text.strip():
                            if schema_match.get(table_tag) is not None:
                                text_table = schema_match.get(table_tag)
                            if delimiter in schema_match.text:
                                text_split = schema_match.text.split(delimiter)
                                text_table = text_split[0]
                                text_field = text_split[1]
                            else:
                                text_table = schema_match.text.strip()
                                text_field = schema_match.text
                            text_value = elem.text
                            if text_table is None:
                                text_table = find_parent_table(schema, path, table_list).table_name
                            find_table(table_list, text_table).add({text_field: text_value})
                else:
                    record_table = schema_match.get(table_tag)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
    return True

# Based on http://stackoverflow.com/questions/9809469/python-sax-to-lxml-for-80gb-xml
class InfiniteXML (object):
    def __init__(self):
        self._root = True
    def read(self, len=None):
        if self._root:
            self._root=False
            return '<?xml version="1.0" encoding="UTF-8" ?>\n'
        else:
            #TODO: What to do here?
            return ''
parse(data_file, etree.parse(schema_file))

class TableClass_Add(unittest.TestCase):
    def test(self):
        self.assertEqual(Table('test_table', [], []).add({'test_field':'test_value'}).sqlify('uid:test', False), 'INSERT INTO "test_table" ("UID","test_field") VALUES ("uid:test","test_value");\n')
class TableClass_Clear(unittest.TestCase):
    def test(self):
        self.assertEqual(Table('test_table', ['test_field'], ['test_value']).clear().sqlify('uid:test', False), None)
class TableClass_Store(unittest.TestCase):
    def test(self):
        self.assertEqual(Table('test_table', ['test_field'], ['test_value']).store([]).sqlify('uid:test', False), None)
        self.assertEqual(len(Table('test_table', ['test_field'], ['test_value']).store([]).storage), 1)
class TableClass_Stringify(unittest.TestCase):
    def test(self):
        self.assertEqual(Table('', [], []).stringify(['Test', '1', '2']), '"Test","1","2"')
        self.assertEqual(Table('', [], []).stringify(['', '', '']), '')
        self.assertTrue(True)
class TableClass_SQLify(unittest.TestCase):
    def test(self):
        self.assertEqual(Table('test_table', [], []).sqlify('uid:test', False), None)
        self.assertEqual(Table('test_table', ['test_field'], ['test_value']).sqlify('uid:test', False), 'INSERT INTO "test_table" ("UID","test_field") VALUES ("uid:test","test_value");\n')
        self.assertEqual(Table('test_table', [], []).sqlify('uid:test', True), 'DELETE FROM "test_table" WHERE ("UID" = "uid:test");\n')
        self.assertRaises(Exception, Table('test_table', [], ['test_value']))
        self.assertRaises(Exception, Table('test_table', ['test_field'], []))
        # TODO: Disconnect the file write for the test.
        self.assertTrue(parse('test_files/test_data.xml', etree.parse('test_files/test_schema.xml')))
