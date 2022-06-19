from dataclasses import replace
import subprocess
from copyreg import constructor
import os
import sys
import os.path
from os import path
import re
from json import JSONEncoder
from termios import CREAD
from webbrowser import get

from ldap3 import BASE

def print_error(file, error_type, error_tuple, rule):
    pattern = "  {color}[{error_type}] ({error_name}){endcolor} - {message}\033[90m{fileinfo}\033[0m"
    pattern2 = "  [{error_type}] ({error_name}) - {message}{fileinfo}"
    colors = {"minor": "\033[1;93m",
        "major": "\033[1;91m",
        "info": "\033[36;1m"}

    fileinfo = ""
    if file and len(file) > 0 or error_tuple[2] and len(str(error_tuple[2])) > 0  :
        fileinfo = " ("
        if file and len(file) > 0:
            fileinfo += file
        if error_tuple[2] and len(str(error_tuple[2])) > 0:
            if file and len(file) > 0:
                fileinfo += ":"
            fileinfo += str(error_tuple[2])
        fileinfo += ")"

    color = colors[error_type] if error_type in colors else ""
    if (rule == False): print("\033[0m" + pattern.format(color=color, error_type=error_type.upper(), error_name=error_tuple[0], message=error_tuple[1], fileinfo=fileinfo, endcolor = "\033[0m"))
    else:
        buffer = open("trace.md", "a")
        buffer.write(pattern2.format(error_type=error_type.upper(), error_name=error_tuple[0], message=error_tuple[1], fileinfo=fileinfo) + "\n")
        buffer.close()

BASEPATH = "./"

class Pointers:
    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        buffer = open(files, "r", encoding="utf8", errors='ignore')
        line = 0
        for lines in buffer:
            line += 1
            if any([(types + '*' in lines) for types in Norm_obj.var_types]):
                Norm_obj.minor.append(('V3', 'The pointer symbol should be attached to the assosiated variable', line))
        buffer.close()
        

class NamingIdentifiers:
    def __init__(self):
        self.active = True
        self.checked = True
        self.t_checked = False

    def run(self, Norm_obj, files):
        if files.endswith(".h"):
            inside = open(files, "r", encoding="utf8", errors='ignore')
            begin = 0
            line = 0
            for lines in inside:
                line += 1
                if "typedef" in lines and not (";" in lines):
                    begin = 1
                elif "typedef" in lines and ";" in lines and lines.replace(";", "").replace("\n", "").split(" ")[-1].endswith("_t") == False:
                    Norm_obj.major.append(("V1", "Typedef name should end with '_t'", line))
                tot=lines.replace(" ", "")
                if begin == 1 and tot[0] == '}':
                    i = 0
                    tot=lines.replace(" ", "").replace("}", "").replace(";\n", "").replace("\n", "")
                    if len(tot) > 0 and not(tot.endswith("_t")) and (self.t_checked == True or Norm_obj.all_rule == True):
                        Norm_obj.major.append(("V1", "Typedef name should end with '_t'", line))
                tab = [i for i, x in enumerate(lines.split(" ")) if (x == "#define")]
                if (tab != []):
                    id = tab[0] + 1
                    if "#define" in lines and id < len(lines.split(" ")) and not(lines.split(" ")[id].split("(")[0].isupper()):
                        Norm_obj.major.append(("V1", "Macros should be in Uppercases", line))
            inside.close()
            buffer = open(files, "r", encoding="utf8", errors='ignore')
            inside = "".join(buffer.read().replace(" ", "").replace("\n", "[END]"))
            get_splited = re.split("enum+.+{+.+}", inside)
            if get_splited[0] == inside:
                return
            get_enums = re.findall("enum+.+{+.+}", inside)
            id = 0
            line = 1
            for enums in get_enums:
                line += get_splited[id].count("[END]")
                for macro in enums.replace("enum", "").split("{")[1].split("}")[0].split(","):
                    if any([i.islower() for i in macro.split("=")[0]]):
                        Norm_obj.major.append(("V1", "Macros should be in Uppercases", line + macro.split([i for i in macro.split("[END]") if len(i) > 0][0])[0].count("[END]")))
                    line += macro.count("[END]")
                id += 1

