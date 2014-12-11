#!/usr/bin/env python
# import os
# import sys
# import re
# import resource
# import time
from lxml import etree
from optparse import OptionParser

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

(options, args) 	= parser.parse_args()
data_file 			= 'sample1.xml'
schema_file			= 'test.xml'
output_file_name	= 'out.txt'
parent_tag          = 'records'
record_tag			= 'REC'
delimiter			= ':'
id_tag				= 'UID'
table_tag			= 'table'
id_list				= []
reserved_keys		= [table_tag]
table_list			= dict()


# Based on http://stackoverflow.com/questions/9809469/python-sax-to-lxml-for-80gb-xml
class InfiniteXML (object):
	def __init__(self):
		self._root = True
	def read(self, len=None):
		if self._root:
			self._root=False
			return '<?xml version="1.0" encoding="US-ASCII"?>\n'
		else:
			# TODO: What should I do with this?
			return '''<record>\n\t<ancestor attribute='value'>text value</ancestor>\n</record>\n'''

class Table():
    def __init__(self, table_name, fields, values):
        self.table_name = table_name
        self.fields = fields
        self.values = values
    def add(self, obj):
        for key, val in obj.iteritems():
            # assert key not in self.fields
            self.fields.append(key)
            self.values.append(val)
        return self
    def sqlify(self, operation):
        fieldstr = ''
        valuestr = ''
        for field in self.fields:
            fieldstr += '"' + field + '",'
        for value in self.values:
            valuestr += '"' + value + '",'
        fieldstr = fieldstr[:-1]
        valuestr = valuestr[:-1]
        try:
            assert len(self.fields) == len(self.values)
        except:
            print self.fields
            print self.values
            raise Exception('Length mismatch. Field(' + str(len(self.fields)) + ') !== value(' + str(len(self.values)) + ')')
        if operation == 'insert':
            return 'INSERT INTO "' + self.table_name + '" (' + fieldstr + ') VALUES (' + valuestr + ');'
        elif operation == 'delete':
            return 'DELETE FROM "' + self.table_name + '" WHERE ("ID" = "PRIMARY_KEY_VALUE");'
        else:
            raise Exception('Invalid operation "' + operation + '". Valid options are "insert" and "delete"')
            
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
	with open(output_file_name, 'a') as output_file:
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
					schema_match = schema.find('/'.join([str(x.tag) for x in path[1:]])[len(parent_tag):])
					table_tag = schema_match.get(table_tag)
					if table_tag is not None:
						curr_table = find_table(table_tag)
				except:
					pass
			else:
				assert event == 'end'
                print path
				path.pop()
				if elem.tag == record_tag:
					assert primary_key is not None
					delete = False
					if primary_key in id_list:
						delete = True
						# output_file.write(find_table(x).add({id_tag:primary_key}).sqlify('delete') + '\n')
					to_write = []
					to_reverse_then_write = []
					for table in table_list:
						id_list.append(primary_key)
						curr_table = find_table(table)
						if delete:
							to_reverse_then_write.append(curr_table.sqlify('delete') + '\n')
						to_write.append(curr_table.add({id_tag:primary_key}).sqlify('insert') + '\n')
					for x in reversed(to_reverse_then_write):
						output_file.write(x)
					for x in to_write:
						output_file.write(x)
					table_list.clear()

			if schema_match is not None:
				attrib_table = None
				attrib_field = None
				attrib_value = None
				if elem.attrib.items():
					for key, value in elem.attrib.items():
						schema_attrib = schema_match.get(key)
						if delimiter in schema_attrib:
							attrib_split = schema_attrib.split(delimiter)
							assert len(attrib_split) == 2
							find_table(attrib_split[0]).add({attrib_split[1]: value})
							

						# # print '-------'
						# # print elem.attrib.items()
						# # print schema_match
						# if delimiter in schema_attrib:
						# 	attrib_split = schema_attrib.split(delimiter)
						# 	attrib_table = find_table(attrib_split[0])
						# 	attrib_field = attrib_split[1]
						# elif curr_table is not None:
						# 	attrib_table = curr_table
						# 	attrib_field = schema_attrib
						# else:
						# 	# raise Exception('Cannot insert into any table.')
						# 	pass
						# print attrib_field
						# print attrib_value
						# attrib_table.fields.append(attrib_field)
						# attrib_table.values.append(attrib_value)
				try:
					if elem.text.strip():
						if schema_match.text.strip():
							if delimiter in schema_match.text:
								attrib_split = schema_match.text.split(delimiter)
								attrib_table = find_table(attrib_split[0])
								attrib_field = attrib_split[1]
							elif curr_table is not None:
								attrib_table = curr_table
								attrib_field = schema_match.text
							else:
								# raise Exception('Cannot insert into any table.')
								pass
					attrib_value = elem.text
				except:
					pass
					
				try:
					attrib_table.fields.append(attrib_field)
					attrib_table.values.append(attrib_value)
				except:
					# print 'oops'
					pass
			# except SyntaxError as syntax:
			# 	# raise Exception('Data does not fit with schema')
			# 	pass
			elem.clear()
			# delete previous siblings
			while elem.getprevious() is not None:
				del elem.getparent()[0]
		output_file.write('EOF\n')
