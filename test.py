import os
import os.path

root_dir = '/Users/cty/Documents/android-master'

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

            pos = all_text.find('manager.getPassword(account);')
            if pos != -1:
                print os.path.join(parent, filename)
