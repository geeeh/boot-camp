import os
import random

import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from termcolor import colored

from database.model_classes import DatabaseBuilder, dec_base, DRoom, DPerson, OfficeAllocations, LivingSpaceAllocations
from person.person import Fellow, Staff
from room.room import Office, LivingSpace


class Dojo(object):
    def __init__(self):
        self.rooms = []
        self.living_space_allocations = {"unallocated": []}
        self.office_allocations = {"unallocated": []}
        self.lspace_ids = {"unallocated":[]}
        self.office_ids = {"unallocated":[]}
        self.last_position = 0
        self.people = []
        self.load_state()

    def create_room(self, room_type, room_name):
        """create a new room, add it to room list and its specific allocation type dictionary. it also creates a
        dictionary for the user ids """
        room_name = room_name.lower()
        if room_name in [room.room_name for room in self.rooms]:
            return colored("room already exists", "red")

        else:
            map_object = {'office': Office, 'living_space': LivingSpace}
            room_object = map_object[room_type](room_name)
            self.rooms.append(room_object)

            if room_type == "living_space":
                self.living_space_allocations[room_name] = []
                self.lspace_ids[room_name] = []

            elif room_type == "office":
                self.office_allocations[room_name] = []
                self.office_ids[room_name] = []
            self.auto_allocate(room_type)

            return colored(room_type + " " + room_name + " created successfully.",
                           "green")

    def auto_allocate(self, room_type):
        pass

    def add_person(self, first_name, last_name, person_type, accommodation="N"):
        """create person object and add it to people list and allocates the person a room"""
        name = first_name.lower() + " " + last_name.lower()
        accommodation = accommodation.upper()
        person_number = self.assign_position()
        map_object = {"fellow": Fellow, "staff": Staff}
        new_person = map_object[person_type](name, person_number)
        self.people.append(new_person)
        office_allocated = self.get_office()
        self.office_allocations[office_allocated].append(name)
        self.office_ids[office_allocated].append(person_number)
        if office_allocated != "unallocated":
            print(colored(name + " id: " + str(person_number) + ", Successfully added and allocated office " +
                          office_allocated, "green"))
        else:
            print(colored(name + " id: " + str(person_number) + " unallocated office", "red"))
        if person_type == "fellow" and accommodation == "Y":
            living_space_allocated = self.get_living_space()
            self.living_space_allocations[living_space_allocated].append(name)
            self.lspace_ids[living_space_allocated].append(person_number)
            if living_space_allocated != "unallocated":
                print(colored(name + " id: " + str(person_number) + " allocated living space " +
                              living_space_allocated, "green"))
            else:
                print(colored(name + " id: " + str(person_number) + " unallocated living space", "red"))
        if person_type == "staff" and accommodation == "Y":
            print(colored("Staff cannot be allocated living spaces", "red"))

    def assign_position(self):
        """return an id to be assigned to the person added"""
        self.last_position += 1
        return self.last_position

    def get_living_space(self):
        """returns random living space to allocate a fellow by checking for living spaces available and those not to
        maximum capacity yet """
        living_spaces = [
            room for room in self.rooms
            if room.room_type == "living_space"]
        living_spaces_to_allocate = []
        for room in living_spaces:
            if room.capacity > len(self.living_space_allocations[room.room_name]):
                living_spaces_to_allocate.append(room.room_name)
        number_of_lspaces = len(living_spaces_to_allocate)
        if number_of_lspaces > 0:
            room_to_allocate = random.choice(living_spaces_to_allocate)
        else:
            return "unallocated"
        return room_to_allocate

    def get_office(self):
        """returns random living space to allocate a fellow by checking for office spaces available and those not to
        maximum capacity yet """
        offices = [
            room for room in self.rooms if room.room_type == "office"]
        offices_to_allocate = []
        for room in offices:
            if room.capacity > len(self.office_allocations[room.room_name]):
                offices_to_allocate.append(room.room_name)
        number_of_offices = len(offices_to_allocate)
        if number_of_offices > 0:
            room_to_allocate = random.choice(offices_to_allocate)
        else:
            return "unallocated"
        return room_to_allocate

    def print_room(self, room_name):
        """display people in a given room"""
        available_offices = self.available_offices()
        available_living_spaces = self.available_living_spaces()
        if room_name in self.office_allocations.keys():
            if len(self.office_allocations[room_name]) == 0:
                return "room " + room_name + " is empty"

        if room_name in self.living_space_allocations.keys():
            if len(self.living_space_allocations) == 0:
                return "room " + room_name + " is empty"
        if room_name not in self.office_allocations.keys() and room_name not in self.living_space_allocations.keys():
            print(colored("room " + room_name + " does not exist", "red"))
        else:
            print(colored(" " * 20 + room_name + "\n", "blue"))
            print("-" * 50 + "\n")
            if room_name in available_offices:
                person_names = [name for name in self.office_allocations[room_name]]
                person_ids = [id for id in self.office_ids[room_name]]
                people_with_ids = zip(person_ids, person_names)
                for item in people_with_ids:
                    item = list(item)
                    print(str(item[0]) + "\t" + item[1])

            if room_name in available_living_spaces:
                person_names = [name for name in self.living_space_allocations[room_name]]
                person_ids = [id for id in self.lspace_ids[room_name]]
                people_with_ids = zip(person_ids, person_names)
                for item in people_with_ids:
                    item = list(item)
                    print(str(item[0]) + "\t" + item[1])

    def available_offices(self):
        """returns offices available in office allocations"""
        available_offices = []
        for room in self.office_allocations:
            if room != "unallocated":
                available_offices.append(room)
        return available_offices

    def available_living_spaces(self):
        """returns living spaces available in living space allocations"""
        available_living_spaces = []
        for room in self.living_space_allocations:
            if room != "unallocated":
                available_living_spaces.append(room)
        return available_living_spaces

    def load_people(self, filename):
        """add people from a file"""
        if os.path.isfile(filename):
            file = open(filename, 'r')
            mylist = file.readlines()
            for line in mylist:
                my_args = line.split()
                if len(my_args) > 3:
                    self.add_person(my_args[0].lower(), my_args[1].lower(), my_args[2].lower(),
                                    my_args[3].upper())
                else:
                    self.add_person(my_args[0], my_args[1], my_args[2].lower())
            file.close()
            return colored("data loaded successfully", "green")
        else:
            return colored("file not found", "red")

    def print_allocations(self, filename=None):
        """prints out list of all allocations"""
        if len(self.office_allocations) <= 1 and len(self.living_space_allocations) <= 1:
            return colored("no allocations to print", "red")
        else:
            if filename:

                for room in self.office_allocations.keys():
                    if room != "unallocated":
                        self.print_text_output(
                            filename, "office " + room, self.office_allocations[room])

                for room in self.living_space_allocations.keys():
                    if room != "unallocated":
                        self.print_text_output(filename,
                                               "living space " + room,
                                               self.living_space_allocations[room])
                return colored(filename + " written successfully", "green")
            else:
                for room in self.office_allocations.keys() :
                    if room != "unallocated":
                        print(room + "\n")
                        print("-" * 20 + "\n")
                        person_names = [name for name in self.office_allocations[room]]
                        person_ids = [id for id in self.office_ids[room]]
                        people_with_ids = zip(person_ids, person_names)
                        for item in people_with_ids:
                            item = list(item)
                            print(str(item[0]) + "\t" + item[1])

                for room in self.living_space_allocations.keys():
                    if room != "unallocated":
                        print( room + "\n")
                        print("-" *20 + "\n")
                        person_names = [name for name in self.living_space_allocations[room]]
                        person_ids = [id for id in self.lspace_ids[room]]
                        people_with_ids = zip(person_ids, person_names)
                        for item in people_with_ids:
                            item = list(item)
                            print(str(item[0]) + "\t" + item[1])
                return colored("done!", "green")

    def print_text_output(self, filename, heading, my_list):
        """print output to a file"""
        file = open(filename, "a")
        file.write(" " * 10 + heading + "\n")
        file.write("-" * 60 + "\n")
        for item in my_list:
            file.write(item + "\n")
        file.close()

    def print_unallocated(self, filename=None):
        """prints a list of unallocated people"""
        if len(self.office_allocations["unallocated"]) == 0 and len(self.living_space_allocations["unallocated"]) == 0:
            return colored("no list of unallocated people", "green")
        else:
            if filename:
                if len(self.office_allocations["unallocated"]) != 0:
                    self.print_text_output(
                        filename, "people without offices", self.office_allocations["unallocated"])
                if len(self.living_space_allocations["unallocated"]) != 0:
                    self.print_text_output(
                        filename, "people without offices", self.living_space_allocations["unallocated"])
            else:
                if len(self.office_allocations["unallocated"]) != 0:
                    print( "people without offices\n")
                    print("-" * 30 + "\n")
                    person_names = [name for name in self.office_allocations["unallocated"]]
                    person_ids = [id for id in self.office_ids["unallocated"]]
                    people_with_ids = zip(person_ids, person_names)
                    for item in people_with_ids:
                        item = list(item)
                        print(str(item[0]) + "\t" + item[1])

                if len(self.living_space_allocations["unallocated"]) != 0:
                    print("people without living spaces")
                    print("-" * 30 + "\n")
                    person_names = [name for name in self.living_space_allocations["unallocated"]]
                    person_ids = [id for id in self.lspace_ids["unallocated"]]
                    people_with_ids = zip(person_ids, person_names)
                    for item in people_with_ids:
                        item = list(item)
                        print(str(item[0]) + "\t" + item[1])

    def load_state(self, default_db="default_db"):
        pass

    def reallocate_person(self, psn_id, room_name):
        """captures data of people to be reallocated"""
        psn_id = int(psn_id)
        fellows = [person.person_number for person in self.people
                   if person.person_type == "fellow"]
        staff = [person.person_number for person in self.people
                 if person.person_type == "staff"]
        available_lspaces = [room.room_name for room in self.rooms
                             if room.room_type == "living_space" and len(
                self.living_space_allocations[room.room_name]) < room.capacity]
        available_offices = [room.room_name for room in self.rooms
                             if room.room_type == "office" and
                             len(self.office_allocations[room.room_name]) < room.capacity]

        if room_name in available_lspaces or room_name in available_offices:
            if psn_id not in fellows and psn_id not in staff:
                return colored(" person to reallocate doesn't exist.", "red")
            else:
                name = [person.name for person in self.people
                        if person.person_number == psn_id]
                my_name = name[0]
                if room_name in self.living_space_allocations.keys():
                    for a_room in self.living_space_allocations.keys():
                        if my_name in self.living_space_allocations[a_room]:
                            self.living_space_allocations[a_room].remove(my_name)
                            self.lspace_ids[a_room].remove(psn_id)
                            self.living_space_allocations[room_name].append(my_name)
                            self.lspace_ids[room_name].append(psn_id)
                            return colored(my_name + " successfully reallocated to living space " + room_name, "green")
                if room_name in self.office_allocations.keys():
                    for a_room in self.office_allocations.keys():
                        if my_name in self.office_allocations[a_room]:
                            my_current_office = self.office_allocations[a_room]
                            my_current_office.remove(my_name)
                            my_current_space = self.office_ids[a_room]
                            my_current_space.remove(psn_id)
                            self.office_allocations[room_name].append(my_name)
                            self.office_ids[room_name].append(psn_id)
                            return colored(my_name + " successfully reallocated to office" + " " + room_name, "green")
        else:
            return colored("room not available for reallocation", "red")

    def save_state(self, db_name="my_default_db"):
        """saves all captured data to a database"""
        my_db = DatabaseBuilder(db_name)
        dec_base.metadata.bind = my_db.engine
        db_session = my_db.session()
        for room in self.rooms:
            a_room = DRoom(
                room_name=room.room_name,
                room_type=room.room_type,
                capacity=room.capacity)
            db_session.add(a_room)

        for person in self.people:
            a_people = DPerson(
                name=person.name,
                person_type=person.person_type,
                person_number=person.person_number)
            db_session.add(a_people)

        for room in self.office_allocations:
            office_members = ",".join(self.office_allocations[room])
            member_ids = ""
            for item in self.office_ids[room]:
                member_ids += str(item) + ","
            saved_allocations = OfficeAllocations(
                room_name=room,
                members=office_members,
                member_ids=member_ids)
            db_session.add(saved_allocations)

        for room in self.living_space_allocations:
            living_space_members = ",".join(self.living_space_allocations[room])

            member_ids = ""
            for item in self.lspace_ids[room]:
                member_ids += str(item) + ","
            saved_allocations = LivingSpaceAllocations(
                room_name=room,
                members=living_space_members,
                member_ids=member_ids)
            db_session.add(saved_allocations)

        db_session.commit()
        return colored("data saved to database successfully!", "green")

    def load_state(self, db_name=None):
        """Loads data from database"""
        if db_name:
            if os.path.isfile(db_name + ".sqlite"):
                engine = create_engine("sqlite:///" + db_name + ".sqlite")
                my_sess = sessionmaker()
                my_sess.configure(bind=engine)
                session = my_sess()
                for new_person in session.query(DPerson).all():
                    self.people.append(new_person)

                for room in session.query(DRoom).all():
                    self.rooms.append(room)

                for allocation in session.query(OfficeAllocations).all():
                    all_members = allocation.members.split(",")
                    member_ids = [num for num in allocation.member_ids.split(",")]
                    member_ids.remove('')
                    member_ids = [int(num) for num in member_ids]
                    self.office_allocations[allocation.room_name] = all_members
                    self.office_ids[allocation.room_name] = member_ids

                for living_space_allocation in session.query(LivingSpaceAllocations).all():
                    all_members = living_space_allocation.members.split(",")
                    member_ids = [num for num in living_space_allocation.member_ids.split(",")]
                    member_ids.remove('')
                    member_ids = [int(num) for num in member_ids]
                    self.living_space_allocations[
                        living_space_allocation.room_name] = all_members
                    self.lspace_ids[
                        living_space_allocation.room_name] = member_ids
                self.load_last_id(db_name + ".sqlite")
                return colored("Data from %s loaded successfully" % db_name, "green")
            else:
                return colored("invalid file", "red")

        else:
            return colored("enter database file name", "red")

    def load_last_id(self, db_name=None):
        """get the last existing id from database"""
        if os.path.isfile(db_name):
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            query = "SELECT max(person_number) FROM person"
            cursor = c.execute(query)
            last_id = cursor.fetchone()[0]
            self.last_position = last_id
        else:
            self.last_position = 0