class VariableDeclaration:
    def __init__(self):
        self.active = True
        self.checked = False

    def run(self, Norm_obj, files):
        buffer = open(files, "r", encoding="utf8", errors='ignore')
        inside = buffer.read().split("\n")
        line = 0
        in_function = False
        in_declaration = False
        prev_line = "" 
        for lines in inside:
            line += 1
            if (lines.replace(" ", "").replace("\t", "").replace("\n", "") == "{" and lines[0] == '{'):
                in_function = True
                in_declaration = True
            if (lines.replace(" ", "").replace("\t", "").replace("\n", "") == "}" and lines[0] == '}'):
                in_function = False
            if len(lines.replace("\t", "").replace(" ", "")) == 0 and in_declaration == False and in_function == True:
                Norm_obj.minor.append(('L6', "There shouldn't be a line break mid function", line))
            if in_function == True:
                if in_declaration == True:
                    new_line = lines.replace("*", "").replace(" ", "").replace("\n", "")
                    if not(any(("(" + types + " " in lines or " " + types + " " in lines) and (new_line.count("(" + types) + lines.count(" " + types + " ") - new_line.count("(" + types + ")") > 0) for types in Norm_obj.var_types)) and not(lines.replace(" ", "").replace("\t", "").replace("\n", "") == "{" and lines[0] == '{') or "for" in lines:
                        in_declaration = False
                        if len(lines.replace("\t", "").replace(" ", "")) != 0 and prev_line.replace(" ", "") != "{":
                            Norm_obj.minor.append(('L6', "There should be a lign break between declarations and code", line))
                    else:
                        if ("," in lines and not("(" in lines or ")" in lines or "{" in lines)):
                            Norm_obj.minor.append(('L5', "Only one variable should be declared per line", line))
                else:
                    new_line = lines.replace("*", "").replace(" ", "").replace("\n", "")
                    if any(("(" + types + " " in lines or " " + types + " " in lines) and (new_line.count("(" + types) + lines.count(" " + types + " ") - new_line.count("(" + types + ")") > 0) for types in Norm_obj.var_types) and not(lines.replace(" ", "").replace("\t", "").replace("\n", "") == "{" and lines[0] == '{'):
                        Norm_obj.minor.append(('L5', "Variable Declaration should be in the head of the function", line))
            prev_line = lines


class CodeLineContent:
    def __init__(self):
        self.multiple_declaration = True
        self.one_line_conditions = True
        self.multiple_ligns_at_once = True
        self.assignement_in_condition = True
        self.checked = False

    def run(self, Norm_obj, files):
        inside = open(files, "r", encoding="utf8", errors='ignore')
        line = 0
        for lines in inside:
            line += 1
            if ("if (" in lines or "if(" in lines or "else" in lines) and ";" in lines and self.one_line_conditions:
                Norm_obj.minor.append(('L1', "There shouldn't be a condition and it's statement on the same line", line))
            if lines.count(";") > 1 and "for" not in lines and self.multiple_ligns_at_once:
                Norm_obj.minor.append(('L1', "There shouldn't be more than one operation per line (except for 'for' loops)", line))
            if lines.count(" = ") > 1 and not("for (" in lines or "for(" in lines or ");" in lines) and self.multiple_declaration:
                Norm_obj.minor.append(('L1', "There shoudn't be more than one assignement per line", line))
            if " = " in lines and "if" in lines and self.assignement_in_condition:
                Norm_obj.minor.append(('L1', "There shoudn't be an assignement in conditions", line))
        inside.close()

class TraillingLine:
    def __init__(self):
        self.active = True
        self.checked = True
    
    def run(self, Norm_obj, files):
        inside = open(files, "r", encoding="utf8", errors='ignore')
        line = 0
        rest = ""
        for lines in inside:
            line+=1
            rest += lines
        splitted = rest.split("\n")
        if (len(splitted) > 2):
            if splitted[-2] == "" and splitted[-1] == "":
                Norm_obj.minor.append(('G9', "Trailling Line", line))
        inside.close()

class Comment_Check:
    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        inside = open(files, "r", encoding="utf8", errors='ignore')
        line = 0
        in_it = 0
        for lines in inside:
            line += 1
            if lines[0] == '{':
                in_it = 1
            if lines[0] == '}':
                in_it = 0
            if ("//" in lines or "/*" in lines or "*/" in lines) and in_it == 1:
                Norm_obj.minor.append(('F6', "There shoudn't be comments inside a function.", line))
        inside.close()

class Check_Goto:
    def __init__(self):
        self.auth = True
        self.checked = True

    def run(self, Norm_obj, files):
        inside = open(files, "r", encoding="utf8", errors='ignore')
        line = 0
        two = 0
        for lines in inside:
            line += 1
            if " goto " in lines and self.auth == True:
                Norm_obj.major.append(('C3', "Cringe t'as un goto fdf.", line))
        inside.close()

class Line_Break:
    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, file_name):
        if self.active == True:
            inside = open(file_name, "r", encoding="utf8", errors='ignore')
            rest = ""
            for lines in inside:
                rest = lines
                if not("\n" in lines):
                    Norm_obj.info.append(('A3', "Line break missing at end of file.", ""))
            inside.close()

class Check_include:
    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r", encoding="utf8", errors='ignore')
            line = 0
            in_it = 0
            for lines in inside:
                line += 1
                if "#include" in lines:
                    if ('"' in lines):
                        tab = lines.split('"')
                        if tab[1][-1] != 'h' or tab[1][-2] != '.':
                            Norm_obj.major.append(('G6', "#include should only contain .h files." , line))
                    else:
                        tot = ""
                        for char in lines:
                            if char == '>':
                                in_it = 0
                            if in_it == 1:
                                tot += str(char)
                            if char == '<':
                                in_it = 1
                        if len(tot) > 3 and (tot[-1] != 'h' or tot[-2] != '.'):
                            Norm_obj.major.append(('G6', "#include should only contain .h files.", line))
            inside.close()

