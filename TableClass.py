from ordereddict import OrderedDict
from numbers import Number
# Only works for numbers and strings, not objects.
def is_number(s):
    # print('Checking if s is a number: ')
    # print(s)
    try:
        float(s)
        # print('Yes, it is')
        return True
    except ValueError:
        # print('No! not a number')
        return False


class Table():
    def __init__(self, **kwargs):
        self.id_tag         = kwargs.get('id_tag', '')
        self.table_quote    = kwargs.get('table_quote', '"')
        self.delimiter      = kwargs.get('delimiter', ':')
        self.name           = kwargs.get('name', '')
        self.fields         = kwargs.get('fields', [])
        self.values         = kwargs.get('values', [])
        self.storage        = []
        self.counter_name   = kwargs.get('counter_name', '')
        self.counter_value  = kwargs.get('counter_value', 0)
        self.child_counters = kwargs.get('child_counters', OrderedDict())
        self.parent_counters= kwargs.get('parent_counters', OrderedDict())
        self.xpath          = ''
        self.queued_counters= []
        self.val_as_string  = kwargs.get('val_as_string', True)

    def add(self, obj):
        for key, val in [(key, val) for key, val in obj.items() if key is not self.id_tag]:
            if not is_number(val):
                val = val.replace('//', '////')
            if key in self.fields:
                self.values[self.fields.index(key)] = val
                # pass
            else:
                self.fields.append(key)
                self.values.append(val)
        return self
    def queue_counter(self, obj):
        self.queued_counters.append(obj)
    def dequeue_counters(self):
        # from_first_to_last = self.queued_counters[0]
        # self.queued_counters.pop(0)
        # self.queued_counters.append(from_first_to_last)
        for x in self.queued_counters:
            self.add(x)
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
        # if self.name == 'ct_master':
        #     print('Storing: ' + self.name)
        #     # print('Fields: ' + ' | '.join(self.fields))
        #     print(self.fields)
        #     # print('Values: ' + ' | '.join(self.values))
        self.storage.append(Table(
            name=self.name,
            fields=self.fields,
            values=self.values,
            counter_name=self.counter_name,
            counter_value=self.counter_value,
            parent_counters=self.parent_counters,
            child_counters=self.child_counters,
            id_tag=self.id_tag,
            delimiter=self.delimiter,
            table_quote=self.table_quote
        ))
        return self.clear()
    def set_xpath(self, path):
        self.xpath = ('/'.join([x.tag for x in path[1:]]))
    def stringify(self, coll, quote_type):
        strin = ''
        for item in coll:
            temp_item = ""
            if item is not "" and item is not None:
                if is_number(item) and not self.val_as_string:
                    temp_item = str(item)
                else:
                    temp_item = quote_type + str(item).strip().replace("'","''") + quote_type
            strin += temp_item + ','
        strin = strin[:-1]
        return strin
    def sqlify(self, id):
        # if self.name == 'ct_master':
        #     print('SQLifying: ' + self.name)

        fieldstr = self.stringify(self.fields, self.table_quote)
        valuestr = self.stringify(self.values, "'")
        try:
            # if self.name == 'ct_master':
                # print('Fields: ' + fieldstr)
            assert len(self.fields) == len(self.values)
        except:
            # print(self.fields)
            # print(self.values)
            raise Exception('Length mismatch. Field(' + str(len(self.fields)) + ') !== value(' + str(len(self.values)) + ')')
        try:
            # assert self.id_tag not in self.fields #TODO: Replace this with a better duplicate removal method--don't just fail it
            assert len(self.fields) > 0
            if (self.delimiter in id):
                curr_id = id.split(self.delimiter)[1]
            else:
                curr_id = id

            temp_id = curr_id
            if is_number(curr_id) and not self.val_as_string:
                temp_id = str(curr_id)
            else:
                temp_id = "'" + str(curr_id).strip().replace("'","''") + "'"

            # useQuotes = "'"
            #     curr_id = str(int(curr_id))
            # if is_number(curr_id):
            #     useQuotes = ""

            return 'INSERT INTO ' + self.table_quote + self.name + self.table_quote + ' (' + self.table_quote + 'id' + self.table_quote + ',' + fieldstr + ') VALUES (' + temp_id + ',' + valuestr + ');\n'
        except (Exception):
            pass
