from optparse import OptionParser

def config()    :
    parser = OptionParser()
    parser.add_option(
            '-d', '--data_file',
            action='store', type='string', dest='data_file',
            help='file name and path of the XML file to be processed. Default: \'test1.xml\'')
    parser.add_option(
            '-o', '--output_folder',
            action='store', type='string', dest='output_folder',
            help='output folder for files. Default: \'./output\'')
    parser.add_option(
            '-i', '--unique_identifier',
            action='store', type='string', dest='unique_identifier',
            help='I dont know how to word this. Default: \'UID\'')
    parser.add_option(
            '-m', '--master_table',
            action='store', type='string', dest='master_table',
            help='the name of the master table. When checking for a duplicate record, what table should we delete from to trigger the cascade delete. Default: \'wos:master\'')
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
            help='file name and path of the XML schema file. Default: \'wos_config.xml\'')
    parser.add_option(
            '-t', '--template_file',
            action='store', type='string', dest='template_file',
            help='file name and path of the SQL template file. Default: \'sql_template.sql\'')
    parser.add_option(
            '-v', '--verbose',
            action='store', type='string', dest='verbose',
            help='boolean to determine whether exceptions should be displayed. Default: True')
    parser.add_option(
            '-a', '--dir_path',
            action='store', type='string', dest='dir_path',
            help='absolute directory path for a list of files to parse. Default: \'\'')
    parser.add_option(
            '-q', '--table_quote',
            action='store', type='string', dest='table_quote',
            help='character to wrap table names with. Default: \'"\' (double quote character)')
    parser.add_option(
            '-l', '--val_as_string',
            action='store', type='string', dest='val_as_string',
            help='treat all values as strings. Default: False')


    return parser