class Misplaced_spaces:
    def __init__(self):
        self.active = True
        self.checked = True

    def tabs_to_space(self, string):
        begin = 0
        len_str = len(string)
        if len_str == 0:
            return (string)
        while string[begin] == ' ':
            begin += 1
        if begin == len_str - 1:
            return (string)
        string = string[begin:]
        while re.search(r'(\s\s)+(?=([^"]*"[^"]*")*[^"]*$)', string):
            string = re.sub(r'(\s\s)+(?=([^"]*"[^"]*")*[^"]*$)', ' ', string)
        return (' ' * begin + string)

    def fix_clang(self, string):
        return string.replace(" ;", ";")

    def run(self, Norm_obj, files):
        if files.endswith(".c") and self.active == True:
            files = [files]
            for f in files:
                break_pos = []
                file_opened = open("./"+f, 'r')
                lines = file_opened.read()
                absolute_lines = lines.replace(' ', '').replace('\\\n', '\n')
                for i in range(len(absolute_lines)):
                    if absolute_lines[i] == '\n':
                        break_pos.append(i)
                fmt = os.popen("clang-format "+f).read().replace('\n', '')
                pos = 0
                i = 0
                while i < len(fmt):
                    if fmt[i] != ' ':
                        pos += 1
                        if (pos in break_pos):
                            fmt = fmt[:i + 1] + '\n' + fmt[i + 1:]
                    i += 1
                fmt = str(fmt).splitlines()
                lines = lines.splitlines()
                for i in range(min(len(lines), len(fmt))):
                    clean_fmt = self.fix_clang(self.tabs_to_space(fmt[i])).strip()
                    clean_line = lines[i].rstrip('\\').strip()
                    if clean_fmt != clean_line and clean_fmt.replace(' ', '') == clean_line.replace(' ', '') and clean_line[0:2] != "**" and not('//' in clean_line) and not("#define" in clean_line.replace(" ", "") or "#include" in clean_line.replace(" ", "")):
                        Norm_obj.minor.append(('L3', "Misplaced spaces.", (i + 1)))
                file_opened.close()

class Too_many_functions:
    def __init__(self):
        self.max_function_nbr = 5
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if (files[-1] == 'c' and files[-2] == '.') and self.active == True:
            inside = open(files, "r", encoding="utf8", errors='ignore')
            function_nbr = 0
            for lines in inside:
                if (lines.replace(" ", "").replace("\t", "").replace("\n", "") == "{" and lines[0] == '{'):
                    function_nbr += 1
            if (function_nbr > self.max_function_nbr):
                Norm_obj.major.append(('O3', "Too many functions in one file (%d > 5)." % function_nbr, ""))
            inside.close()

class Include_guard:
    def __init__(self):
        self.check_ifndef = 0
        self.check_endif = 0
        self.check_define = 0
        self.pragma = 0
        self.checked = True

    def run(self, Norm_obj, files):
        if (files[-1] == 'h' and files[-2] == '.'):
            buffer = open(files, "r", encoding="utf8", errors='ignore')
            for lines in buffer:
                if "#ifndef" in lines:
                    self.check_ifndef = 1
                if "#define" in lines:
                    self.check_define = 1
                if "#endif" in lines:
                    self.check_endif = 1
                if "#pragma" in lines:
                    self.pragma = 1
            buffer.close()
            if (self.check_ifndef == 0 or self.check_endif == 0 or self.check_define == 0) and self.pragma == 0:
                Norm_obj.minor.append(('H2', "Header not protected from double inclusion.", ""))


class Too_many_depth:
    def __init__(self):
        self.max_depth = 3
        self.indentation_space_nbr = 4
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if self.active == True:
            tot = 1
            spaces_lvl = 4
            depth = 1
            op_list = [ "for (", "for(", "if (", "if(", "while (", "while(", "do(", "do (" ]
            inside = open(files, "r", encoding="utf8", errors='ignore')
            line = 0
            for lines in inside:
                line += 1
                in_it = 0
                i = 0
                while (lines[i] == ' '): i+=1
                for val in op_list:
                    if val in lines:
                        in_it = 1
                        break;
                if in_it == 1:
                    if i > spaces_lvl:
                        depth += 1
                        spaces_lvl = i
                    elif i < spaces_lvl:
                        depth = i // self.indentation_space_nbr
                        spaces_lvl = i
                    elif i == spaces_lvl and not("else if" in lines):
                        depth = i // self.indentation_space_nbr
                        spaces_lvl = i
                    if "else if" in lines:
                        depth += 1
                if depth >= self.max_depth and in_it == 1:
                    Norm_obj.minor.append(('C1', "Conditionnal branching.", line))
            inside.close()

