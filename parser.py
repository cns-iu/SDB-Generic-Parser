# Based on http://stackoverflow.com/questions/9809469/python-sax-to-lxml-for-80gb-xml
 
#!/usr/bin/env python
# import os
# import sys
# import re
# import resource
# import psycopg2
from time import gmtime, strftime
from lxml import etree
from collections import *
import OptParser
import unittest

parser = OptParser.config()
(options, args)     = parser.parse_args()
data_file           = options.data_file         or 'data_files/sample1.xml'
schema_file         = options.schema_file       or 'data_files/wos_config.xml'
parent_tag          = options.parent_tag        or 'records'
output_file_name    = options.output_file       or 'queries.txt'
record_tag          = options.record_tag        or 'REC'
id_tag              = options.unique_identifier or 'UID'
verbose             = options.verbose           or False
delimiter           = ':'
table_tag           = 'table'
counter_tag         = 'ctr_id'
reserved_keys       = [table_tag]

# Only works for numbers and strings, not objects.
def is_number(s):
    if type(s) is not str:
        return True
    else:
        return False

def verbose_exceptions(ex):
    if verbose:
        print(ex)
 
class Table():
    def __init__(self, **kwargs):
        self.name           = kwargs.get('name', '')
        self.fields         = kwargs.get('fields', [])
        self.values         = kwargs.get('values', [])
        self.storage        = []
        self.counter_name   = kwargs.get('counter_name', '')
        self.counter_value  = kwargs.get('counter_value', 0)
        self.parent_counters= kwargs.get('parent_counters', OrderedDict())
        self.xpath          = ''
    def add(self, obj):
        for key, val in [(key, val) for key, val in obj.items() if key is not id_tag]:
            self.fields.append(key)
            self.values.append(val)
        return self
    def clear(self):
        self.fields = []
        self.values = []
        return self
    def increment_counter_value(self):
        self.counter_value += 1
        return self
    def reset_counter_value(self):
        self.counter_value = 0
        return self
    def store(self):
        self.storage.append(Table(
            name=self.name,
            fields=self.fields,
            values=self.values,
            counter_name=self.counter_name,
            counter_value=self.counter_value,
            parent_counters=self.parent_counters
        ))

        return self.clear()
    def set_xpath(self, path):
        self.xpath = ('/'.join([str(x.tag) for x in path[1:]]))
    def stringify(self, coll, quote_type):
        strin = ''
        for item in coll:
            temp_item = ""
            if item is not "" and item is not None:
                if is_number(item):
                    temp_item = str(item)
                else:
                    temp_item = quote_type + item.strip().replace("'","''") + quote_type
            strin += temp_item + ','
        return strin[:-1]
    def sqlify(self, id):
        fieldstr = self.stringify(self.fields, '"')
        valuestr = self.stringify(self.values, "'")
        try:
            assert len(self.fields) == len(self.values)
        except:
            print(self.fields)
            print(self.values)
            raise Exception('Length mismatch. Field(' + str(len(self.fields)) + ') !== value(' + str(len(self.values)) + ')')
        try:
            assert id_tag not in self.fields
            assert len(self.fields) > 0
            if (delimiter in id):
                curr_id = id.split(delimiter)[1]
            else:
                curr_id = id
            # useQuotes = "'"
            #     curr_id = str(int(curr_id))
            # if is_number(curr_id):
            #     useQuotes = ""
            return 'INSERT INTO "' + self.name + '" (' + '"id",' + fieldstr + ') VALUES (' + curr_id  + ',' + valuestr + ');\n'
        except (Exception):
            pass

def get_table(table_list, tblstr):
    if tblstr not in table_list:
        table_list[tblstr] = Table(name=tblstr)
    return table_list[tblstr]
def get_parent_table(schema, path, table_list):
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
    return get_table(table_list, curr_tag)
def order_schema(source):
    context = etree.iterparse(source, events=('start', 'end',), remove_comments=True)
    arr = []
    [arr.append(elem.attrib.get(table_tag)) for event, elem in context if event == 'start' and elem.attrib.get(table_tag) is not None]
    return arr
def sort_statements(schema_order, table_list):
    ordered_list = []
    [ordered_list.append(x) for x in schema_order if x in table_list]
    return ordered_list
def parse(source, schema):
    # cnx = psycopg.connect(host='dbdev.cns.iu.edu', database='wos_test', user='wos_admin', password='57Ax34Fq')
    # cursor = cnx.cursor()
    # cursor.execute('SELECT file_number FROM admin.processing_record WHERE file_name = ' + source + ';')
    # file_number = cursor.fetchone()
    file_number = 1
    ordered_schema = order_schema(schema_file)
    f = open('sql_template.txt', 'r')
    sql_template = f.read()
    with open(output_file_name, 'w') as output_file:
        context         = etree.iterparse(source, events=('start', 'end',), remove_comments=True)
        path            = []
        primary_key     = None
        schema_match    = None
        table_list      = OrderedDict()
        open_tables     = []
        record_table    = None
        temp_parent_counter = None
        i = 0
        print ('Start time:           ' + strftime("%H:%M:%S", gmtime()))
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
                if elem.tag == id_tag: primary_key = elem.text
                try:
                    schema_match = schema.find('/'.join([str(x.tag) for x in path[1:]]))
                except (SyntaxError):
                    verbose_exceptions(SyntaxError)
                if schema_match is not None and schema_match.get(table_tag) is not None:
                    open_tables.append(schema_match.get(table_tag))
                    get_table(table_list, schema_match.get(table_tag)).set_xpath(path)
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

