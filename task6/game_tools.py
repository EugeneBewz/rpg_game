"""
Game assets: characters, districts, items
"""


# import random


# * Items ==============================================================================================================
class Item:
    """
    Contains data about useful tools, which will help MC
    to achieve their goal
    """
    def __init__(self, item_name: str, item_description: str, damage: int = 0):
        self.item_name = item_name
        self.item_description = item_description

        self.damage = damage

    def set_item_damage(self, damage_amount: int):
        """
        If you create a weapon for hostile NPCs,
        give item its damage and make MC value his life
        """
        self.damage = damage_amount


# * NPCs ===============================================================================================================
class NPC:
    """
    Contains data about NPC in general
    """
    def __init__(self, npc_name: str, npc_description: str, npc_health: int = 3):
        self.npc_name = npc_name
        self.npc_description = npc_description
        self.npc_health = npc_health

        self.dialogue = "..."

        self.npc_equipment = None

    def set_dialogue(self, character_dialogue: str):
        """
        Set a dialogue for character in order to be able
        to have a conversation with characters
        """
        self.dialogue = character_dialogue

    def set_npc_equipment(self, equipment: Item | None):
        """
        Give NPC something to possess. It can be either
        weapon or buffs for MC.
        """
        self.npc_equipment = equipment

    def talk(self):
        """
        Allow character to speak and mock your MC.

        >>> stan = NPC("Stan", "Local barman")
        >>> stan.set_dialogue("Back off! You don't drink today: I'm so sick of you!")
        >>> stan.talk()
        "Stan says: Back off! You don't drink today: I'm so sick of you!"
        """
        return print(f"{self.npc_name} says: {self.dialogue}")


# ! Friendly NPCs (Allies) ===========================================
class Friendly(NPC):
    """
    Contains data about friendly NPCs - they will
    grant MC buffs and items.

    >>> stan = Friendly("Stan", "Local barman")
    >>> stan.set_dialogue("Be careful: they're already there...")
    >>> stan.talk()
    "Stan says: Be careful: they're already there..."
    """
    def __init__(self, npc_name: str, npc_description: str, npc_health: int = 3):
        super().__init__(npc_name, npc_description, npc_health)
        self.available_buff = None
        # self.buff_id = 0

    def set_buff(self, buff: str):
        """
        Give character buffs he can transfer to MC
        """
        self.available_buff = buff

    def give_buff(self) -> int:
        """
        Give MC buffs and let him taste his last moments of peaceful life.
        There are the types of buffs: add lives, give items or reduce
        hostile health.
        Returns a buff "id", which represents every possible buff.
        """
        # if self.available_buff == "heal":
        #     return 1
        if self.available_buff == "gift":
            return 1
        elif self.available_buff == "weaken enemies":
            return 2
        else:
            return 0


# ! Hostile NPC (Mobs) ===============================================
class Hostile(NPC):
    """
    Contains data about hostile NPC - they will
    try to make MC suffer defeat at any cost.
    """
    def __init__(self, npc_name: str, npc_description: str, npc_health: int = 3):
        super().__init__(npc_name, npc_description, npc_health)
        self.npc_equipment = None

        self.npc_weakness = None
        self.npc_resistance = None

    def set_weakness(self, weakness: str):
        """
        Give a hostile NPC a weakness. If MC possesses such item,
        its damage changes by +1
        """
        self.npc_weakness = weakness

    def set_resistance(self, resistance: str):
        """
        Give a hostile NPC a resistance. If MC possesses such item,
        its damage changes by -1
        """
        self.npc_resistance = resistance

    def fight(self, item: Item) -> bool:
        """
        Fight with hostile NPC. Return True if MC achieves victory,
        else return False and die

        >>> loc_item = Item("sword", "A weapon of noble hero", 3)
        >>> bad_npc = Hostile("Mal", "An evil duke of forests", 3)
        >>> bad_npc.fight(loc_item)
        True
        >>> loc_item = Item("sword", "A weapon of noble hero", 3)
        >>> bad_npc = Hostile("Mal", "An evil duke of forests", 5)
        >>> bad_npc.fight(loc_item)
        False
        """
        if item.damage >= self.npc_health:
            return True
        return False