class Arguments_nbr:
    def __init__(self):
        self.max_arguments_nbr = 4
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if self.active == True and files.endswith(".c"):
            inside = open(files, "r", encoding="utf8", errors='ignore')
            line = 0
            counter = 0
            last_char = 'p'
            for lines in inside:
                line += 1
                for char in lines:
                    if (char == '(' and lines[0] != ' '):
                        counter = 1
                    if (counter > 0 and char == ','):
                        counter += 1
                    if (char == ')' and lines[0] != ' '):
                        if (counter > self.max_arguments_nbr):
                            Norm_obj.major.append(('F5', "Function should not need more than %d arguments (%d > %d)." % (self.max_arguments_nbr, counter, self.max_arguments_nbr), line))
                        if last_char == '(':
                            Norm_obj.major.append(('F5', "Argumentless functions should take void as parameter.", line))
                        counter = 0
                    last_char = char
            inside.close()

class Function_length:
    def __init__(self):
        self.max_length = 20
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r", encoding="utf8", errors='ignore')
            counter = 0
            begin_line = 0
            line = 0
            if (".c" in files):
                for lines in inside:
                    line += 1
                    if (lines[0] == '{'):
                        counter = 1
                        begin_line = line
                    if (counter > 0):
                        counter += 1
                    if (lines[0] == '}'):
                        if (counter - 3 > self.max_length):
                            Norm_obj.major.append(('F4', "A function should not exceed %d lines (%d > %d)." % (self.max_length, (counter - 3), self.max_length), begin_line))
                        counter = 0
            inside.close()

class Curly_brackets:
    def __init__(self):
        self.active = True
        self.checked = True

    def check_c_files(self, Norm_obj, files):
        inside = open(files, "r", encoding="utf8", errors='ignore')
        line = 0
        prev_line = "02"
        for lines in inside:
            line += 1
            if (lines[0] != ' ' and lines[0] != '\n' and "(" in lines and ")" in lines and "{" in lines):
                Norm_obj.minor.append(('L4', "Curly brackets misplaced.", line))
            if (lines[0] == ' ' and "{" in lines and not("if" in lines) and not("else" in lines) and not("for" in lines) and not("while" in lines) and not(")" in lines) and not("}" in lines)) and not("do" in lines) and ("if" in prev_line or "else" in prev_line or "for" in prev_line or "while" in prev_line or ")" in prev_line or "}" in prev_line or "do" in prev_line):
                Norm_obj.minor.append(('L4', "Curly brackets misplaced.", line))
            if (prev_line[0] == ' ' and "}" in prev_line and not("if" in prev_line) and not("else" in prev_line) and not("for" in prev_line) and not("while" in prev_line) and "else" in lines and not("}" in lines)):
                Norm_obj.minor.append(('L4', "Curly brackets misplaced.", line))
            prev_line = lines
        inside.close()

    def check_h_files(self, Norm_obj, files):
        inside = open(files, "r", encoding="utf8", errors='ignore')
        line = 0
        prev_line = "02"
        for lines in inside:
            line += 1
            if lines[0] == '{' and lines.replace("\n", "").replace(" ", "").replace("\t", "") == "{" and "struct" in prev_line:
                Norm_obj.minor.append(('L4', "Curly brackets misplaced.", line))
            prev_line = lines
        inside.close()

    def run(self, Norm_obj, files):
        if self.active == True:
            if ".c" in files:
                self.check_c_files(Norm_obj, files)
            if ".h" in files:
                self.check_h_files(Norm_obj, files)

class Identation_error:
    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r", encoding="utf8", errors='ignore')
            test = 0
            for lines in inside:
                nbr = 0
                test += 1
                i = 0
                while lines[i] == ' ':
                    i+=1
                if i % 4 != 0:
                    Norm_obj.minor.append(('L2', "No tab should be replaced by an indentation.", test))
                for char in lines:
                    if (char == '\t' and ("Makefile" in files) != True):
                        Norm_obj.minor.append(('L2', "No tab should be replaced by an indentation.", test))
            inside.close()

class Trailling_spaces:
    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r", encoding="utf8", errors='ignore')
            line = 0
            for lines in inside:
                line += 1
                if len(lines) >= 2:
                    if lines[-1] == '\n' and lines[-2] == ' ':
                        Norm_obj.minor.append(('G8', "Trailling space.", line))
            inside.close()

class Line_Endings:
    def __init__(self):
        self.forbidden_endings = [
            b'\r\n',
            b'\n\r',
            b'\r',
        ]
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if ".c" in files or ".h" in files and self.active == True:
            counts = dict.fromkeys(self.forbidden_endings, 0)
            line_nbr = 0
            with open(files, 'rb') as fp:
                for line in fp:
                    line_nbr += 1
                    for x in self.forbidden_endings:
                        if line.endswith(x):
                            Norm_obj.minor.append(('G7', "Line should end with \\n", line_nbr))

