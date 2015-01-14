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
storage             = []

class Table():
    def __init__(self, table_name, fields, values):
        self.table_name = table_name
        self.fields     = fields
        self.values     = values
    def add(self, obj):
        for key, val in obj.iteritems():
            if key is not id_tag:
                self.fields.append(key)
                self.values.append(val)
        return self
    def clear(self):
        self.fields = []
        self.values = []
        return self
    def store(self):
        storage.append(Table(self.table_name, self.fields, self.values))
        return self.clear()
    def stringify(self, coll):
        str = ''
        for item in coll:
            temp_item = item.strip()
            if (temp_item == ""):
                pass
            else:
                str += '"' + item.strip() + '",'
        return str[:-1]
    def sqlify(self, id, delete):
        fieldstr = self.stringify(self.fields)
        valuestr = self.stringify(self.values)
        try:
            assert len(self.fields) == len(self.values)
        except:
            print self.fields
            print self.values
            raise Exception('Length mismatch. Field(' + str(len(self.fields)) + ') !== value(' + str(len(self.values)) + ')')
        if delete:
            return 'DELETE FROM "' + self.table_name + '" WHERE ("' + id_tag + '" = "' + id + '");\n'
        else:
            try:
                assert 'UID' not in self.fields
                assert len(self.fields) > 0
                return 'INSERT INTO "' + self.table_name + '" (' + '"' + id_tag + '",' + fieldstr + ') VALUES ("' + id + '",' + valuestr + ');\n'
            except Exception, e:
                print e
                pass
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
        context = etree.iterparse(source, events=('start', 'end'), remove_comments=True)
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
                    try:
                        assert primary_key is not None
                    except AssertionError:
                        raise Exception('Cannot find a primary key. Make sure the id_tag value ["' + id_tag + '"] matches the primary key tag in the data.')
                        # TODO: Pause the parse here.
                        return False
                    delete = False
                    if primary_key in id_list:
                        delete = True
                    else:
                        id_list.append(primary_key)
                    to_write = []
                    to_reverse_then_write = []
                    # TODO: This can be cleaned up a bit.
                    for table in table_list:
                        curr_table = find_table(table)
                        for stored in storage:
                            to_write.append(stored.add({id_tag: primary_key}).sqlify(primary_key, False))
                            if delete:
                                to_reverse_then_write.append(curr_table.sqlify(primary_key, True))
                        to_write.append(curr_table.add({id_tag: primary_key}).sqlify(primary_key, False))
                    for x in reversed(to_reverse_then_write):
                        try:
                            output_file.write(x.encode('utf-8'))
                        except:
                            pass
                    for x in to_write:
                        try:
                            output_file.write(x.encode('utf-8'))
                        except:
                            pass
                    table_list.clear()
