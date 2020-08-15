import os
import random
import platform
import time
from Chapter_Two.exception_class import LocationError
import colorama

colorama.init()


# allows me to clear the screen when playing
def clear():
    operating = platform.system()
    if operating == "Linux" or operating == "Darwin":
        os.system("clear")
    elif operating == "Windows":
        os.system("cls")


# a fun little thing for sleeping. does nothing useful.
def simulation_faker():
    percent = 0
    progress = ""
    clear()
    while len(progress) < 11:
        print(f"Simulating world: [{progress:<10}] {percent}%")
        progress += "-"
        percent += 10
        time.sleep(0.5)
        clear()
    print("Finished Simulation")
    time.sleep(1)


# a class for picking random events
class RandomEvent:
    """A class to return random events."""

    def __init__(self, local_dict):
        self.local_dict = local_dict
        self.random_event_dict = {
            # town center random events
            "town center": [
                "A wagon races through the town.",
                "A young man trips and falls while distracted by a passing lady.",
                "A dog bark sets your fur on edge.",
            ],
            # town bar random events
            "bar": [
                "A glass is dropped and broken by an drunk patron.",
                "the bar tender wipes down the counter after a patron leaves.",
            ],
            # bath house random events
            "bath house": [
                "The pipe let out an odd groaning noise around you.",
                "The faint sound of water dripping echoes from the building.",
            ],
            # general store random events
            "general store": [
                "A young child tries to pick up some sweets, but her mother makes her put them back.",
                "A echo of moving material rumbles from the back rooms.",
                "The faint smell of smoked meat reminds you that you're hungry.",
            ],
            #
            "gate house": [
                "A guard taps his foot waiting for you say what you want.",
                "You see young children playing on the mansion front lawn.",
                "The large mansion gates creak eerily in the wind.",
            ],
            # ruins random events
            "ruined street": [
                "You spot a small rodent running across the street into some nearby bushes.",
                "A dog looks at you nervously before running off down the street.",
            ],
            "ruined office": [
                "The room creaks loudly, making you nervous.",
                "You hear the faint sound of water dripping somewhere in the room.",
            ],
            "ruined house": [
                "A large spider scuttles quickly across one of the walls,"
                "\ntaking refuge behind one of the curtains."
            ],
            "ruined garage": [
                "The scent of old oil and fuel hits your nose.",
                "You hear the sounds of something running around in the ceiling.",
            ],
            # garage upstairs random events
            "break room": [
                "A musty smell hits your nose, making you feel a little nauseous."
            ],
            "managers office": [],
            "balcony": ["A bird flys off into the distance."],
            # back rooms random events
            "weapons storage": [
                "The glint of sun light off chrome plated weapons momentarily blinds you."
            ],
            "work room": [],
            "freezer": [
                "You find yourself salivating at the smell of smoked fish.",
                "The scent of smoked ham has you feeling hungry.",
                "Your nose is overwhelmed by the scent of smoked cheese.",
            ],
            "general storage": ["The cobwebs blow slightly in the dusty breeze."],
            # tower rooms random events
            "tower entrance": [],
            "tower peak": [
                "It strikes you how lovely the surrounding mansion grounds look from up here.",
                "The organ's pipes seem to stretch for miles downward. Such an impressive instrument.",
            ],
            # mansion rooms and actions
            "foyer": [
                "A butler greets you politely as you walk in.",
                "A maid gives the furniture in the room a clean with a duster.",
            ],
            "sun room": [
                "The warmth from the sunlight makes you feel cozy.",
                "Your eyes adjust to the sudden change in brightness as you walk in.",
            ],
            "hallway": [
                "A cleaner walks by with a mop and bucket.",
                "A nanny smiles at you as she passes by with two young children in tow.",
            ],
            "kitchen": [
                "The smells coming from within the kitchen have you looking forward to a nice meal."
            ],
            "living room": [],
            # garden rooms random events
            # "garden entrance": [],
            # inn rooms random events
            "inn entrance": [],
            "inn room": [
                "The windows shake in the wind. Though you would swear there's no wind to cause it.",
                "Whispers seem to echo from the closet but when you try to listen they stop.",
            ],
            # cellar rooms random events
            "cellar entrance": [],
            "wine casks": [
                "You notice how some of the casks seem to be newer than the rest.",
                "The amount of spider webs down here creep you out.",
            ],
            "lab": ["Beakers and bottles bubble all around you."],
        }

    def grab_event(self, player_location):
        # if the random number is between my range then it runs a random event
        rand_num = random.randint(0, 100)
        if 0 <= rand_num <= 15:
            location_library = self.random_event_dict.get(player_location)
            if location_library:
                return random.choice(location_library)
            # it should never return a None
            elif location_library is None:
                raise LocationError(player_location)
            else:
                return False
        else:
            return False


