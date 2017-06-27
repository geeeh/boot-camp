class Person(object):
    """class to model an object person"""

    def __init__(self, person_name, person_number):
        if type(self) == Person:
            raise NotImplementedError("object cannot be instantiated directly")
        self.name = person_name
        self.person_number = person_number


class Staff(Person):
    """  class Staff that inherits from Person"""
    def __init__(self, person_name, person_number):
        self.person_type = "staff"
        Person.__init__(self, person_name, person_number)


class Fellow(Person):
    """class fellow inheriting from person"""
    def __init__(self, person_name, person_number):
       self.person_type = "fellow"
       Person.__init__(self, person_name, person_number)