parse(InfiniteXML(), data_file, etree.parse(schema_file))



# TODO: Take this out. Just testing.
# print len(list(etree.ElementTree(file=data_file).iter()))

# # pass==asdfqwerty
# if __name__ == '__main__':
# 	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iai.settings')
# 	from django.core.management import execute_from_command_line
# 	execute_from_command_line(sys.argv)



				# if elem.tag == id_tag:
				# 	print elem.text
				# 	if elem.text in uid_list:
				# 		curr_table.fields.append(id_tag)
				# 		curr_table.values.append(elem.text)
				# 		output.append(curr_table.sqlify('delete'))
				# 	else:
				# 		uid_list.append(elem.text)
				# 		pass							
				# if elem.attrib.items():
				# 	for key, value in elem.attrib.items():
				# 		schema_value = schema_match.get(key)
				# 		if key not in reserved_keys:
				# 			if delimiter in schema_value:
				# 				splitstr = schema_value.split(delimiter)
				# 				# print value.split(delimiter)[0]
				# 				curr_curr_model = find_table(splitstr[0])
				# 				curr_curr_model.fields.append(splitstr[1])
				# 				curr_curr_model.values.append(value)
				# 				output.append(curr_curr_model.sqlify('insert'))
				# 			else:
				# 				if table_attr in elem.attrib.items():
				# 					curr_table = find_table(table_attr)
				# 				else:
				# 					pass
				# 				# TODO: Use existing model
				# if elem.text:
				# 	if delimiter in elem.text:
				# 			splitstr = schema_match.text.split(delimiter)
				# 			# print value.split(delimiter)[0]
				# 			curr_curr_model = find_table(splitstr[0])
				# 			curr_curr_model.fields.append(splitstr[1])
				# 			curr_curr_model.values.append(value)
				# 			# TODO: Do something processy here
				# 			output.append(curr_curr_model.sqlify('insert'))
				# 		# TODO: do something processy here
				# 	else:
				# 		pass
				# 		# TODO: Try to use tag's table. Otherwise, use the current tables


			# output = []
			# curr_table = None
			# schema_match = None
			# try:
			# 	schema_match = schema.find('/'.join([str(x.tag) for x in path[1:]])[len(record_tag) + 1:])
			# 	assert schema_match is not None
			# 	print schema_match
			# 	table_attr = str(schema_match.get('table'))
			# 	# add/remove from/to list to build path
			# 	if event == 'start':
			# 		path.append(elem)
			# 		# OR path.append(elem.tag)
			# 		if table_attr is not None:
			# 			curr_table = find_table(table_attr)
			# 		else:
			# 			pass
			# 	else:
			# 		assert event == 'end'
			# 		path.pop()
			# 		if elem.tag == record_tag:
			# 			for x in output:
			# 				output_file.write(x + '\n')
			# except:
			# 	pass
			
			# # match the data to the schema
			# try:
			# 	#TODO: Iterate over parents to find nearest table
			# 	if elem.attrib.items():
			# 		for key, value in elem.attrib.items():
			# 			schema_value = None
			# 			if schema_match is not None:
			# 				schema_value = schema_match.get(key)
			# 				if key not in reserved_keys:
			# 					if delimiter in schema_value:
			# 						splitstr = schema_value.split(delimiter)
			# 						curr_table = find_table(splitstr[0])
			# 						curr_table.fields.append(splitstr[1])
			# 						curr_table.values.append(value)
			# 		output.append(curr_table)