class Global_variable:

    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if ".c" in files and self.active == True:
            inside = open(files, "r", encoding="utf8", errors='ignore')
            line = 0
            for lines in inside:
                ids = []
                for i,x in enumerate(lines):
                    if '"' == x:
                        ids.append(i)
                line += 1
                for types in Norm_obj.var_types:
                    out = [i for i,x in enumerate(ids) if types in lines and lines.index(types) < x]
                    if lines.replace("const", "").replace(" ", "").startswith(types) and (out if len(out) > 0 else [0])[0]%2==0 and ((not("const" in lines) and Norm_obj.all_rule == True) or (not("static" in lines) and not("const" in lines) and Norm_obj.all_rule == False)) and not("(" in lines) and lines[0] != ' ' and lines[0] != '\t' and not(")" in lines) and not(lines[0:2] == "**"):
                        Norm_obj.minor.append(('G4', "Global variable should be const.", line))
                        break
            inside.close()

class Preprocessor_Directives:
    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        start=0
        line = 0
        inside = open(files, "r", encoding="utf8", errors='ignore')
        if (".h" in files and files[-1] == 'h') and self.active == True:
            for lines in inside:
                line += 1
                if "#ifndef" in lines or "#pragma" in lines:
                    start=1
                if "#endif" in lines:
                    start = 0
                if "#endif" in lines or "#ifndef" in lines:
                    if lines[0] != '#':
                        Norm_obj.minor.append(('G3', "Preprocessor directives should be indented", line))
                if ("#define" in lines or "#include" in lines) and start == 1:
                    i = 0
                    while (lines[i] == ' '):
                        i += 1
                    if (i != 4):
                        Norm_obj.minor.append(('G3', "Preprocessor directives should be indented", line))
        inside.close()

class Empty_line:
    def __init__(self):
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        inside = open(files, "r", encoding="utf8", errors='ignore')
        trailling_lines = 0
        line_nbr = 0
        if (".c" in files or "Makefile" in files) and self.active == True:
            for lines in inside:
                line_nbr += 1
                if (lines == "\n"):
                    trailling_lines += 1
                else:
                    trailling_lines = 0
                if (trailling_lines == 2):
                    trailling_lines = 0
                    Norm_obj.minor.append(('G2', "There should be only one empty_line each time.", line_nbr))
        inside.close()
        inside = open(files, "r", encoding="utf8", errors='ignore')
        prev_line = "\n"
        line = 0
        if (".c" in files) and self.active == True:
            for lines in inside:
                line += 1
                if prev_line.replace("\n", "").replace(" ", "").replace("\t", "") == "}" and prev_line[0] == '}' and lines[0] != '\n':
                    Norm_obj.minor.append(('G2', "There should be only one empty_line each time.", line))
                prev_line = lines
        inside.close()

class Check_file_header:

    def __init__(self):
        self.c_file_header = "/*\n** EPITECH PROJECT,\n** File description:\n*/\n"
        self.h_file_header = "##\n## EPITECH PROJECT,\n## File description:\n##\n"
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r", encoding="utf8", errors='ignore')
            line_nbr = 0
            result = ""
            mid_res = ""
            for line in inside:
                if (line_nbr > 5):
                    break
                if (line_nbr != 2 and line_nbr != 4):
                    if (line_nbr == 1):
                        for char in line:
                            mid_res += char
                            if (char == ','):
                                break
                        mid_res += "\n"
                        result += mid_res
                    else:
                        result += line
                line_nbr += 1
            if (".c" in files or ".h" in files):
                if (result != self.c_file_header):
                    Norm_obj.major.append(('G1', "File header not correct.", ""))
            if ("Makefile" in files):
                if (result != self.h_file_header):
                    Norm_obj.major.append(('G1', "File header not correct.", ""))
            inside.close()

class Check_Include:

    def __init__(self):
        self.authorised_files = [ ".h" ]
        self.active = True
        self.checked = True

    def run(self, files, rule):
        if self.active == True:
            tot = []
            for dos in os.listdir(files):
                if ((".h" in dos) != True):
                    tot.append(('G6', "Include folder should only contain .h files.", dos.replace("./", "")))
            if len(tot) > 0:
                er = 1
                print("\033[1m‣ In Include\n")
                for i in tot:
                    print_error("", "major", i, rule)
                print("")

