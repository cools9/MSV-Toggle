import re
import csv,json,requests,pickle
import tkinter as tk


class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {
            'intiger': int(),
            'float_value': float(),
            'csv': csv,
            'json': json,
            'requests': requests,
            'pickle': pickle,
            're': re,
            'tk': tk,
            'match_case': zip,
            'input': input,
            'list': list,
            'split': str.split,
            'range': range,
            'tuple': tuple,
            'maximum_val': max,
            'minimum_val':min,
            'type':type,
            'read_file': self.read_file,
            'write_file': self.write_file,
            'append_file': self.append_file,
            'close_file': self.close_file
        }

    def import_package(self, package_name, package_functions):
        package = __import__(package_name)
        package_functions = package_functions.split(',')
        package_dict = {f: getattr(package, f) for f in package_functions}
        self.functions.update(package_dict)

    
    def open_file(self, filename, mode='r'):
        self.files[filename] = open(filename, mode)
        return filename

    def read_file(self, filename):
        with open(filename, 'r') as file:
            contents = file.read()
            print(contents)

    def write_file(self, filename, text):
        self.files[filename].write(text)

    def append_file(self, filename, text):
        self.files[filename].write(text)

    def close_file(self, filename):
        self.files[filename].close()
        del self.files[filename]
    
    def eval_expression(self, expr):
        if expr.isnumeric():
            return int(expr)
        elif expr in self.vars:
            return self.vars[expr]
        elif re.match(r'^\[.*\]$', expr):
            # List literal
            return eval(expr)
        elif re.match(r'^\{.*\}$', expr):
            # Dictionary literal
            return eval(expr)
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\(.*\)$', expr):
            # Function call
            func_name, args = expr.split('(', 1)
            args = args[:-1]  # remove the closing parenthesis
            args = self.eval_expression(args)
            if func_name in self.functions:
                return self.functions[func_name](*args)
            else:
                raise NameError(f"Undefined function: {func_name}")
        else:
            raise NameError(f"Invalid expression: {expr}")
    
    def execute(self, code):
        code = re.sub(r'#.*', '', code)
        for line in code.splitlines():
            line = line.strip()
            if not line:
                continue  # skip empty lines
            if line.startswith('import_package '):
                package_name, package_functions = line.split()[1:]
                self.import_package(package_name, package_functions)

            elif line.startswith('print '):
                expr = line[6:]
                print(self.eval_expression(expr))
            elif line.startswith('print('):
                print(self.eval_expression(line[6:-1]))
            elif '=' in line:
                var, expr = line.split('=', 1)
                self.vars[var] = self.eval_expression(expr)
            elif line.startswith('def '):
                func_name, func_code = line[4:].split(':', 1)
                func_code = func_code.strip()
                self.functions[func_name] = lambda *args: self.execute(func_code)
            elif line.startswith('if '):
                condition, then_code = line[3:].split(':', 1)
                then_code = then_code.strip()
                if self.eval_expression(condition):
                    self.execute(then_code)
            elif line.startswith('else:'):
                else_code = line[5:].strip()
                self.execute(else_code)
            elif line.startswith('for '):
                var, iterable = line[4:].split(' in ')
                for val in self.eval_expression(iterable):
                    self.vars[var] = val
                    self.execute(line[line.index(':')+1:])
            elif line.startswith('while '):
                condition, while_code = line[6:].split(':', 1)
                while_code = while_code.strip()
                while self.eval_expression(condition):
                    self.execute(while_code)
            elif line.startswith('run_py('):
                code_to_run = line[7:-1]
                exec(code_to_run, self.functions)
            elif line.startswith('py_file_info'):
                file_info=line[13:]
                with open(file_info,'r') as file_name:
                    contents=file_name.read()
                    argument,file_to_r=contents.split(':')
                    with open(file_to_r,'r') as file_to_read:
                        py_file_contents=file_to_read.read()
                        exec(py_file_contents, self.functions)
                        
            elif line.startswith('read_file '):
                filename = line.split()[1]
                print(self.read_file(filename))
            elif line.startswith('write_file '):
                filename, text = line.split()[1:]
                self.write_file(filename, text)
            elif line.startswith('append_file '):
                filename, text = line.split()[1:]
                self.append_file(filename, text)
            elif line.startswith('close_file '):
                filename = line.split()[1]
                self.close_file(filename)
            elif line.startswith('open_file '):
                filename, mode = line.split()[1:]
                self.open_file(filename, mode)

interpreter=Interpreter()
interpreter.execute("""
import_package Names_manager using pos,exit
Names_manager.pos("Hello,World!")
""")
