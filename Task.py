import sc2

class Task :
    type = None
    id = None
    location = None
    upgrade = None

    def __init__(self, type, id, location, upgrade):
        self.type = type
        self.id = id
        self.location = location
        self.upgrade = upgrade
