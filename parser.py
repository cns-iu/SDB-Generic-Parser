# Based on http://stackoverflow.com/questions/9809469/python-sax-to-lxml-for-80gb-xml

# !/usr/bin/env python
# import os
# import sys
# import re
# import resource
# import psycopg2
from time import gmtime, strftime
from lxml import etree
from collections import *
import OptParser
from TableClass import Table
from os import listdir
from os.path import isfile, join
import unittest

parser = OptParser.config()
(options, args) = parser.parse_args()
data_file = options.data_file or 'data_files/isolated_parse_issue.xml'
schema_file = options.schema_file or 'wos_config.xml'
parent_tag = options.parent_tag or 'records'
record_tag = options.record_tag or 'REC'
id_tag = options.unique_identifier or 'UID'
verbose = options.verbose or False
dir_path            = options.dir_path          or "C:/Users/adhsimps/Documents/Workspaces/Python/SDB-generic_parser/data_files"
dir_path = "data_files"
delimiter = ':'
table_tag = 'table'
counter_tag = 'ctr_id'
reserved_keys = [table_tag]
f = open('sql_template.txt', 'r')
sql_template = f.read()


def verbose_exceptions(ex):
    if verbose:
        print(ex)

def get_table(table_list, tblstr):
    if tblstr not in table_list:
        table_list[tblstr] = Table(name=tblstr, id_tag=id_tag, delimiter=delimiter)
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
    [arr.append(elem.attrib.get(table_tag)) for event, elem in context if
     event == 'start' and elem.attrib.get(table_tag) is not None]
    return arr


def sort_statements(schema_order, table_list):
    ordered_list = []
    [ordered_list.append(x) for x in schema_order if x in table_list]
    return ordered_list


def parse_attr(elem, tbl, schema_match, schema, path, table_list, event):
    # *********************************************************
    # Tag attribute items. Ex: <tag attribute="attribute value">
    #       Match the schema tag to the data tag. Use the
    #       value from the schema to map the value from
    #       the data. The schema attribute item values
    #       usually include the table as well. That is
    #       handled by splitting a string if the delimiter
    #       exists.
    # *********************************************************
    for key, value in elem.attrib.items():
        attrib_table = None
        attrib_field = None
        attrib_value = None

        if schema_match.get(key) is not None:

            attrib_split = schema_match.get(key).split(delimiter)
            # TODO: Does this make sense?
            if delimiter in schema_match.get(key):
                attrib_split = schema_match.get(key).split(delimiter)
                attrib_table = attrib_split[0]
                attrib_field = attrib_split[1]
            else:
                attrib_table = key
                attrib_field = tbl
            attrib_value = value
            if attrib_table is None:
                attrib_table = get_parent_table(schema, path, table_list).name
            get_table(table_list, attrib_table).add({attrib_field: attrib_value.encode('utf-8')})

def parse_text(elem, tbl, schema_match, schema, path, table_list):
    # *********************************************************
    # Tag element text. Ex: <tag>tag element text
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
            if delimiter in schema_match.text:
                text_split = schema_match.text.split(delimiter)
                text_table = text_split[0]
                text_field = text_split[1]
            else:
                text_table = get_parent_table(schema, path, table_list)
                text_field = schema_match.text
            text_value = elem.text
            if text_table is None:
                text_table = get_parent_table(schema, path, table_list).name
            get_table(table_list, text_table).add({text_field: text_value.encode('utf-8')})


