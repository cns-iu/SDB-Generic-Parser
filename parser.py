# Based on http://stackoverflow.com/questions/9809469/python-sax-to-lxml-for-80gb-xml

#!/usr/bin/python
# -*- coding: utf-8 -*-
# import os
import sys
# import re
# import resource
# import psycopg2
from time import gmtime, strftime
from lxml import etree
from collections import *
from ordereddict import OrderedDict
import OptParser
from TableClass import Table
from os import listdir
from os.path import isfile, join
import unittest
import os


parser              = OptParser.config()
(options, args)     = parser.parse_args()
dir_path            = options.dir_path          or ''
data_file           = options.data_file         or 'test_files/sample1.xml'
schema_file         = options.schema_file       or 'wos_config.xml'
template_file       = options.template_file     or 'sql_template.sql'
parent_tag          = options.parent_tag        or 'records'
record_tag          = options.record_tag        or 'REC'
id_tag              = options.unique_identifier or 'UID'
verbose             = options.verbose           or True
delimiter           = ':'
table_quote         = options.table_quote       or '\"'
table_tag           = 'table'
counter_tag         = 'ctr_id'
reserved_keys       = [table_tag]

sql_template_file = open(template_file, 'r')
sql_template = sql_template_file.read()
sql_template_file.close()

def verbose_exceptions(ex):
    if verbose:
        print(ex)

def get_table(table_list, tblstr):
    if tblstr not in table_list:
        table_list[tblstr] = Table(name=tblstr, id_tag=id_tag, table_quote=table_quote, delimiter=delimiter)
    return table_list[tblstr]

def order_schema():
    """
    Performs an initial parse of the schema file and
        maps out the proper table hierarchy so the statements
        can be organized before written to the file.

    :return: list of tables in the schema.
    """
    context = etree.iterparse(schema_file, events=('start', 'end',), remove_comments=True)
    arr = []
    [arr.append(elem.attrib.get(table_tag)) for event, elem in context if
    event == 'start' and elem.attrib.get(table_tag) is not None]
    return arr

def sort_statements(schema_order, table_list):
    ordered_list = []
    [ordered_list.append(x) for x in schema_order if x in table_list]
    return ordered_list

def parse_attr(elem, tbl, schema_match, schema, path, table_list, open_tables):
    """
        Tag attribute items. Ex: <tag attribute="attribute value">
            Match the schema tag to the data tag. Use the
            value from the schema to map the value from
            the data. The schema attribute item values
            usually include the table as well. That is
            handled by splitting a string if the delimiter
            exists.
    """
    for key, value in elem.attrib.items():
        attrib_table = None
        attrib_field = None
        attrib_value = None
        if schema_match.get(key) is not None:
            attrib_split = schema_match.get(key).split(delimiter)
            if delimiter in schema_match.get(key):
                attrib_split = schema_match.get(key).split(delimiter)
                attrib_table = attrib_split[0]
                attrib_field = attrib_split[1]
            else:
                attrib_table = key
                attrib_field = tbl
            attrib_value = value
            if attrib_table is None:
                attrib_table = open_tables[-1]
            get_table(table_list, attrib_table).add({attrib_field: attrib_value})

def parse_text(elem, tbl, schema_match, schema, path, table_list, open_tables):
    """
        Tag element text. Ex: <tag>tag element text
            Match the schema text to the data text. Use the
            text from the schema to map the text from
            the data. The schema text is usually include the
            table as well. That is handled by splitting a
            string if the delimiter exists.
    """
    # print('Parsing text')
    if elem.text:
        text_table = None
        text_field = None
        text_value = None
        if elem.text.strip():
            if tbl is not None:
                text_table = tbl
                # print('Text table: '+ text_table)
            if schema_match.text is not None and delimiter in schema_match.text:
                # print('Delimiter: '+ delimiter)
                # print('Schema match: '+ schema_match.text)
                text_split = schema_match.text.split(delimiter)
                text_table = text_split[0]
                text_field = text_split[1]
            else:
                text_table = open_tables[-1]
                text_field = schema_match.text
            text_value = elem.text
            if text_table is None:
                text_table = open_tables[-1]
            get_table(table_list, text_table).add({text_field: text_value})