class Check_file:
    def __init__(self):
        self.forbidden_files = [ ".o", ".gch", ".a", ".so", "~", "#", ".d" ]
        self.active = True
        self.checked = True

    def check_04(self, file_name, paths, Norm_obj):
        if any(ele.isupper() for ele in str(file_name)) == True and (path.isdir(paths) or file_name.endswith(".c") or file_name.endswith(".h") or Norm_obj.all_rule == True ) and self.active == True and file_name != "Makefile":
            Norm_obj.bad_files.append(('O4', "Name not in snake case convention.", paths.replace("./", "")))

    def check_01(self, file_name, files, Norm_obj):
        for ext in self.forbidden_files:
            if (ext in file_name and ext[-1] == file_name[-1]):
                Norm_obj.bad_files.append(('O1', "Delivery Folder should not contain %s files." % ext, files.replace("./", "")))
    def run(self, file_name, path, Norm_obj):
        if self.active == True:
            self.check_04(file_name, path, Norm_obj)
            self.check_01(file_name, path, Norm_obj)

class Too_Long_Line:
    def __init__(self):
        self.line_length = 80
        self.attributes = {"line_length" : self.line_length}
        self.active = True
        self.checked = True

    def run(self, Norm_obj, files):
        if self.active == True:
            inside = open(files, "r", encoding="utf8", errors='ignore')
            line = 0
            for lines in inside:
               line += 1
               if len(lines) > self.line_length:
                   Norm_obj.major.append(('F3', "The length of a line should not exceed 80 columns. (%d > %d)" % (len(lines), self.line_length), str(line)))
            inside.close()

