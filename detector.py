# encoding=utf-8
# life is short, i use python.

import os
import os.path
import re

rootdir = "/Users/cty/Documents/EclipseWebWorkspace/TSIN"
classes_contain_pairfunc = []

for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        if filename.endswith(".java"):
            file = open(os.path.join(parent, filename))
            try:
                all_text = file.read()
            finally:
                file.close()
            if '.close()' in all_text and '.getConnection(' in all_text:
                # print 'filename: ' + filename
                # classes_contain_pairfunc.append(parent[parent.rfind('/') + 1:] + '.' + filename[:filename.find('.java')])
                classes_contain_pairfunc.append((parent[parent.rfind('/') + 1:],
                    filename[:filename.find('.java')]))

# for debug
# for i in classes_contain_pairfunc:
#     print i

## ClassName instanceName = new ClassName()
## <jsp:useBean id="videoDisplay" class="video.Display" scope="request" />

for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        if filename.endswith('.jsp'):
            # 对于每个 jsp 文件
            # print "filename: " + filename
            file = open(os.path.join(parent, filename))
            try:
                all_text = file.read()
            finally:
                file.close()
            # instancenames = []
            for classname in classes_contain_pairfunc:
                instances =  re.findall(r'<jsp:useBean id="(.+)" class="'
                    + classname[0] + '\.' + classname[1]
                    + '" scope="request"[ \t]*/>', all_text)
                if instances != []:
                    # print '\tclassname: ' + classname[0] + '.' + classname[1]
                    for instance in instances:
                        if all_text.find(instance + '.release()') == -1:
                            print 'warning: in file ' + filename + ' instance ' + instance + ' of class ' + classname[1] + ' in package ' + classname[0] + ' may not be properly released. '
