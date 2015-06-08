SDB-Generic-Parser
==================
### Description
This is a generic parser for SDB. This parser will load a schema XML into memory and reference it as a data file is fed into an iterative parser. For each record, the parser will map the data XPath to the schema and build SQL statements accordingly. 

### Requirements
The following Python packages are required:

lxml - Quick XML parser based on the C libraries libxml2 and libxslt
OptionParser - Flexible library for parsing command-line options
psycopg2 - database connector for postgresql. Warning: also needs Visual Studio installed and configured in the path

Additionally, two XML files are needed. One is the data file to be processed, and another should be an appropriate schema to pair the data with. For sample data files and official (current) SDB schemas, see [here](http://wiki.cns.iu.edu/display/DEV/SDB+Generic+Parser)

### Usage
Run parser.py from the command line.

Soon we will support command line arguments to prevent the need to modify a script. The required arguments are:

| Short Option        | Longer Option               | Description  |
| :-------------: |:-------------:| :----- |
| -d | --datafile | file name and path of the XML file to be processed. ex: data_file_name.xml |
| -s | --schemafile | file name and path of the XML schema file. ex: data_file_name.xml |
| -o | --outputfile | desired file name and path of the resulting SQL operations |
| -p | --parenttag | root tag of the data file |
| -r | --recordtag | identifying tag for the records |
| -i | --idtag | primary identifier across tables |
| -a | --dir_path | path of data files. if set, the parser will run for each xml found |
  
### Credits
TODO: Put something here

### License
TODO: Put something here too