def parse_counters(schema_match, table_list, open_tables, ctr, curr_table, event):
    """
        Counter handling. For each instance of a counter we find, we need to
            find the current counter and increment it, while also searching
            for all parent counters to add to the write. If a table is closed
            all of the child counters' values should reset.
    """
    if ctr is not None and delimiter in ctr:
        ctr = ctr.split(delimiter)[1]
        curr_table.counter_name = ctr
        if event == "start":
            open_tables_no_null_with_counters = [y for y in [x for x in open_tables if x is not None] if get_table(table_list, y).counter_name is not '']
            if (len(curr_table.parent_counters) > 0) and (len(open_tables_no_null_with_counters) > 1):
                live_table = get_table(table_list, open_tables_no_null_with_counters[-2])
                live_counters = live_table.parent_counters.copy()
                live_counters[live_table.counter_name] = live_table.counter_value

                curr_counters = curr_table.parent_counters.copy()

                if live_counters == curr_counters:
                    curr_table.counter_value += 1
                else:
                    curr_table.counter_value = 1
            else:
                curr_table.counter_value += 1
            for otnnwc in open_tables_no_null_with_counters[:-1]:
                open_table_not_null_with_counter = get_table(table_list, otnnwc)
                curr_table.parent_counters[open_table_not_null_with_counter.counter_name] = open_table_not_null_with_counter.counter_value
            curr_table.queue_counter({curr_table.counter_name: curr_table.counter_value})
            for write in curr_table.parent_counters.items():
                curr_table.queue_counter({write[0]: write[1]})
            curr_table.dequeue_counters()

def write_to_file(elem, table_list, event, primary_key, output_file, file_number):
    if event == 'end' and elem.tag == record_tag:
        to_write = []
        ordered_table_list = sort_statements(ordered_schema, table_list)
        # print(ordered_table_list)
        for table in ordered_table_list:
            # print(table)
            curr_table = get_table(table_list, table)
            curr_table.store()
            curr_table.storage = curr_table.storage[::-1]
            while len(curr_table.storage) > 0:
                temp = curr_table.storage[-1]
                to_write.append(temp.add({id_tag: primary_key}))
                curr_table.storage.pop()
            curr_table.storage = []
        data_str = ""
        for x in to_write:
            sqx = x.sqlify(primary_key)

            if sqx is not None and len(to_write) > 0:
                data_str += '\t\t\t\t\t' + sqx
        output_file.write(sql_template.replace('%pkey%', primary_key).replace('%data%', data_str).replace('%file_number%',str(file_number)).encode('utf-8'))
        table_list.clear()

def write_to_cache(output_cache, elem, table_list, event, primary_key, output_file, file_number):
    cache_line = {'elem': elem, 'table_list': table_list, 'event': event, 'primary_key': primary_key, 'output_file': output_file, 'file_number': file_number}
    output_cache.append(cache_line)
    # print(len(output_cache))

def write_cached_lines(output_cache, primary_key):
    if output_cache is not None:
        for line in output_cache:
            if primary_key is not None:
                # print('PK passed: ' + primary_key)
                write_to_file(line['elem'], line['table_list'], line['event'], primary_key, line['output_file'], line['file_number'])
            else:
                # print('PK from line: ' + line['primary_key'])
                write_to_file(line['elem'], line['table_list'], line['event'], line['primary_key'], line['output_file'], line['file_number'])
    # else:
        # print('Cache is empty')

def int_or_varchar(s):
    if s is not None:
        try: 
            int(s)
            return s
        except ValueError:
            return "'" + s + "'"
    else:
        return s