# function class for inheritance
class FunctionClass:
    """Never to be called. Only used for giving all other classes the same methods."""

    # class variables for print formatting
    bold = colorama.Style.BRIGHT
    end = colorama.Style.NORMAL
    look_at_remarks = ("I can't look at the {0}.", "What {0}?")
    oper_remarks = ("I can't operate the {0}.", "How would I operate the {0}?")
    go_to_remarks = ("I can't go to {0}.", "Where is {0}?")
    use_remarks = ("What is a(n) {0}.", "I can't do anything to the {0}")
    get_remarks = ("There isn't a(n) {0} to get.", "I can't find a(n) {0} to pick up.")
    drop_remarks = (
        "I don't have a(n) {0} to drop.",
        "I would need to have a(n) {0} to drop it.",
    )

    # allows getting a print function form the look dictionary.
    def get_look_commands(self, look_at):
        # you have to enter at least three letters
        if len(look_at) >= 3:
            for key in self.look_dict:
                if look_at in key:
                    look_command = self.look_dict.get(key)
                    look_command()
                    break
            else:
                self.print_random_phrase(self.look_at_remarks, look_at)

        else:
            self.print_random_phrase(self.look_at_remarks, look_at)

    # allows getting operate commands
    def get_oper_commands(self, operate):
        # you have to enter at least three letters
        if len(operate) >= 3:
            for key in self.oper_dict:
                if operate in key:
                    oper_command = self.oper_dict.get(key)
                    oper_command()
                    break
            else:
                self.print_random_phrase(self.oper_remarks, operate)
        else:
            self.print_random_phrase(self.oper_remarks, operate)

    # allows getting go commands
    def get_go_commands(self, go):
        # you have to enter at least three letters
        if len(go) >= 2:
            for key in self.go_dict:
                if go in key:
                    go_command = self.go_dict.get(key)
                    go_command()
                    break
            else:
                self.print_random_phrase(self.go_to_remarks, go)
        else:
            self.print_random_phrase(self.go_to_remarks, go)
        # allows using item on objects

    def get_use_commands(self, use_list):
        item = use_list[0]
        room_object = use_list[1]
        # you have to enter at least three letters
        if item in self.player_object.inventory:
            if len(room_object) >= 3:
                for key in self.use_dict:
                    if room_object in key:
                        use_command = self.use_dict.get(key)
                        use_command(item)
                        break
                else:
                    print(f"I can't find the {room_object}.")
            else:
                print(f"What is a(n) {room_object}.")
        else:
            print(f"I don't have a(n) {item}.")

    # gives item to player
    def get_item(self, item):
        if item in self.inventory:
            print(f"I got the {self.bold + item + self.end}.")
            self.inventory.remove(item)
            self.player_object.inventory.append(item)
        else:
            self.print_random_phrase(self.get_remarks, item)

    # dropping item back into room
    def drop_item(self, item):
        if item in self.player_object.inventory and item != "map":
            print(f"I dropped the {self.bold + item + self.end}.")
            self.inventory.append(item)
            self.player_object.inventory.remove(item)
        else:
            self.print_random_phrase(self.drop_remarks, item)

    # prints items and bolds them for effect.
    def print_items(self):
        if len(self.inventory) > 0:
            for item in self.inventory:
                print(f"There is a(n) ", end="")
                print(self.bold, item, self.end)

    # prints what you can look at
    def print_look(self):
        look_list = ""
        print("I could look at...")
        for thing in self.look_dict:
            look_list += f"'{self.bold+ thing+ self.end}', "
        print(look_list)
        print("_" * len(look_list))

    # prints where you can go
    def print_locations(self):
        go_list = ""
        print("I could go to...")
        for location in self.go_dict:
            go_list += f"'{self.bold+ location+ self.end}', "
        print(go_list)
        if self.inventory:
            print("_" * len(go_list))

    @staticmethod
    def print_random_phrase(selection_list, item):
        rand_phrase = random.choice(selection_list)
        print(rand_phrase.format(item))


