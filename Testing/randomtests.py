# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 02:08:36 2016

@author: jaspe
"""

import re
import subprocess

p=subprocess.Popen('ipconfig',
        stdout=subprocess.PIPE)
output = p.stdout.read()
RegExp = 'IPv4 Address. . . . . . . . . . . : [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
RegExp1 = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
ipadres = re.findall(RegExp1, re.findall(RegExp, output)[0])
print (ipadres[0])