# *********************************************************
#   Record parser.
# *********************************************************
            if schema_match is not None:
                tbl = schema_match.get(table_tag)
                if tbl in open_tables:
                    curr_table = get_table(table_list, tbl)
                    curr_table.store()
                ctr = schema_match.get(counter_tag)
                counter_table = ''
                counter_name = ''

    # *********************************************************
    #   Counter generation.
    #   Creates or increments a counter based on the schema.
    #   Gets all counters from the open tables and stores
    #   them as parent tables, thereby creating a unique
    #   list of ids to be inserted into the SQL statements.
    # *********************************************************
                if ctr is not None and event == 'start':
                    counter_split = ctr.split(delimiter)
                    counter_table = counter_split[0]
                    counter_name = counter_split[1]

                    # if delimiter in ctr:
                    #     counter_split = ctr.split(delimiter)
                    #     counter_table = counter_split[0]
                    #     counter_name = counter_split[1]
                    # else:
                    #     counter_name = ctr

                    curr_table.counter_name = counter_name
                    parent_counters = OrderedDict()
                    for x in (x for x in open_tables if x is not None):
                        open_table = get_table(table_list, x)
                        if open_table.counter_name is not '':
                            parent_counters[open_table.counter_name] = open_table.counter_value
                    # print curr_table.storage[-1].parent_counters[curr_table.storage[-1].parent_counters.keys()[-1]]
                    # print curr_table.storage[-1].parent_counters.keys()[-1]
                    # if len(curr_table.storage) > 0:
                    #     if len(curr_table.storage[-1].parent_counters) > 0:
                    #         if curr_table.storage[-1].parent_counters[curr_table.storage[-1].parent_counters.keys()[-1]] == curr_table.parent_counters[curr_table.parent_counters.keys()[-1]]:
                    #             pass
                    #         else:
                    #             curr_table.counter_value = 0
                    curr_table.increment_counter_value()
                    curr_table.parent_counters = parent_counters
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

                        if schema_match.get(key) is not None:
                            attrib_split = schema_match.get(key).split(delimiter)
                            attrib_table = attrib_split[0]
                            attrib_field = attrib_split[1]

                            # if delimiter in schema_match.get(key):
                            #     attrib_split = schema_match.get(key).split(delimiter)
                            #     attrib_table = attrib_split[0]
                            #     attrib_field = attrib_split[1]
                            # else:
                            #     attrib_table = key
                            #     attrib_field = tbl
                            attrib_value = value
                            if attrib_table is None:
                                attrib_table = get_parent_table(schema, path, table_list).name
                            get_table(table_list, attrib_table).add({attrib_field: (attrib_value).encode('utf-8')})
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
                            if tbl is not None:
                                text_table = tbl
                            text_split = schema_match.text.split(delimiter)
                            text_table = text_split[0]
                            text_field = text_split[1]

                            # if delimiter in schema_match.text:
                            #     text_split = schema_match.text.split(delimiter)
                            #     text_table = text_split[0]
                            #     text_field = text_split[1]
                            # else:
                            #     text_table = schema_match.text.strip()
                            #     text_field = schema_match.text
                            text_value = elem.text
                            if text_table is None:
                                text_table = get_parent_table(schema, path, table_list).name
                            get_table(table_list, text_table).add({text_field: (text_value).encode('utf-8')})
                else:
                    record_table = tbl
    # *********************************************************
    #   Write data to file
    # *********************************************************
            if event == 'end' and elem.tag == record_tag:
                print("Processing record:    " + str(i), "               \r",)
                i += 1
                to_write = []
                ordered_table_list = sort_statements(ordered_schema, table_list)
                for table in ordered_table_list:
                    curr_table = get_table(table_list, table)
                    curr_table.store()
                    curr_table.storage = curr_table.storage[::-1]
                    while len(curr_table.storage) > 0:
                        to_write.append(curr_table.storage[-1].add({id_tag: (primary_key).encode('utf-8')}))
                        curr_table.storage.pop()
                    curr_table.storage = []
                curr_table.storage = []
                data_str = ""
                # for x in [y for y in to_write if y is not None]:

                for x in to_write:
                # x.parent_counters[x.counter_name] = x.counter_value
                    if x.counter_name is not None and x.counter_name is not "":
                        x.add({x.counter_name:x.counter_value})
                        x.parent_counters.pop(x.counter_name, None)
                    i = 1
                    for key, value in x.parent_counters.items():
                        x.add({key: i})
                        i += 1
                    # [x.add({key: value}) for key, value in x.parent_counters.iteritems() if value > 0]
                    if x.sqlify(primary_key) is not None:
                        data_str += '\t\t\t\t\t' + x.sqlify(primary_key)
                sql_template_copy = sql_template.replace('%pkey%', primary_key).replace('%data%', data_str).replace('%file_number%', str(file_number))
                output_file.write(sql_template_copy)
                table_list.clear()
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        print(' ')
    print('End time:             ' + strftime("%H:%M:%S", gmtime()))
    return True
parse(data_file, etree.parse(schema_file))

# cnx = psycopg.connect(host='dbdev.cns.iu.edu', database='wos_test', user='wos_admin', password='57Ax34Fq')
# cursor = cnx.cursor()
# cursor.execute('SELECT file_number FROM admin.processing_record WHERE file_name = ' + data_file + ';')
# data = cursor.fetch()
# print cursor.fetchone()