# town center rooms
class TownCenter(FunctionClass):
    """Starting room and center of town."""

    def __init__(self, player_object, timer):

        self.inventory = []
        self.clock = timer
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "bar": self.go_bar,
            "general store": self.go_gen_store,
            "gate house": self.go_gate_house,
            "bath house": self.go_bath_house,
            "ruined street": self.go_ruined_street,
            "town inn": self.go_inn_entrance,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You arrive in the town center. It is a small yet bustling town full of people going about their day."
            "\nThe streets are lined with shops and stalls selling various goods, from basic food items"
            "\nto useful supplies for a traveller like yourself. A fountain sits in the middle of the center,"
            "\nits water glimmers in the daylight."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_bar(self):
        self.player.location = "bar"

    def go_gen_store(self):
        if 2000 <= self.clock.timer <= 2500 or 0 <= self.clock.timer <= 800:
            print("It's closed for the night. It will open at 8:00 AM.")
        else:
            self.player.location = "general store"

    def go_gate_house(self):
        self.player.location = "gate house"

    def go_bath_house(self):
        self.player.location = "bath house"

    def go_ruined_street(self):
        self.player.location = "ruined street"

    def go_inn_entrance(self):
        self.player.location = "inn entrance"


class TownBar(FunctionClass):
    """Bar that acts as a shop and a meeting place."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"town center": self.go_town_center}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk into the town bar. It is a small yet cozy feeling bar. The walls are lined with"
            "\nmemorabilia from the old world, as well as signs with names you don't recognize."
            "\nThere are several patrons sitting at the bar, some of whom would appear to have spent the"
            "\nwhole day drinking. A band is playing some soft folk music in the corner, and the smell of"
            "\nbeer and tobacco fills the air."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_town_center(self):
        self.player.location = "town center"


class TownGenStore(FunctionClass):
    """town general store that acts as a shop and a puzzle hub."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"town center": self.go_town_center}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk into the town's general store. The shop is full of shelves stocked with various items ranging"
            "\nfrom weapons and ammunition, to medical supplies and food items. A lioness sits at the counter,"
            "\nyou find her to be rather cute."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_shop(self):
        print("It's a nice General store.", end=" ")
        if len(self.shop_inventory) > 0:
            print("Looks like there are things to buy.")
        else:
            print("She's all sold out of things I'd want.")

    def go_town_center(self):
        self.player.location = "town center"


class TownBathHouse(FunctionClass):
    """town bath house that acts as a small puzzle for getting cleaned up."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"town center": self.go_town_center}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("You walk into the bath house. What was once a relic of the past in the old world has become a part"
              "\nof common life in the current world. The building is full of people waiting for a chance to clean"
              "\nthemselves up.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_town_center(self):
        self.player.location = "town center"


class TownGateHouse(FunctionClass):
    """town gate house that allows or denies entry to mansion."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "town center": self.go_town_center,
            "mansion": self.go_mansion_foyer,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The town center gate house.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_town_center(self):
        self.player.location = "town center"

    def go_mansion_foyer(self):
        self.player.location = "foyer"


