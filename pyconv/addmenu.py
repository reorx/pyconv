'''
Created on 2012-11-5

@author: reorx
'''

import os
import sys
import subprocess
import platform

_system = platform.system()


def main():
    data_dir_path = os.path.join(os.path.dirname(__file__), 'data')
    if 'Windows' == _system:
        reg_path = os.path.join(data_dir_path, 'addmenu.reg')
        status = subprocess.call(['regedit', '/s', reg_path], stdout=sys.stdout)
        print 'Exit status %s' % status
    else:
        print 'Sorry, your platform %s does not support yet.' % _system


if __name__ == '__main__':
    main()