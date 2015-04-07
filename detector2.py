# root_dir = '/Users/cty/Documents/android-master'
# dir of hyper sql db
# root_dir = '/Users/cty/Documents/hsqldb'
# dir of hibernate
root_dir = '/Users/cty/Documents/axion-master'
dict_path = '/Users/cty/Documents/coding/violations_detector/dictionary.txt'

from srcfileutils import *
import itertools
import string
import re

# get the function names list
func_names = find_method_names(root_dir)
# debug info
print str(len(func_names)) + ' methods found. '
# for name in func_names:
#     print name
antonym_dict = read_antonym_dict('dictionary.txt')
paired_methods = generate_paired_func_list(func_names, antonym_dict)
# debug info
print str(len(paired_methods)) + ' possible \'paired\' funcs. '
try_catch_blocks = find_try_catch_blocks(root_dir)
print str(len(try_catch_blocks)) + ' try-catch blocs found. '
# for i in try_catch_blocks:
#     print i
#     print '*****\n'

violations = detect_violations(try_catch_blocks, paired_methods)

print 'total ' + str(len(violations)) + ' possible violations. '
violations.sort(cmp = lambda x, y: cmp(x[5], y[5]), reverse = True)
for i in range(0, 40):
    print '**********'
    for j in violations[i]:
        print j