def parse_single(source, schema):
    # cnx = psycopg.connect(host='dbdev.cns.iu.edu', database='wos_test', user='wos_admin', password='57Ax34Fq')
    # cursor = cnx.cursor()
    # cursor.execute('SELECT file_number FROM admin.processing_record WHERE file_name = ' + source + ';')
    # file_number = cursor.fetchone()
    file_number = 1

    with open("output/" + source.split("/")[-1].split(".")[0] + "-queries.txt", 'wb') as output_file:
        context         = etree.iterparse(source, events=('start', 'end',), remove_comments=True)
        path            = []
        primary_key     = None
        schema_match    = None
        table_list      = OrderedDict()
        open_tables     = []
        output_cache    = []
        cache_writes    = True
        print('Start time:           ' + strftime("%H:%M:%S", gmtime()))
        for event, elem in context:
# *********************************************************
# XML event catchers.
    # *********************************************************
    #   Start event.
    #   When a new tag opens, try to match the schema to the
    #   data.
            if event == 'start':
                # print('Started: ' + elem.tag)
                path.append(elem)
                # print(path)
                if elem.tag == id_tag and elem.text is not None:
                    primary_key = elem.text
                    cache_writes = False
                    write_cached_lines(output_cache, primary_key)
                    # print(id_tag + ': ' + elem.text)
                # print('++' + elem.tag + ': ' + elem.text + '--')
                try:
                    # schema_prefix = '' if record_tag == elem.tag else '/'
                    schema_to_match = ''
                    if parent_tag == elem.tag:
                        schema_match = schema.getroot()
                    else:
                        if record_tag == elem.tag:
                            schema_to_match = elem.tag
                        else:
                            schema_to_match = '/'.join([x.tag for x in path[1:]])
                        # print('Schema to match: ' + schema_to_match)
                        schema_match = schema.find(schema_to_match)
                    # print(schema_match.tag)
                    # print(schema_match.get(table_tag))
                except (SyntaxError):
                    verbose_exceptions("Could not match schema to data: " + str(elem.tag))
                if schema_match is not None and schema_match.get(table_tag) is not None:
                    open_tables.append(schema_match.get(table_tag))
                    get_table(table_list, schema_match.get(table_tag)).set_xpath(path)
                else:
                    open_tables.append(None)
                    # open_tables.append(open_tables[-1])
                # print(open_tables)
    # *********************************************************
    #   End event.
    #   When an open tag closes, build strings from each table
    #   built through the parsing.
            if event == 'end':
                path.pop()
                open_tables.pop()
                # try:
                #     assert primary_key is not None
                # except AssertionError:
                #     raise Exception(
                #         'Cannot find a primary key. Make sure the id_tag value ["' + id_tag + '"] matches the primary key tag in the data.')
    # *********************************************************
    #   Record parser.
            if schema_match is not None:
                tbl = schema_match.get(table_tag)
                ctr = schema_match.get(counter_tag)
                curr_table = get_table(table_list, tbl)
                if tbl in open_tables:
                    curr_table.store()
                    if curr_table.counter_name is not '':
                        curr_table.queue_counter({curr_table.counter_name:1})
                        # curr_table.add({curr_table.counter_name:1})
                # if elem.tag != record_tag:
                # print('Parsing: ' + '++' + elem.tag + '--')
                parse_attr(elem, tbl, schema_match, schema, path, table_list, open_tables)
                parse_text(elem, tbl, schema_match, schema, path, table_list, open_tables)
                parse_counters(schema_match, table_list, open_tables, ctr, curr_table, event)
                if event == 'start' and schema_match.get("file_number") is not None:
                    curr_table.add({"file_number": file_number})

            if cache_writes:
                write_to_cache(output_cache, elem, table_list, event, 'None', output_file, file_number)
            else:
                write_to_file(elem, table_list, event, primary_key, output_file, file_number)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
    print('End time:             ' + strftime("%H:%M:%S", gmtime()))
    return True

if not os.path.exists("output"):
    os.makedirs("output")

ordered_schema = order_schema()
parsed_schema = etree.parse(schema_file)
# print(parsed_schema.find('..').tag)
if dir_path is not "":
    print(listdir(dir_path))
    for f in listdir(dir_path):
        if isfile(join(dir_path, f)):
            if f.endswith('.xml'):
                parse_single(dir_path + "/" + f, parsed_schema)
else:
    parse_single(data_file, parsed_schema)