# Ruined City rooms
class RuinedHouse(FunctionClass):
    """A ruined house in the city."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"ruined street": self.go_ruined_street}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("You walked into a ruined house. What was once a man's castle is now a ransacked shell of it's former"
              "\nglory. The furniture within has been tossed around with reckless abandon, the walls are mildewed"
              "\nand crumbling. Bits of glass and broken crockery cover the floor, among various other possessions"
              "\nfrom the previous owner.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_ruined_street(self):
        self.player.location = "ruined street"


class RuinedStreet(FunctionClass):
    """The main street of the ruined city."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.office_opened, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "town center": self.go_town_center,
            "ruined house": self.go_ruined_house,
            "ruined garage": self.go_ruined_garage,
            "ruined office": self.go_ruined_office,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("You arrive at a ruined street. You find yourself surrounded by buildings in various states of disrepair,"
              "\nsome of which you think would crumble at the force of a gentle breeze. The road surface is badly"
              "\nbroken up badly and burnt out and rusted cars dot the rest of the street, along with all  manner"
              "\nof rubble and shrapnel that would cut up your delicate paws if you're not careful.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_town_center(self):
        self.player.location = "town center"

    def go_ruined_house(self):
        self.player.location = "ruined house"

    def go_ruined_garage(self):
        self.player.location = "ruined garage"

    def go_ruined_office(self):
        if not self.office_opened:
            print("It's blocked. I'll have to figure out how to clear it first.")
        else:
            self.player.location = "ruined office"


class RuinedOffice(FunctionClass):
    """A ruined office building in the city."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"ruined street": self.go_ruined_street}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk into the ruined office. The building has collapsed somewhat, having turned into something of"
            "\na manmade cave. The atmosphere of the room makes you nervous about it's structural integrity."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_ruined_street(self):
        self.player.location = "ruined street"


class RuinedGarage(FunctionClass):
    """An old garage in the ruined city."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "ruined street": self.go_ruined_street,
            "upstairs": self.go_upstairs_break_room,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk into the garage.What was once a thriving automotive workshop has become a time capsule"
            "\nof the past. By the front roller door sits a car riddled with bullet holes, suggesting that"
            "\nwhoever owned the business did whatever they could to protect their investment. At the back of"
            "\nthe workshop sits a much more well preserved car, aside from the engine bay being empty"
            "\nand small rust spots appearing around the windows. The walls are adorned with banners advertising"
            "\nbrands the shop stocked, as well as some old car parts and tool cabinets. The floor is strewn"
            "\nwith empty boxes, tools, bottles and parts. The smell of stale fuel lingers in the air."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_ruined_street(self):
        self.player.location = "ruined street"

    def go_upstairs_break_room(self):
        self.player.location = "break room"


# Garage Upstairs
class UpstairsBreakRoom(FunctionClass):
    """An upstairs break room in the garage."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "ruined garage": self.go_ruined_garage,
            "office": self.go_upstairs_office,
            "balcony": self.go_upstairs_balcony,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk in to the break room of the garage. There is a table and chairs in the middle of the room."
            "\nIn one corner is a sink with an old water cooler next to it. In the other corner sits a refrigerator"
            "\nwith a bench next to it, with an old microwave and some crockery and cutlery."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_ruined_garage(self):
        self.player.location = "ruined garage"

    def go_upstairs_office(self):
        self.player.location = "managers office"

    def go_upstairs_balcony(self):
        self.player.location = "balcony"


class UpstairsBalcony(FunctionClass):
    """An upstairs balcony that overlooks the city street."""

    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "break room": self.go_upstairs_break_room,
            "office": self.go_upstairs_office,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk on to the garage's balcony. You find yourself overlooking the ruined street. There is a table"
            "\nand chairs with a small ashtray in the middle of the table. In the corner is a now dead pot plant."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_upstairs_break_room(self):
        self.player.location = "break room"

    def go_upstairs_office(self):
        self.player.location = "managers office"


class UpstairsOffice(FunctionClass):
    """An upstairs office in the garage."""

    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)

        self.shop_inventory = []
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "break room": self.go_upstairs_break_room,
            "balcony": self.go_upstairs_balcony,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk into the manager's office of the garage. It would appear the place had been ransacked by the"
            "\nscavengers you scared off. Various documents are strewn across the floor, mostly sales records"
            "\nand maintenance records for the courtesy cars the shop once owned. A broken computer sits on the"
            "\ndesk along with an ashtray and a diary. In the corner sits a large safe."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_upstairs_break_room(self):
        self.player.location = "break room"

    def go_upstairs_balcony(self):
        self.player.location = "balcony"


# mansion rooms
class MansionFoyer(FunctionClass):
    """The entrance to the mansion."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "gate house": self.go_gate_house,
            "kitchen": self.go_mansion_kitchen,
            "hallway": self.go_mansion_hallway,
            "sun room": self.go_mansion_sun_room,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk into the mansion's foyer. It's apparent that the owner is well off, judging by the immaculate"
            "\nmarble floor and chandelier hanging from the ceiling. The walls are adorned with paintings of the"
            "\nowner's family, as well as some vintage paintings from the old world."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_gate_house(self):
        self.player.location = "gate house"

    def go_mansion_kitchen(self):
        self.player.location = "kitchen"

    def go_mansion_hallway(self):
        self.player.location = "hallway"

    def go_mansion_sun_room(self):
        self.player.location = "sun room"


class MansionSunRoom(FunctionClass):
    """A warm sun room in the house."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "foyer": self.go_mansion_foyer,
            "tower entrance": self.go_tower_entrance,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The mansion sun room.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_mansion_foyer(self):
        self.player.location = "foyer"

    def go_tower_entrance(self):
        self.player.location = "tower entrance"


class MansionKitchen(FunctionClass):
    """A kitchen in the mansion."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "foyer": self.go_mansion_foyer,
            "cellar": self.go_cellar_entrance,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The mansion kitchen.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_mansion_foyer(self):
        self.player.location = "foyer"

    def go_cellar_entrance(self):
        self.player.location = "cellar entrance"


class MansionHallWay(FunctionClass):
    """A hallway in the mansion."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "foyer": self.go_mansion_foyer,
            "living room": self.go_mansion_living_room,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The mansion hallway.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_mansion_foyer(self):
        self.player.location = "foyer"

    def go_mansion_living_room(self):
        self.player.location = "living room"


class MansionLivingRoom(FunctionClass):
    """A living room in the mansion."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"hallway": self.go_mansion_hallway}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The mansion foyer.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_mansion_hallway(self):
        self.player.location = "hallway"


# tower rooms
class TowerEntrance(FunctionClass):
    """The entrance to the mansion tower."""

    def __init__(self, player_object):

        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "tower peak": self.go_tower_peak,
            "hallway": self.go_mansion_sun_room,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The tower entrance.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_mansion_sun_room(self):
        self.player.location = "sun room"

    def go_tower_peak(self):
        self.player.location = "tower peak"


class TowerPeak(FunctionClass):
    """The top of the mansion tower."""

    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"tower peak": self.go_tower_entrance}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The tower entrance.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_tower_entrance(self):
        self.player.location = "tower entrance"


