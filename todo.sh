#!/usr/bin/env bash

# python3 todo.py "$@"
python3 $0.py "$@"

# This satisfies specification 4 listed in provided readme.md
# i.e. The application must open the files todo.txt and done.txt from where the app is run,
# and not where the app is located.
# HOW?
# To run cmd we have to type => path/to/app/todo cmd
# $0 is mapped to first cmd line arg => path/to/app/todo
# which runs => python3 path/to/app/todo.py "$@" in current directory

# To use todo cmd whithout specifying complete path  => todo ls
# add sym link todo to PATH
#export PATH=$PATH:/absolute/path/to/app/directory
#to permanantly add to PATH add above cmd to appropriate profile file ex. ~/.bashrc

# NOTE
# todo , todo.sh , todo.py must be in same directory

