[![Build Status](https://travis-ci.org/geeeh/boot-camp.svg?branch=master)](https://travis-ci.org/geeeh/boot-camp)
[![Coverage Status](https://coveralls.io/repos/github/geeeh/boot-camp/badge.svg?branch=master)](https://coveralls.io/github/geeeh/boot-camp?branch=master)

#Dojo allocator

Dojo allocator is a command line python project for room allocation in the Dojo. It allows users to create rooms and allocate people to the created rooms.

#requirements

    - python 3.4 or higher
    - SQLite3
    - python-pip
#setup

    - clone project from https://github.com/geeeh/boot-camp.git
    - move into the project folder. 'cd boot-camp'
    - install all the requirements. 'pip install -r requirements.txt'
    - run your application. 'python dojo.py -i'
#usage

    - create_room <room_name>...
    - add_person [--accomodate=N]
    - reallocate_person
    - load_people
    - print_room <room_name>
    - print_allocations [--o=filename]
    - print_unallocated [--o=filename]
    - save_state [--o=db_name]
    - quit
    - dojo (-i|--interactive)
    - dojo (-h|--help)

#contributor

    - Godwin Gitonga