# cellar rooms
class CellarEntrance(FunctionClass):
    """Entrance to cellar of mansion."""

    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "mansion": self.go_mansion_kitchen,
            "wine casks": self.go_wine_casks,
            "lab": self.go_lab,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The cellar entrance.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_mansion_kitchen(self):
        self.player.location = "kitchen"

    def go_wine_casks(self):
        self.player.location = "wine casks"

    def go_lab(self):
        self.player.location = "lab"


class CellarWineCasks(FunctionClass):
    """Wine Casks in cellar of mansion."""

    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"cellar entrance": self.go_cellar_entrance}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The cellar wine casks.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_cellar_entrance(self):
        self.player.location = "cellar entrance"


class CellarLab(FunctionClass):
    """Secret lab in cellar of mansion."""

    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"cellar entrance": self.go_cellar_entrance}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The cellar secret lab.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_cellar_entrance(self):
        self.player.location = "cellar entrance"


# the general store's back rooms
class GeneralStorage(FunctionClass):
    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "general store": self.go_general_store,
            "work room": self.go_work_room,
            "freezer": self.go_freezer,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The General Store's storage.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_general_store(self):
        self.player.location = "general store"

    def go_work_room(self):
        self.player.location = "work room"

    def go_freezer(self):
        self.player.location = "freezer"


class WeaponsStorage(FunctionClass):
    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {"work room": self.go_work_room}
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk into the general store's weapon storage room. All around you are various types of firearms,"
            "\nneatly stored on racks that cover both walls. On the floor are various ammo boxes, some of which"
            "\nyou recognize from your days in the military."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_work_room(self):
        self.player.location = "work room"


