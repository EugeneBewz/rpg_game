"""
RPG game
"""


# * Character classes ==================================================================================================
class Character:
    """
    Allows user to create a character
    """
    defeats = 0

    def __init__(self, name: str, character_description: str):
        self.name = name
        self.character = character_description
        self.phrase = None
        self.weakness = None

    def set_conversation(self, phrase: str):
        self.phrase = phrase

    def set_weakness(self, weakness: str):
        self.weakness = weakness

    def describe(self):
        """
        Describe NPCs in the room
        """
        if self.character:
            print(f"{self.name} is here!")
            print(f"{self.character}")

    def talk(self):
        """
        Talk with a character
        """
        return print(f"[{self.name} says]: {self.phrase}.")

    def fight(self, mc_equipment: str) -> bool:
        """
        Fight with this character
        """
        if mc_equipment == self.weakness:
            # self.defeats += 1
            return True
        return False

    def get_defeated(self) -> int:
        Character.defeats += 1
        return Character.defeats


class Enemy(Character):
    """
    Create an enemy based on a character attributes
    """
    def __init__(self, name: str, enemy_description: str):
        super().__init__(name, enemy_description)
        self.phrase = None
        self.weakness = None


class Ally(Character):
    """
    Create an ally based on a character attributes
    """
    def __init__(self, name: str, ally_description: str):
        super().__init__(name, ally_description)


# * Item class =========================================================================================================
class Item:
    """
    Create a usable item
    """
    def __init__(self, name: str):
        self.name = name
        self.description = None

    def set_description(self, description: str):
        """
        Set description to an item
        """
        self.description = description

    def describe(self):
        """
        Describe an item in the room
        """
        if not self.description:
            print(f"The [{self.name}] is here.")
        else:
            print(f"The [{self.name}] is here - {self.description}.")

    def get_name(self):
        """
        Get a name of an item
        """
        return self.name


# * Room class =========================================================================================================
class Room:
    """
    Allow user to generate a room
    """
    def __init__(self, name: str):
        # * Basic description ==========================================================================================
        self.name = name
        self.description = None

        self.character = None

        self.enemy_in_the_room = None
        self.item_in_the_room = None
        self.inhabitant = None

        # * Rooms ======================================================================================================
        self.north_room = None
        self.south_room = None
        self.west_room = None
        self.east_room = None
        # self.linked_rooms = {}

    def set_description(self, description: str):
        """
        Add a description to the room

        >>> kitchen = Room("Kitchen")
        >>> kitchen.set_description("A dank and dirty room buzzing with flies.")
        >>> print(kitchen.description)
        A dank and dirty room buzzing with flies.
        """
        self.description = description

    def link_room(self, room, side: str):
        """
        Link a room to the current room

        >>> current_room = Room("Kitchen")
        >>> bathroom = Room("Bathroom")
        >>> current_room.link_room(bathroom, "south")
        >>> assert(current_room.south_room == bathroom)
        """
        if side == "north":
            self.north_room = room
        if side == "south":
            self.south_room = room
        if side == "west":
            self.west_room = room
        if side == "east":
            self.north_room = room

    def set_character(self, character: Character | Enemy | Ally):
        """
        Put a character inside a room
        """
        self.character = character

    def set_item(self, item: Item):
        """
        Put an item inside a room
        """
        self.item_in_the_room = item

    def get_character(self):
        """
        Get a character from a room
        """
        return self.character

    def get_item(self):
        """
        Get an item from a room
        """
        return self.item_in_the_room

    def get_details(self):
        """
        Return user a description of the room
        containing information about it, items and
        inhabitants.
        """
        # * Name and description =======================================================================================
        print(f"{self.name}")
        print("--------------------")
        if self.description:
            print(f"{self.description}")
        # * Linked rooms ===============================================================================================
        if self.north_room:
            print(f"{self.north_room.name} is north")
        if self.south_room:
            print(f"{self.south_room.name} is south")
        if self.west_room:
            print(f"{self.west_room.name} is west")
        if self.east_room:
            print(f"{self.east_room.name} is east")

    def move(self, direction: str):
        """
        Move character to another room

        >>> current_room = Room("Kitchen")
        >>> throne_room = Room("Throne Room")
        >>> current_room.link_room(throne_room, "north")
        >>> new_current_room = current_room.move("north")
        >>> assert(new_current_room.name == "Throne Room")
        """
        if direction == "north":
            return self.north_room
        elif direction == "south":
            return self.south_room
        elif direction == "west":
            return self.west_room
        else:
            return self.east_room


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
