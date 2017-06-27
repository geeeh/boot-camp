import os
from io import StringIO
from unittest import TestCase

import sys

import sqlite3

from dojo import Dojo


class TestRoom(TestCase):
    """class for testing dojo functions"""
    def setUp(self):
        """setup defaults"""
        self.held, sys.stdout = sys.stdout, StringIO()
        self.my_instance = Dojo()

    def test_create_office(self):
        """test for successful office creation"""
        initial_room_count = len(self.my_instance.rooms)
        self.my_instance.create_room("office", "blue")
        new_room_count = len(self.my_instance.rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)
        self.assertIn("blue", self.my_instance.office_allocations.keys())

    def test_create_living_space(self):
        """test for successful living space creation"""
        initial_room_count = len(self.my_instance.rooms)
        self.my_instance.create_room("living_space", "white")
        new_room_count = len(self.my_instance.rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)
        self.assertIn("white", self.my_instance.living_space_allocations.keys())

    def test_create_room_with_similar_names(self):
        """test whether someone can create rooms will similar names.
        This is not allowed"""
        self.my_instance.create_room("office", "blue")
        output = self.my_instance.create_room("office", "blue")
        self.assertIn("room already exists", output)

    def test_add_staff(self):
        """"test for successful staff addition to the dojo"""
        initial_person_count = len(self.my_instance.people)
        self.my_instance.add_person("Godwin", "Gitonga", "staff")
        new_person_count = len(self.my_instance.people)
        self.assertEqual(new_person_count > initial_person_count, True)

    def test_add_staff_requesting_accommodation(self):
        """"test for staff addition to the dojo with request for accommodation. It """
        initial_person_count = len(self.my_instance.people)
        self.my_instance.add_person("Godwin", "Gitonga", "staff", "Y")
        output = sys.stdout.getvalue()
        self.assertIn("Staff cannot be allocated living spaces", output)
        new_person_count = len(self.my_instance.people)
        self.assertEqual(new_person_count > initial_person_count, True)

    def test_add_fellow(self):
        """"test for successful fellow addition to the dojo"""
        initial_person_count = len(self.my_instance.people)
        self.my_instance.add_person("Godwin", "Gitonga", "fellow", "Y")
        new_person_count = len(self.my_instance.people)
        self.assertEqual(new_person_count > initial_person_count, True)

    def test_add_fellow_with_similar_names(self):
        """"test for successful fellow addition to the dojo"""
        initial_person_count = len(self.my_instance.people)
        self.my_instance.add_person("Godwin", "Gitonga", "fellow", "Y")
        self.my_instance.add_person("Godwin", "Gitonga", "fellow", "Y")
        output = sys.stdout.getvalue()
        self.assertIn("1", output)
        self.assertIn("2", output)
        new_person_count = len(self.my_instance.people)
        self.assertEqual(new_person_count - initial_person_count, 2)

    def test_add_person_on_full_office(self):
        """test for addition of people when an office is full"""
        self.my_instance.create_room("office", "blue")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "staff")
        output = sys.stdout.getvalue()
        self.assertIn("unallocated office", output)

    def test_add_person_on_full_lspace(self):
        """test for addition of people when an living space is full"""
        self.my_instance.create_room("living_space", "pink")
        self.my_instance.add_person("godwin", "gitonga", "fellow", "Y")
        self.my_instance.add_person("godwin", "gitonga", "fellow", "Y")
        self.my_instance.add_person("godwin", "gitonga", "fellow", "Y")
        self.my_instance.add_person("godwin", "gitonga", "fellow", "Y")
        self.my_instance.add_person("godwin", "gitonga", "fellow", "Y")
        output = sys.stdout.getvalue()
        self.assertIn("unallocated living space", output)

    def test_auto_allocate_office(self):
        self.my_instance.add_person("godwin", "gitonga", "staff")
        self.assertIn("godwin gitonga", self.my_instance.office_allocations["unallocated"])
        self.my_instance.create_room("office", "blue")
        self.assertIn("godwin gitonga", self.my_instance.office_allocations["blue"])
        self.assertNotIn("godwin gitonga", self.my_instance.office_allocations["unallocated"])

    def test_auto_allocate_lspace(self):
        self.my_instance.create_room("office", "blue")
        self.my_instance.add_person("godwin", "gitonga", "fellow", "Y")
        self.assertIn("godwin gitonga", self.my_instance.living_space_allocations["unallocated"])
        self.my_instance.create_room("living_space", "white")
        self.assertIn("godwin gitonga", self.my_instance.living_space_allocations["white"])
        self.assertNotIn("godwin gitonga", self.my_instance.living_space_allocations["unallocated"])


    def test_print_room(self):
        """test for the printing a rooms occupants"""
        self.my_instance.create_room("office", "blue")
        self.my_instance.add_person("godwin", "gitonga", "staff")
        self.my_instance.print_room("blue")
        my_output = sys.stdout
        output = my_output.getvalue()
        self.assertIn("godwin gitonga", output)

    def test_print_non_existing_room(self):
        """test for the printing a non existing room"""
        self.my_instance.print_room("blue")
        my_output = sys.stdout
        output = my_output.getvalue()
        self.assertIn("room blue does not exist", output)

    def test_print_empty_room(self):
        """test for the printing a non existing room"""
        self.my_instance.create_room("office", "blue")
        output = self.my_instance.print_room("blue")
        self.assertIn("room blue is empty", output)

    def test_load_people(self):
        """test for loading people from a file"""
        initial_people_count = len(self.my_instance.people)
        output = self.my_instance.load_people("people.txt")
        self.assertIn("data loaded successfully", output)
        current_people_count = len(self.my_instance.people)
        self.assertEqual(current_people_count > initial_people_count, True)

    def test_load_people_from_unavailable_file(self):
        """test for loading people from a file that is not available"""
        initial_people_count = len(self.my_instance.people)
        output = self.my_instance.load_people("dummy.txt")
        self.assertIn("file not found", output)
        current_people_count = len(self.my_instance.people)
        self.assertEqual(current_people_count, initial_people_count)

    def test_print_with_no_allocations(self):
        """test for print allocations without people allocated"""
        my_output = self.my_instance.print_allocations()
        self.assertIn("no allocations to print", my_output)

    def test_print_allocations_on_file(self):
        """test for printing allocation on a file"""
        self.my_instance.create_room("office", "blue")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "fellow", "y")
        self.my_instance.print_allocations("allocations.txt")
        self.assertTrue(os.path.isfile("allocations.txt"))
        os.remove("allocations.txt")

    def test_print_allocations_on_screen(self):
        """test for displaying allocations"""
        self.my_instance.create_room("office", "blue")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "fellow", "y")
        self.my_instance.print_allocations()
        my_output = sys.stdout.getvalue()
        self.assertIn("martin white", my_output)

    def test_print_unallocated(self):
        """test for displaying unallocated people"""
        self.my_instance.create_room("office", "grey")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "fellow", "y")
        self.my_instance.print_unallocated()
        my_output = sys.stdout.getvalue()
        self.assertIn("martin", my_output)

    def test_print_unallocated_from_empty_list(self):
        """test for displaying unallocated people"""
        self.my_instance.create_room("office", "white")
        my_output = self.my_instance.print_unallocated()
        self.assertIn("no list of unallocated people", my_output)

    def test_print_unallocated_on_file(self):
        """test for printing unallocated people on a file"""
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "staff")
        self.my_instance.add_person("martin", "white", "fellow", "y")
        self.my_instance.add_person("martin", "white", "fellow", "y")
        self.my_instance.print_unallocated("unallocations.txt")
        self.assertTrue(os.path.isfile("unallocations.txt"))
        os.remove("unallocations.txt")

    def test_reallocate_office(self):
        """test for reallocation function"""
        self.my_instance.create_room("office", "blue")
        self.my_instance.add_person("Godwin", "Gitonga", "staff")
        self.assertEqual(len(self.my_instance.office_allocations["blue"]), 1)
        self.my_instance.create_room("office", "white")
        self.my_instance.reallocate_person(1, "white")
        self.assertEqual(len(self.my_instance.office_allocations["blue"]), 0)
        self.assertEqual(len(self.my_instance.office_allocations["white"]), 1)

    def test_reallocate_living_space(self):
        """test for reallocation function"""
        self.my_instance.create_room("living_space", "blue")
        self.my_instance.add_person("Godwin", "Gitonga", "fellow", "Y")
        self.assertEqual(len(self.my_instance.living_space_allocations["blue"]), 1)
        self.my_instance.create_room("living_space", "white")
        self.my_instance.reallocate_person(1, "white")
        self.assertEqual(len(self.my_instance.living_space_allocations["blue"]), 0)
        self.assertEqual(len(self.my_instance.living_space_allocations["white"]), 1)

    def test_reallocate_non_existing_person(self):
        self.my_instance.create_room("office", "blue")
        self.assertEqual(len(self.my_instance.office_allocations["blue"]), 0)
        self.my_instance.create_room("office", "white")
        output = self.my_instance.reallocate_person(1, "white")
        self.assertIn("person to reallocate doesn't exist", output)

    def test_reallocate_non_existing_room(self):
        self.my_instance.create_room("office", "blue")
        self.my_instance.add_person("Godwin", "Gitonga", "staff")
        self.assertEqual(len(self.my_instance.office_allocations["blue"]), 1)
        output = self.my_instance.reallocate_person(1, "white")
        self.assertIn("room not available for reallocation", output)

    def test_default_save_state(self):
        """test for storing the current state in the database"""
        self.my_instance.save_state()
        self.assertTrue(os.path.isfile('my_default_db.sqlite'))
        os.remove('my_default_db.sqlite')

    def test_save_state_with_filename(self):
        """test for storing the current state in the database"""
        self.my_instance.save_state("my_db")
        self.assertTrue(os.path.isfile('my_db.sqlite'))
        os.remove('my_db.sqlite')

    def test_content_in_db(self):
        db_name = "my_db"
        self.my_instance.create_room("office", "blue")
        self.my_instance.save_state(db_name)
        conn = sqlite3.connect(db_name+".sqlite")
        c = conn.cursor()
        query = "SELECT room_name FROM room"
        cursor = c.execute(query)
        last_id = cursor.fetchone()[0]
        self.assertIn(last_id, "blue")

    def test_load_state(self):
        """test for retrieving the current state from the database"""
        my_instance = Dojo()
        people_initial_list = len(my_instance.people)
        my_instance.load_state("alloc")
        people_new_list = len(my_instance.people)
        self.assertTrue(people_new_list > people_initial_list)