# *********************************************************
#   XML parser.
# *********************************************************
            if schema_match is not None:
                attrib_table = None
                attrib_field = None
                if schema_match.get(table_tag) is not None:
                    attrib_table = schema_match.get(table_tag)
                    find_table(attrib_table).store()

                # *********************************************************
                #   Tag attribute items. Ex: <tag attribute="attribute value">
                #       Match the schema tag to the data tag. Use the
                #       value from the schema to map the value from
                #       the data. The schema attribute item values
                #       usually include the table as well. That is
                #       handled by splitting a string if the delimiter
                #       exists.
                # *********************************************************
                try:
                    assert len(elem.attrib.items()) > 0
                    assert len(schema_match.attrib.items()) > 0
                    for key, value in elem.attrib.items():
                        schema_attrib = schema_match.get(key)
                        try:
                            if delimiter in schema_attrib:
                                attrib_split = schema_attrib.split(delimiter)
                                assert len(attrib_split) == 2
                                if schema_match.attrib.get('table') is not None:
                                    # TODO; CHECK NEW?
                                    find_table(attrib_split[0]).store()
                                find_table(attrib_split[0]).add({attrib_split[1]: value})
                        except TypeError, e:
                            #TODO: What to do here?
                            pass
                        except AssertionError, e:
                            #TODO: What to do here?
                            pass
                            #SUB1
                except:
                    #TODO: What to do here?
                    pass
                # *********************************************************
                #   Tag element text. Ex: <tag>tag element text
                #       Match the schema text to the data text. Use the
                #       text from the schema to map the text from
                #       the data. The schema text is usually include the
                #       table as well. That is handled by splitting a
                #       string if the delimiter exists.
                # *********************************************************
                try:
                    assert len(elem.text) > 0
                    assert len(schema_match.text) > 0
                    if delimiter in schema_match.text:
                        attrib_split = schema_match.text.split(delimiter)
                        # if schema_match.attrib.get('table') is not None:
                        #     find_table(attrib_split[0]).store()
                        attrib_table = find_table(attrib_split[0])
                        attrib_field = attrib_split[1]
                        # elif curr_table is not None:
                        #     attrib_table = curr_table
                        #     attrib_field = schema_match.text
                    attrib_value = elem.text
                    # else:
                    #     pass
                except:
                    #TODO: What to do here?
                    pass
                # *********************************************************
                #   Add the fields to the current table for final
                #   string building.
                # *********************************************************
                try:
                    assert len(attrib_field.strip()) > 0
                    assert len(attrib_value.strip()) > 0
                    attrib_table.fields.append(attrib_field)
                    attrib_table.values.append(attrib_value)
                except AssertionError:
                    pass
                except AttributeError:
                    pass
            elem.clear()

            while elem.getprevious() is not None:
                del elem.getparent()[0]
    return True

class TableClass_Add(unittest.TestCase):
    def test(self):
        self.assertEqual(Table('test_table', [], []).add({'test_field':'test_value'}).sqlify(primary_key), 'INSERT INTO "test_table" ("test_field") VALUES ("test_value");\n')
class TableClass_Clear(unittest.TestCase):
    def test(self):
        self.assertEqual(Table('test_table', ['test_field'], ['test_value']).clear().sqlify(primary_key), 'INSERT INTO "test_table" () VALUES ();\n')
# class TableClass_Store(unittest.TestCase):
#     def test(self):
#         self.assertEqual(Table('test_table', ['test_field'], ['test_value']).store().sqlify(), 'INSERT INTO "test_table" () VALUES ();\n')
#         self.assertEqual(len(Table('test_table', ['test_field'], ['test_value']).store().storage), 1)
class TableClass_Stringify(unittest.TestCase):
    def test(self):
        self.assertEqual(Table('', [], []).stringify(['Test', '1', '2']), '"Test","1","2"')
        self.assertEqual(Table('', [], []).stringify(['', '', '']), '')
        self.assertTrue(True)
# class TableClass_SQLify(unittest.TestCase):
#     def test(self):
#         self.assertEqual(Table('test_table', [], []).sqlify(primary_key), 'INSERT INTO "test_table" () VALUES ();\n')
#         self.assertEqual(Table('test_table', ['test_field'], ['test_value']).sqlify(primary_key), 'INSERT INTO "test_table" ("test_field") VALUES ("test_value");\n')
#         self.assertEqual(Table('test_table', [], []).sqlify('primary_key'), 'DELETE FROM "test_table" WHERE ("UID" = "primary_key");\n')
#         self.assertRaises(Exception, Table('test_table', [], ['test_value']))
#         self.assertRaises(Exception, Table('test_table', ['test_field'], []))
#         # TODO: Disconnect the file write for the test.
#         self.assertTrue(parse('test_files/test_data.xml', etree.parse('test_files/test_schema.xml')))
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
parse('test_files/test_data.xml', etree.parse('test_files/test_schema.xml'))
# parse(data_file, etree.parse(schema_file))
# parse(InfiniteXML(), data_file, etree.parse(schema_file))
