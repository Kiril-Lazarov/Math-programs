'''
    Description:
    The purpose of this program is to overcome the limit of recursive calls set by Python - 996 times.
The idea is for a piece of code to be written into a separate file and then run that file. This file writes the same
piece of code in a subsequent file, etc. For example, file_1 writes file_2 and calls it. File_2 writes file_3,
calls it and deletes file_2. Since no recursive function calls are made in this way, there is no maximum number
of calls. In this way, the memory is not clogged - at any given moment there are only two files of code. Due to
the constant creation and deletion of files, the process is very slow.
'''

import os
import subprocess
n = 1

if n <100:
    with open(f'file_{n}.py', 'w') as file:
        print(f'n = {n}')
        # next file name
        call_string = f'file_{n}.py'
        n+=1
        script = open('script_file.txt')
        script = script.read()
        # the content of a new file
        file.write(f'import os\nimport subprocess\n\nn = {n}\nif n < 4:\n{script}\n'
                   f'    if n -1 >1:\n   '
                   f'     file = f"file_{n-1}.py"\n        os.remove(file)\n    '
                   f'subprocess.call(["python.exe", call_string])\n'
                   f'else:\n    print("End program")')

    # checks whether the number of the current file is grater than 1.If it is - delete
    #the previous file and call the current py. file.
    if n -1 >1:
        file = f'file_{n-1}.py'
        os.remove(file)
    subprocess.call(['python.exe', call_string])
else:
    print('End program')
