# Library of utilities for provisioning scripts
# 1) 'Printer' class to construct dict() while letting you print them in a specified format
# 2) 'MyPrettyPrinter' wrapper around 'PrettyPrinter' to dump Python objects
# 3) Misc functions like 'fatal'

import pprint
import simplejson as json
import sys

# Class to construct a dictionary
class BuildAndPrintDict():
    # TODO - could check format, but we do it earlier
    #      - may not work for:
    #        - arrays of arrays
    #        - arrays of values instead of arrays of dicts
    #        - top level array

    # List can show as:
    #    Teams:
    #      Id: 0
    #      Attribute: value
    #      ...
    #      Id: 1
    # OR
    #    Team: 0
    #      Attribute: value

    def __init__(self, printit=False):
        self.printit = printit
        self.indent_string = '  '
        self.current_indent = 0
        self.dict = dict()
        self.obj_stack = []
        self.current_obj = self.dict

    def comment(self, message):
        if self.printit:
            print(message)

    def get_dict(self):
        return self.dict

    def start_object(self, key):
        self.obj_stack.append(self.current_obj)
        self.current_obj[key] = dict()
        self.current_obj = self.current_obj[key]

        if self.printit:
            print('{}{}:'.format(self.indent_string * self.current_indent, key))
        self.current_indent += 1

    def end_object(self, key):
        self.current_obj = self.obj_stack.pop()
        self.current_indent -= 1
        if self.current_indent <= 0:
            #self.end()
            None

    def start_list(self, key):
        self.obj_stack.append(self.current_obj)     # adding the 
        self.current_obj[key] = []
        self.current_obj = self.current_obj[key]
        self.obj_stack.append(self.current_obj)     # adding also the array on the stack

        if self.printit:
            print('{}{}:'.format(self.indent_string * self.current_indent, key))
        self.current_indent += 1

    def end_list(self, key):
        self.obj_stack.pop()    # pop the list
        self.current_obj = self.obj_stack.pop()     # pop the object containing the list
        self.current_indent -= 1
        if self.current_indent <= 0:
            #self.end()
            None

    def new_list_obj(self):
        new_obj = dict()
        parent_list = self.obj_stack[len(self.obj_stack)-1]
        parent_list.append(new_obj)
        self.current_obj = new_obj

    def key_values(self, *keyvalueformat):
        if self.printit:
            indent = '{}'.format(self.indent_string * self.current_indent)
            sys.stdout.write(indent)
            for oneitem in keyvalueformat:
                if len(oneitem) >= 3:
                    formatstr = '{}: ' + oneitem[2] + ' '
                    print( formatstr.format(oneitem[0], oneitem[1]) ),
                else:
                    print( '{}: {}'.format(oneitem[0], oneitem[1]) ),
            print('')
        for oneitem in keyvalueformat:
            self.current_obj[oneitem[0]] = oneitem[1]

    # TODO - not used anymore, may want to remove
    def end(self):
        # we are done, let's print the structure
        print(json.dumps(self.dict, indent=2))
        self.dict = ()
        self.obj_stack = []


# Misc functions

def fatal(code, message):
    print("\nFATAL - {}".format(message))
    sys.exit(code)


# Imported code from Stack Overflow

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

