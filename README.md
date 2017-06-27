[![Build Status](https://travis-ci.org/geeeh/boot-camp.svg?branch=master)](https://travis-ci.org/geeeh/boot-camp)
[![Coverage Status](https://coveralls.io/repos/github/geeeh/boot-camp/badge.svg?branch=master)](https://coveralls.io/github/geeeh/boot-camp?branch=master)

# Dojo allocator

Dojo allocator is a command line python project for room allocation in the Dojo. It allows users to create rooms and allocate people to the created rooms.

# requirements

    - python 3.4 or higher
    - SQLite3
    - python-pip
    
---
# setup

- Create a virtual environment
```
virtualenv venv
```

- Activate your virtual environment
```
source venv/bin/activate
```

- Clone the repo

> git clone https://github.com/geeeh/boot-camp.git

- Once in the app directory, install Requirements
```pip install -r requirements.txt```


---
   
# usage

    - create_room <room_name>...
    - add_person <first_name> <last_name> <fellow|staff> [--c=N]
    - reallocate_person <person_identifier> <new_room_name>
    - load_people <filename>
    - print_room <room_name>
    - print_allocations [--o=filename]
    - print_unallocated [--o=filename]
    - save_state [--o=db_name]
    - quit
    - dojo (-i|--interactive)
    - dojo (-h|--help)
    
 ---
# Explanation:


```dojo create_room (living_space|office) <room_name>...``` 
 command creates rooms in the Dojo
> Using this command, the user can create as many rooms as possible by specifying multiple room names
  after the create_room command.

```add_person <first_name> <last_name> <fellow|staff> [--c]``` 
adds a person to the system and allocates the person
 a random room
>--c here is an optional argument which can be either Y or N.
Its default value when it is not provided is N.

```print_room <room_name>``` 
prints  the names of all the people in room_name on the screen.

```print_allocations [--o=filename]```  
prints a list of allocations onto the screen.
> Specifying the optional -o option here outputs the registered allocations to a txt file.

```print_unallocated [--o=filename]``` 
prints a list of unallocated people to the screen.
> Specifying the -o option here outputs the information to the txt file provided.

```reallocate_person <person_identifier> <new_room_name>```
reallocates the person with person_identifier to new_room_name.

```load_people <filename>``` 
adds people to rooms from a txt file.

```save_state [--db=sqlite_database]```
 persists all the data stored in the app to a SQLite database.
> Specifying the --db parameter explicitly stores the data in the sqlite_database specified.

```load_state [--o=filename]``` 
loads data from a database into the application.

---
# License

- This app is provided under the [MIT License](https://opensource.org/licenses/MIT)

---
#contributor

    - Godwin Gitonga