class Norms:
    ### Norms class: Central hub of the error handling
    def __init__(self, rule, json_rule, all_rule):

        # A list of checked errors

        self.norm_list = {"Too long line" : Too_Long_Line(),
                          "Check file header" : Check_file_header(),
                          "Empty line" : Empty_line(),
                          "Preprocessor_Directives" : Preprocessor_Directives(),
                          "Global Variable" : Global_variable(),
                          "Line_Endings" : Line_Endings(),
                          "Trailling_spaces" : Trailling_spaces(),
                          "Identation_error" : Identation_error(),
                          "Curly_brackets" : Curly_brackets(),
                          "Function_length" : Function_length(),
                          "Arguments_nbr" : Arguments_nbr(),
                          "Too_many_functions" : Too_many_functions(),
                          "Misplaced_spaces" : Misplaced_spaces(),
                          "Too_many_depth" : Too_many_depth(),
                          "Line_Break" : Line_Break(),
                          "Check_include" : Check_include(),
                          "Check_Goto" : Check_Goto(),
                          "Include Guard" : Include_guard(),
                          "Comment_Check" : Comment_Check(),
                          "TraillingLine" : TraillingLine(),
                          "CodeLineContent" : CodeLineContent(),
                          "VariableDeclaration" : VariableDeclaration(),
                          "NamingIdentifiers" : NamingIdentifiers(),
                          "Pointers" : Pointers()}
        self.organisation_norms = Check_file()
        self.major = []
        self.minor = []
        self.info = []
        self.bad_files = []
        self.error_nbr = 0
        self.minor_color = "\033[93;1m"
        self.major_color = "\033[91;1m"
        self.info_color = "\033[36;1m"
        self.reset_color = "\033[0m"
        self.ignored_files = []
        self.major_nbr = 0
        self.minor_nbr = 0
        self.info_nbr = 0
        self.var_types = [ "int", "char", "float", "double", "void", "DIR", "size_t", "size", "ssize_t", "dirent", "stat", "long", "WINDOW", "sfCircleShape", "sfConvexShape", "sfFont", "sfImage", "sfShader", "sfRectangleShape", "sfRenderTexture", "sfRenderWindow", "sfShape", "sfSprite", "sfText", "sfTexture", "sfTransformable", "sfVertexArray", "sfVertexBuffer", "sfView", "sfContext", "sfCursor", "sfWindow", "sfMusic", "sfSound", "sfSoundBuffer", "sfSoundBufferRecorder", "sfSoundRecorder", "sfSoundStream", "sfFtpDirectoryResponse", "sfFtpListingResponse", "sfFtpResponse", "sfFtp", "sfHttpRequest", "sfHttpResponse", "sfHttp", "sfPacket", "sfSocketSelector", "sfTcpListener", "sfTcpSocket", "sfUdpSocket", "sfClock", "sfMutex", "sfThread" ]

        ## Option rules

        self.rule = rule
        self.json_rule = json_rule
        self.all_rule = all_rule
        
        ## Goto rule

        self.goto = False

        ## Json List on error for option -json argument

        self.json_output = {"major" : {"count" : 0, "list": {}},
                            "minor" : {"count" : 0, "list": {}},
                            "info" : {"count" : 0, "list" : {}}}
        self.inside = 0

    def check_for_goto(self, directory, paths):
        for files in directory:
            absolute_path = paths + "/" + files
            if path.isdir(absolute_path):
                self.check_for_goto(os.listdir(absolute_path), absolute_path)
            else:
                if (absolute_path.endswith(".c")):
                    inside = open(absolute_path, "r", encoding="utf8", errors='ignore')
                    line = 0
                    for lines in inside:
                        line += 1
                        if " goto " in lines:
                            print("\033[1;32mSorry there was a goto, so i \033[0;1mgot to\033[1;32m the end of the checking ^^'.(Don't use goto please)\033[0m")
                            inside.close()
                            quit(1)
                    inside.close()


    def get_struct(self, direct, paths):
        for files in direct:
            test = paths + "/" + files
            if path.isdir(test):
                self.get_struct(os.listdir(test), test)
            else:
                if (test[-1] == 'h' and test[-2] == '.'):
                    inside = open(test, "r", encoding="utf8", errors='ignore')
                    begin = 0
                    for lines in inside:
                        if "typedef" in lines:
                            begin = 1
                        tot=lines.replace(" ", "")
                        if begin == 1 and tot[0] == '}':
                            i = 0
                            tot=lines.replace(" ", "").replace("}", "").replace(";\n", "").replace("\n", "")
                            if len(tot) > 0:
                                self.var_types += [tot]

    def browse_directory(self, directory, paths):

        ### Use : A function that browse reccursivly through each file and folder begin to the current user position

        for files in directory:
            test = paths + "/" + files
            if test in self.ignored_files:
                continue
            
            ### Checking if the file is a folder

            if path.isdir(test) and files != "tests" and files[0] != '.':
                ## Checking include because specifics rule applies to this folder
                if (files == "include"):
                    inc = Check_Include()
                    inc.run(test, self.rule)

                # Checking 04 and 01 and putting errors in bad files
                obj = self.organisation_norms
                obj.check_04(files, test, self)
                self.browse_directory(os.listdir(test), paths + "/" + str(files))
            else:

                ### Checking Rules

                # Checking organisation norms
                if (files[0] != '.'):
                    obj = self.organisation_norms
                    obj.run(files, paths + "/" + files, self)

                ## Checking file extension

                if (".c" in files or ".h" in files or "Makefile" in files or ".o" in files):
                    if ((files[-1] == 'c' and files[-2] == '.') or "Makefile" in files or (files[-1] == 'h' and files[-2] == '.')) and not("~" in files) and not(".swp" in files) and files.replace("./", "")[0] != '.':
                        
                        ## Checking Rule list

                        for rules in self.norm_list:
                            obj = self.norm_list[rules]
                            if obj.checked == True or self.all_rule == True:
                                obj.run(self, paths + "/" + files)
                    
                    ## Checking if there is errors to display

                    if (len(self.major) != 0 or len(self.minor) != 0 or len(self.info) != 0):
                        self.error_nbr += 1
                        filename = test[2:].replace(BASEPATH[2:] + '/', "")

                        ### Displaying file name
                        if not self.json_rule:
                            if (self.rule == False): print("\033[1m‣ In File", filename)
                            else:
                                self.inside = open("trace.md", "a")
                                self.inside.write("# ‣ In File " + filename + "\n\n")
                                self.inside.close()
                        
                        ### Displayer of found errors in files and adding errors to json rule if needed

                        # Displaying Major Coding Style errors
                        for i in self.major:

                            # Adding error in json output depending on options
                            if self.json_rule:
                                self.json_output["major"]["count"] += 1
                                if i[0] not in self.json_output["major"]["list"]:
                                    self.json_output["major"]["list"][i[0]] = { "description" : i[1], "list" : [ { "file" : filename, "line": i[2] } ] }
                                else:
                                    self.json_output["major"]["list"][i[0]]["list"].append({ "file" : filename, "line": i[2] })

                            # Displaying Major error
                            else :print_error(filename, "major", i, self.rule)

                        # Displaying Minor Coding Style errors
                        for i in self.minor:

                            # Adding error in json output depending on options
                            if self.json_rule:
                                self.json_output["minor"]["count"] += 1
                                if i[0] not in self.json_output["minor"]["list"]:
                                    self.json_output["minor"]["list"][i[0]] = { "description" : i[1], "list" : [ { "file" : filename, "line": i[2] } ] }
                                else:
                                    self.json_output["minor"]["list"][i[0]]["list"].append({ "file" : filename, "line": i[2] })

                            # Displaying Minor error
                            else: print_error(filename, "minor", i, self.rule)

                        # Displaying Info Coding Style errors
                        for i in self.info:

                            # Adding error in json output depending on options
                            if self.json_rule:
                                self.json_output["info"]["count"] += 1
                                if i[0] not in self.json_output["info"]["list"]:
                                    self.json_output["info"]["list"][i[0]] = { "description" : i[1], "list" : [ { "file" : filename, "line": i[2] } ] }
                                else:
                                    self.json_output["info"]["list"][i[0]]["list"].append({ "file" : filename, "line": i[2] })

                            # Displaying info error
                            else: print_error(filename, "info", i, self.rule)

                        # Displaying Line Break Depending on options
                        if not self.json_rule:
                            if (self.rule == False): print("\033[0m")
                            else:
                                self.inside = open("trace.md", "a")
                                self.inside.write("\n")
                                self.inside.close()
                    
                    ### Reset of error tabs for next file and Incrementation of total error number for final report

                    self.major_nbr += len(self.major)
                    self.minor_nbr += len(self.minor)
                    self.info_nbr += len(self.info)
                    self.major = []
                    self.minor = []
                    self.info = []

    def run(self):
        ## Run function
        ## Use : Run Main rule

        # Generating clang file for L3 Detection
        os.system("echo \"BasedOnStyle: LLVM\nAccessModifierOffset: -4\nAllowShortIfStatementsOnASingleLine: false\nAlignAfterOpenBracket: DontAlign\nAlignOperands: false\nAllowShortCaseLabelsOnASingleLine: true\nContinuationIndentWidth: 0\nBreakBeforeBraces: Linux\nColumnLimit: 0\nAllowShortBlocksOnASingleLine: false\nAllowShortFunctionsOnASingleLine: None\nFixNamespaceComments: false\nIndentCaseLabels: false\nIndentWidth: 4\nNamespaceIndentation: All\nTabWidth: 4\nUseTab: Never\nSortIncludes: true\nIncludeBlocks: Preserve\" > .clang-format")

        # Don't ignore files if the -md is active for DiscordCi.
        if not self.rule:
            process = subprocess.Popen(["git", "clean", "-ndX"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.ignored_files = [BASEPATH + line.decode().split()[-1] for line in process.stdout.readlines()]

        # Get types
        self.get_struct(os.listdir(BASEPATH), BASEPATH)

        self.check_for_goto(os.listdir(BASEPATH), BASEPATH)

        # Start Check_Error
        self.browse_directory(os.listdir(BASEPATH), BASEPATH)

        # Erasing Clang file
        os.system("rm .clang-format")

        # Displaying bad files if needed
        if len(self.bad_files) > 0:
            self.error_nbr += 1
            if (not self.json_rule):
                if (self.rule == False): print("\033[1m‣ Bad files :\033[0m")
                else:
                    self.inside = open("trace.md", "a")
                    self.inside.write("# ‣ Bad files :\n\n")
                    self.inside.close()
            for i in self.bad_files:

                ### Adding errors in json file depending of options given as paramater

                if self.json_rule:
                    self.json_output["major"]["count"] += 1
                    if not(i[0] in self.json_output["major"]["list"]):
                        self.json_output["major"]["list"][i[0]] = { "description" : i[1], "list" : [ { "file" : i[2].replace(BASEPATH[2:] + '/', ""), "line": "" } ] }
                    else:
                        self.json_output["major"]["list"][i[0]]["list"].append({ "file" : i[2].replace(BASEPATH[2:] + '/', ""), "line": "" })
                else:
                    print_error("", "major", i, self.rule)
            if not self.json_rule:
                if (self.rule == False): print("")
                else:
                    self.inside = open("trace.md", "a")
                    self.inside.write("\n")
                    self.inside.close()
            # Jenkins check for Abricot's Performance
            if "JENKINS" in os.environ:
                sys.exit(0)
            self.major_nbr += len(self.bad_files)
        if not self.json_rule:
            if (self.rule == False):
                if self.error_nbr == 0:
                    print("\033[1;32mNo Coding style error detected : Code clean\033[0m")
                    if "JENKINS" in os.environ:
                        sys.exit(1)
                else:
                    ## Display Report of all errors
                    print("\033[1mHere's your report:")
                    print(self.major_color + "[MAJOR]" + self.reset_color + " : ", self.major_nbr, end=" | ")
                    print(self.minor_color + "[MINOR]" + self.reset_color + " : ", self.minor_nbr, end=" | ")
                    print(self.info_color + "[INFO]" + self.reset_color + " : ", self.info_nbr)
            else:
                # This code set a variable used for DiscordCi when the program is
                # called with args -md.
                # The print function is normal here.

                # Set env var NORM to 0 or 1.
                if self.major_nbr != 0 or self.minor_nbr != 0:
                    print(f"::set-output name=NORM::1")
                else:
                    print(f"::set-output name=NORM::0")

                # Set env var to a JSON with details of error.
                output = {}
                output["major"] = self.major_nbr
                output["minor"] = self.minor_nbr
                output["info"] = self.info_nbr
                print(f"::set-output name=SUMMARY::{JSONEncoder().encode(output)}")
        else: print(JSONEncoder().encode(self.json_output))

def main():
    global BASEPATH
    BASEPATH = './'
    rule=False
    json_rule=False
    all_rule=False
    if (len(sys.argv) == 2):
        if (sys.argv[1] == "-md"): rule = True
        if (sys.argv[1] == "-json"): json_rule = True
        if (sys.argv[1] == "--all"): all_rule = True
    if (len(sys.argv) == 3):
        if (sys.argv[1] == "--dir"):
            BASEPATH = './' + sys.argv[2]
            json_rule = True
    rule = Norms(rule, json_rule, all_rule)
    rule.run()

main()