class WorkRoom(FunctionClass):
    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "weapon storage": self.go_weapon_storage,
            "general storage": self.go_general_storage,
            "freezer": self.go_freezer,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The General Store's work room.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_weapon_storage(self):
        self.player.location = "weapons storage"

    def go_general_storage(self):
        self.player.location = "general storage"

    def go_freezer(self):
        self.player.location = "freezer"


class Freezer(FunctionClass):
    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "general storage": self.go_general_storage,
            "work room": self.go_work_room,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print(
            "You walk into the general store's freezer. Once used to keep perishable items cold, it has been"
            "\nconverted into a smoking room. On the ceiling hangs some hooks, holding meats such as ham, pork"
            "\nand several types of smoked fish. On one of the walls is a group of shelves where various types of"
            "\njerky and peppers are drying out, and on another wall is shelves stocked with smoked cheeses."
        )
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_general_storage(self):
        self.player.location = "general storage"

    def go_work_room(self):
        self.player.location = "work room"


# towns inn locations
class InnEntrance(FunctionClass):
    def __init__(self, player_object):
        self.inventory = []
        self.player = player_object
        self.room_rented = False
        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {"room": self.print_description_room}
        self.go_dict = {
            "town center": self.go_town_center,
            "inn room": self.go_inn_room,
        }
        self.oper_dict = {}
        self.use_dict = {}

    def print_description_room(self):
        print("The inns entrance.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def go_town_center(self):
        self.player.location = "town center"

    def go_inn_room(self):
        if not self.room_rented:
            print("I should rent the room first.")
        else:
            self.player.location = "inn room"


class InnRoom(FunctionClass):
    def __init__(self, player_object, timer):
        self.inventory = []
        self.clock = timer
        self.player = player_object

        # ghost quest stuff
        self.ghost_found = False
        self.ghost_solved = False

        self.bool_one, self.bool_two, self.bool_three = (False, False, False)
        self.look_dict = {
            "room": self.print_description_room,
            "bed": self.print_description_bed,
        }
        self.go_dict = {"inn lobby": self.go_inn_entrance}
        self.oper_dict = {"bed": self.operate_inn_bed}
        self.use_dict = {}

    def print_description_room(self):
        print("The inn's bed room you rented.")
        print("__________________")
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_bed(self):
        print("A lion like me does need lots of naps.")
        if self.ghost_found and not self.ghost_solved:
            print("I still need to figure out what that spirit needed.")
        else:
            print("I hope I don't run into anything else ghostly.")

    def operate_inn_bed(self):
        if self.clock.timer >= 1800 or self.clock.timer <= 700:
            print("It's time for a good sleep.")
            time.sleep(2)
            sleep_action = self.random_sleep_event()
            sleep_action()
            self.player.sleep = True
        else:
            print("It's too early to go to bed right now.")

    def go_inn_entrance(self):
        self.player.location = "inn entrance"

    # TO DO: will allow random events to play when sleeping
    def random_sleep_event(self):
        rand_num = random.randint(0, 100)
        if not self.ghost_found:
            # find ghost function
            return self.find_ghost
        elif "some item" in self.player.inventory:
            # solve ghost puzzle function
            return self.solve_ghost
        # ten percent chance to happen
        elif 0 <= rand_num < 10:
            return simulation_faker
        # ten percent chance to happen
        elif 10 <= rand_num < 20:
            return simulation_faker
        # five percent chance to happen
        elif 20 <= rand_num < 25:
            return simulation_faker
        else:
            return simulation_faker

    def solve_ghost(self):
        self.ghost_solved = True
        print("Ghost solve puzzle here.")

    def find_ghost(self):
        self.ghost_found = True
        print("Please, listen to me. A voice echos to you as you lay in bed.")
        time.sleep(0.5)
        clear()
        print(
            "I need you to find my lost family's heirloom."
            "\nIt's a white mostly see through spirit, your heart races in your chest."
        )
        time.sleep(0.5)
        clear()
        print(
            "Please... Search my office..."
            "\nThe spirit fades away and you are left wondering if you really did hear what you thought you did."
        )