class Bargainer(NPC):
    """
    Bargainer - main goal of MC. MC has to buy souvenir from him.
    Bargainer can ask for items or renown
    """
    def __init__(self, npc_name: str, npc_description: str):
        super().__init__(npc_name, npc_description)

    def bargain(self, mc_renown: int = 0) -> int:
        """
        Trade with bargainer. Each renown point gives MC a -1 discount.
        The more MC possesses, the less they'll have to pay. If MC has defeated
        every enemy on a map, bargainer will give souvenir for free.
        """
        if mc_renown == 3:
            return 0
        elif mc_renown == 2:
            return 1
        elif mc_renown == 1:
            return 2
        elif mc_renown == 0:
            return 3


# * Town districts =====================================================================================================
class District:
    """
    Town district. Contains its name, data about
    items and inhabitants.
    """
    visits = 0

    def __init__(self, district_name: str):
        self.district_name = district_name
        self.district_description = None

        self.north_district = None
        self.south_district = None
        self.west_district = None
        self.east_district = None

        self.local_hostile_npc = None
        self.local_friendly_npc = None

        self.local_item = None

    def set_description(self, district_description: str):
        self.district_description = district_description

    def build_road_between_districts(self, destination_district, direction: str):
        """
        Connect two separate districts with a road in order to allow MС
        travelling through them.
        """
        if direction == "north":
            self.north_district = destination_district
        elif direction == "south":
            self.south_district = destination_district
        if direction == "west":
            self.west_district = destination_district
        if direction == "east":
            self.east_district = destination_district

    def set_local_item(self, item: Item | None):
        """
        Put an item in district and allow user to take it
        """
        self.local_item = item

    def set_local_hostile_npc(self, npc: Hostile | None):
        """
        Place a hostile mob here and make MC sweat
        """
        self.local_hostile_npc = npc

    def set_local_friendly_npc(self, npc: Bargainer | Friendly):
        """
        Place a friendly NPC here or hopeless MC will die
        """
        self.local_friendly_npc = npc

    def get_local_hostile_npc(self) -> Hostile | None:
        """
        Return a hostile mob of current location
        """
        return self.local_hostile_npc

    def get_local_friendly_npc(self) -> Bargainer | Friendly | None:
        """
        Return a friendly NPC of current location
        """
        return self.local_friendly_npc

    def get_local_item(self) -> Item:
        """
        Return an item if current location
        """
        return self.local_item.item_name

    def get_district_info(self):
        """
        Return general info about current district
        """
        # * Basic info ====================================
        print(f"{self.district_name}.")
        print("-------------------------------------------")
        print(f"{self.district_description}")

        if self.north_district:
            print(f"{self.north_district.district_name} is north.")
        if self.south_district:
            print(f"{self.south_district.district_name} is south.")
        if self.west_district:
            print(f"{self.west_district.district_name} is west.")
        if self.east_district:
            print(f"{self.east_district.district_name} is east.")

        # * Local inhabitants ==============================
        if self.local_hostile_npc:
            print(f"District belongs to {self.local_hostile_npc.npc_name}, they're hostile")
        if self.local_friendly_npc:
            print(f"{self.local_friendly_npc.npc_name} lives here, they're friendly")
        # * Items ==========================================
        if self.local_item:
            print(f"You noticed a/an {self.local_item.item_name}.")

    def travel(self, direction: str):
        """
        Travel between districts and discover who else wishes
        to beat the crap out of MC.
        """
        if direction == "north":
            return self.north_district
        elif direction == "south":
            return self.south_district
        elif direction == "west":
            return self.west_district
        elif direction == "east":
            return self.east_district

    def visit_district(self) -> int:
        """
        Mark the number of current district visits
        """
        District.visits += 1
        return District.visits


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