def parse_single(source, schema):
    # cnx = psycopg.connect(host='dbdev.cns.iu.edu', database='wos_test', user='wos_admin', password='57Ax34Fq')
    # cursor = cnx.cursor()
    # cursor.execute('SELECT file_number FROM admin.processing_record WHERE file_name = ' + source + ';')
    # file_number = cursor.fetchone()
    file_number = 1
    ordered_schema = order_schema(schema_file)
    with open("output/" + source.split("/")[-1].split(".")[0] + "-queries.txt", 'w') as output_file:
        context = etree.iterparse(source, events=('start', 'end',), remove_comments=True)
        path = []
        primary_key = None
        schema_match = None
        table_list = OrderedDict()
        open_tables = []
        open_counters = []
        counter_dict = OrderedDict()
        record_table = None
        i = 0
        print('Start time:           ' + strftime("%H:%M:%S", gmtime()))
        for event, elem in context:

            # *********************************************************
            # XML event catchers.
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
                    raise Exception(
                        'Cannot find a primary key. Make sure the id_tag value ["' + id_tag + '"] matches the primary key tag in the data.')


                    # *********************************************************
                    #   Record parser.
                    # *********************************************************
            if schema_match is not None:

                tbl = schema_match.get(table_tag)
                ctr = schema_match.get(counter_tag)
                curr_table = get_table(table_list, tbl)

                if tbl in open_tables:
                    curr_table.store()
                    if curr_table.counter_name is not '':
                        curr_table.add({curr_table.counter_name:1})
                if elem.tag != record_tag:
                    parse_attr(elem, tbl, schema_match, schema, path, table_list, event)
                    parse_text(elem, tbl, schema_match, schema, path, table_list)
                else:
                    record_table = tbl

                if ctr is not None:
                    ctr = ctr.split(delimiter)[1]
                    curr_table.counter_name = ctr
                    if event == "start":
                        open_tables_no_null_with_counters = [y for y in [x for x in open_tables if x is not None] if get_table(table_list, y).counter_name is not '']

                        if len(curr_table.parent_counters) > 0:
                            print(get_table(table_list, open_tables_no_null_with_counters[-2]).counter_value, curr_table.parent_counters)
                            if get_table(table_list, open_tables_no_null_with_counters[-2]).counter_value == curr_table.parent_counters[list(curr_table.parent_counters.keys())[-1]]:
                                curr_table.counter_value += 1
                            else:
                                curr_table.counter_value = 1
                        else:
                            curr_table.counter_value += 1
                    # if event == "end":
                        for otnnwc in open_tables_no_null_with_counters[:-1]:
                            open_table_not_null_with_counter = get_table(table_list, otnnwc)
                            curr_table.parent_counters[open_table_not_null_with_counter.counter_name] = open_table_not_null_with_counter.counter_value
                        for write in curr_table.parent_counters.items():
                            curr_table.add({write[0]:write[1]})
                        curr_table.add({curr_table.counter_name: curr_table.counter_value})

                if event == 'start' and schema_match.get("file_number") is not None:
                    curr_table.add({"file_number":file_number})

            if event == 'end' and elem.tag == record_tag:
                # print("Processing record:    " + str(i), "               \r",)
                i += 1
                to_write = []
                ordered_table_list = sort_statements(ordered_schema, table_list)
                for table in ordered_table_list:
                    curr_table = get_table(table_list, table)
                    curr_table.store()
                    curr_table.storage = curr_table.storage[::-1]
                    while len(curr_table.storage) > 0:
                        temp = curr_table.storage[-1]
                        to_write.append(temp.add({id_tag: (primary_key).encode('utf-8')}))
                        curr_table.storage.pop()
                    curr_table.storage = []
                curr_table.storage = []
                data_str = ""
                for x in to_write:
                    if x.sqlify(primary_key) is not None:
                        data_str += '\t\t\t\t\t' + x.sqlify(primary_key)
                output_file.write(
                    sql_template.replace('%pkey%', primary_key).replace('%data%', data_str).replace('%file_number%',
                                                                                                    str(file_number)))
                table_list.clear()
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
    print('End time:             ' + strftime("%H:%M:%S", gmtime()))
    return True


if (dir_path is not ""):
    print(listdir(dir_path))
    for f in listdir(dir_path):
        if isfile(join(dir_path, f)):
            if f.endswith('.xml'):
                parse_single(dir_path + "/" + f, etree.parse(schema_file))
else:
    parse_single(data_file, etree.parse(schema_file))

    # parse_single(data_file, etree.parse(schema_file))

    # cnx = psycopg2.connect(host='dbdev.cns.iu.edu', database='wos_test', user='wos_admin', password='57Ax34Fq')
    # cursor = cnx.cursor()
    # cursor.execute('SELECT file_number FROM admin.processing_record WHERE file_name = ' + data_file + ';')
    # data = cursor.fetch()
    # print cursor.fetchone()