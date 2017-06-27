import unittest
from unittest import TestCase

from person.person import Fellow, Staff, Person


class TestPerson(TestCase):
    def setUp(self):
        self.fellow = Fellow("godwin gitonga", 1)
        self.staff = Staff("mzee kijana", 2)

    def test_fellow(self):

        self.assertEqual(self.fellow.person_type, "fellow")
        self.assertEqual(self.fellow.person_number, 1)
        self.assertEqual(self.fellow.name, "godwin gitonga")
        self.assertEqual(issubclass(Fellow, Person), True)

    def test_staff(self):
        self.assertEqual(self.staff.person_type, "staff")
        self.assertEqual(self.staff.person_number, 2)
        self.assertEqual(self.staff.name, "mzee kijana")
        self.assertEqual(issubclass(Staff, Person), True)

    def test_for_not_implemeneted_error(self):
        self.assertRaises(NotImplementedError, Person, "Godwin Gitonga", 5)


if __name__ == '__main__':
    unittest.main()

