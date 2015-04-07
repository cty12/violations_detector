# this is the module offering some utils for processing java src files

import os
import os.path
import re
import string
import itertools

version = 0.1

def find_method_names(root_dir):
    # pattern string for functions
    pattern_function = re.compile('(?:(?:public|private|protected|static|final|native|synchronized|abstract|threadsafe|transient)+\s)+[\$_\w\<\>\[\]]*\s+([\$_\w]+)\([^\)]*\)?\s*\{?[^\}]*\}?')
    all_func_names = list()

    for parent, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # select all java files
            if filename.endswith('.java'):
                # open and read file
                file = open(os.path.join(parent, filename))
                try:
                    # read file
                    all_text = file.read()
                finally:
                    file.close()
                # find functions from the java file
                func_names = re.findall(pattern_function, all_text)
                # add them to the list
                # all_func_names.extend(func_names)
                for name in func_names:
                    # get rid of all the constructors
                    if name[0] in string.lowercase:
                        all_func_names.append(name)

    # unify the names
    return list(set(all_func_names))

def find_try_catch_blocks(root_dir):
    # pattern string for try-catch blocks
    pattern_try_catch = re.compile('try\s*\{(?:(?!try)[^\}])*\}(?:\s*catch\s*\(.+\)\s*\{(?:(?!try)[^\}])*\})+(?:\s*finally\s*\{[^\}]*\})?')
    blocks = list()

    for parent, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.java'):
                # open and read file
                file = open(os.path.join(parent, filename))
                try:
                    # read file
                    all_text = file.read()
                finally:
                    file.close()
                try_catch_block = re.findall(pattern_try_catch, all_text)
                # blocks.extend(try_catch_block)
                for block in try_catch_block:
                    blocks.append((block, os.path.join(parent, filename)))

    return blocks

def read_antonym_dict(dict_file):
    antonym_list = list()

    dictionary = open('dictionary.txt', 'r')
    line = dictionary.readline()
    while line:
        tmp = line.split(', ')
        for i in range(0, len(tmp)):
            tmp[i] = tmp[i].strip(' \"\n')
        antonym_list.append(tuple(tmp))
        line = dictionary.readline()

    return antonym_list

def long_substr(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr

def generate_paired_func_list(method_names, antonym_dict):
    print 'generate paired function list start...'
    paired_methods = list(itertools.permutations(method_names, 2))
    paired_methods_val = list()
    cnt = 0
    for pair in paired_methods:
        cnt += 1
        if cnt % 50000 == 0:
            print 'processed: ' + str(cnt)
        pair = list(pair)
        # if the method names are the same,
        # set value to minimum
        if pair[0] == pair[1]:
            pair.append(-1)
        else:
            # if the second method name is the 'opposite' to the first
            if pair[1].endswith(pair[0]) and (pair[1].startswith('re') or
                    pair[1].startswith('un') or
                    pair[1].startswith('re') or
                    pair[1].startswith('de') or
                    pair[1].startswith('dis')):
                # set value to maximum
                pair.append(100000)
            else:
                head1 = re.findall(r'^[a-z0-9]+', pair[0])[0]
                head2 = re.findall(r'^[a-z0-9]+', pair[1])[0]
                body1 = pair[0][len(head1):]
                body2 = pair[1][len(head2):]
                # start with antonym
                if (body1 == body2) and ((head1, head2) in antonym_dict):
                    pair.append(100000)
                # else set value to the length of the longest common str
                else:
                    pair.append(len(long_substr(pair)))
                    # pair.append(1)

        paired_methods_val.append(pair)
    # debug info
    print 'generate paired function list done. '
    return paired_methods_val

def detect_violations(try_catch_blocks, paired_funcs):
    violations = list()
    for block in try_catch_blocks:
        normal_path = re.findall(r'try\s*\{([^\}]*)\}', block[0])[0]
        err_paths = re.findall(r'catch\s*\(.+\)\s*\{([^\}]*)\}', block[0])
        finally_block = re.findall(r'finally\s*\{([^\}]*)\}', block[0])
        if len(finally_block) != 0:
            for index in range(0, len(err_paths)):
                err_paths[index] += ('\n' + finally_block[0])

        for func in paired_funcs:
            if normal_path.find(func[0] + '(') != -1:
                for err_path in err_paths:
                    if err_path.find(func[1] + '(') == -1:
                        violations.append((block, normal_path, err_path, func[0], func[1], func[2]))

    # ((try-catch, class_dir), normal_path, err_path, func_in_normal, func_in_err, value)
    return violations
