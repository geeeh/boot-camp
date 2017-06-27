#!/usr/bin/env python
"""
Dojo Room Allocation Program

Usage:
    dojo create_room (office | living_space) <room_name>...
    dojo add_person <firstname> <lastname> (fellow | staff) [--c=N]
    dojo reallocate_person <person_id> <newroom>
    dojo load_people <filename>
    dojo print_room <room_name>
    dojo print_allocations [--o=filename]
    dojo print_unallocated [--o=filename]
    dojo save_state [--o=db_name]
    dojo quit
    dojo (-i|--interactive)
    dojo (-h|--help)

Options:
    -i,--interactive  :  Interactive Mode
    -h,--help  :  shows this message
    --version  :  Dojo app version
"""

import cmd
import sys

import pyfiglet
from docopt import docopt, DocoptExit
from termcolor import colored

from dojo import Dojo

dojo = Dojo()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            msg = 'Invalid Command'
            print(msg)
            print(e)
            return
        except SystemExit:
            return
        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive(cmd.Cmd):

    intro = colored(pyfiglet.figlet_format(
        "Dojo Room Allocator", font="slant") + "\n "+__doc__ , "cyan")
    prompt = '(Dojo)'
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room (office | living_space) <room_name>..."""
        room_name = arg["<room_name>"]
        if arg['office']:
            room_type = "office"
        else:
            room_type = "living_space"
        for name in room_name:
            if name.isalpha():
                print(dojo.create_room(room_type, name))
            else:
                print(colored("names should be alphabetic characters", "red"))

    @docopt_cmd
    def do_add_person(self, arg):
        """
        Usage: add_person <firstname> <lastname> (fellow | staff) [--c=N]

         """
        firstname = arg["<firstname>"]
        lastname = arg["<lastname>"]
        if lastname.isalpha() and firstname.isalpha():
            if arg['fellow']:
                person_type = "fellow"
                if arg["--c"] == "Y" or arg["--c"] == "y":
                    accommodate = arg["--c"]
                    dojo.add_person(firstname, lastname, person_type, accommodate)
                elif arg["--c"] == "N" or arg["--c"] == "n" or arg["--c"] == None:
                    dojo.add_person(firstname, lastname, person_type)
                else:
                    print(colored("accommodate options are N or Y", "red"))
            else:
                if arg["--c"]:
                    print(colored("staff do not get accommodation", "red"))
                else:
                    person_type = "staff"
                    dojo.add_person(firstname, lastname, person_type)

        else:
            print(colored("names should be alphabetic characters", "red"))

    @docopt_cmd
    def do_print_room(self, arg):
        """
                prints a given room's occupants
                Usage: print_room <room_name>
                """
        room_name = arg["<room_name>"]
        dojo.print_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """
                Prints all rooms and the people in them.
                Usage: print_allocations [--o=filename]
                """
        filename = arg["--o"] or ""
        print(dojo.print_allocations(filename))

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """
                Prints all unallocated people in dojo.
                Usage: print_unallocated [--o=filename]
                """
        filename = arg["--o"] or ""
        print(dojo.print_unallocated(filename))

    @docopt_cmd
    def do_reallocate(self, arg):
        """
                reallocates a member a room in the dojo
                Usage: reallocate_person <person_id> <new_room>
                """
        person_id = arg["<person_id>"]
        room_name = arg["<new_room>"]
        print(dojo.reallocate_person(person_id, room_name))

    @docopt_cmd
    def do_save_state(self, arg):
        """
                saves all the data into an sqlite database
                Usage: save_state [--db_name=sqlite_db]
                """
        my_db = arg['--db_name']
        if my_db:
            print(dojo.save_state(my_db))
        else:
            dojo.save_state()
    @docopt_cmd
    def do_load_state(self, arg):
        """
                saves all the data into an sqlite database
                Usage: save_state [--db_name=sqlite_db]
                """
        my_db = arg['--db_name']
        if my_db:
            print(dojo.load_state(my_db))
        else:
            print("add a db name")

    @docopt_cmd
    def do_load_people(self, arg):
        """
                loads people from a file
                Usage: load_people <filename>
                """
        my_file = arg['<filename>']
        if my_file:
            print(dojo.load_people(my_file))


    @docopt_cmd
    def do_quit(self, arg):
        """
                closes the app.
                Usage: quit
                """
        sys.exit()


opt = docopt(__doc__, sys.argv[1:], True)

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
