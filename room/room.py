class Room(object):
    """class to model object room"""

    def __init__(self, room_name):
        if type(self) == Room:
            raise NotImplementedError("object cannot be instantiated directly")
        self.room_name = room_name


class Office(Room):
    """ class office extending Room class"""
    def __init__(self, room_name):
        self.room_type = "office"
        self.capacity = 6
        Room.__init__(self, room_name)


class LivingSpace(Room):
    """class Living_space extending Room class"""
    def __init__(self, room_name):
        self.room_type = "living_space"
        self.capacity = 4
        Room.__init__(self, room_name)