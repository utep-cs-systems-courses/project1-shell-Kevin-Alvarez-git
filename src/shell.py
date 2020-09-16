#! /usr/bin/env python3

import os
import sys
import re

# Check if $PS1 is set
try:
    sys.ps1
except AttributeError:
    sys.ps1 = "$ " 

user_in = input(sys.ps1)

while user_in != "exit":
    rc = os.fork()
    args = re.split(" ", user_in)
    tries = 0
    
    if rc < 0:
        sys.exit(1)

    elif rc == 0:
        for dir in re.split(":", os.environ['PATH']):
            prompt = "%s/%s" % (dir, args[0])
            
            try:
                os.execve(prompt, args, os.environ)
            except FileNotFoundError:
                pass

        sys.exit(1)

    else:
        if args[0] == 'cd':
            os.chdir(args[1])
        child_pid = os.wait()
    
    user_in = input(sys.ps1)

