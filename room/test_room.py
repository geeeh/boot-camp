import unittest
from unittest import TestCase

from room.room import LivingSpace, Office, Room


class TestRoom(TestCase):
    def setUp(self):
        self.office = Office("kilimanjaro")
        self.living_space = LivingSpace("nyumbani")

    def test_office(self):
        self.assertEqual(self.office.capacity, 6)
        self.assertEqual(self.office.room_type, "office")
        self.assertEqual(self.office.room_name, "kilimanjaro")
        self.assertEqual(issubclass(Office, Room), True)

    def test_living_space(self):

        self.assertEqual(self.living_space.capacity, 4)
        self.assertEqual(self.living_space.room_type, "living_space")
        self.assertEqual(self.living_space.room_name, "nyumbani")
        self.assertEqual(issubclass(Office, Room), True)

    def test_for_not_implemented_error(self):
        self.assertRaises(NotImplementedError, Room, "blue")


if __name__ == '__main__':
    unittest.main()
