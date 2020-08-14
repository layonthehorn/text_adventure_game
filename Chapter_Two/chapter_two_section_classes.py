import time
import pprint
import random
import Chapter_Two.chapter_two_room_classes as rooms
import Chapter_Two.chapter_two_npc_classes as npc
from Chapter_Two.exception_class import (
    LocationError,
    NPCLocationError,
    ChangeSectionError,
    RedundantMoveError,
    MapMatchError,
)
import colorama

colorama.init()


# Player Class
class PlayerClass:
    """This is the main player class. It holds the player inventory and score among other things."""

    # class variables for print formatting
    bold = colorama.Style.BRIGHT
    end = colorama.Style.NORMAL

    # dictionaries used for formatting the maps
    map_dict = {
        "inn": {"IE": "inn entrance", "IR": "inn room"},
        "town": {
            "TC": "town center",
            "TB": "bar",
            "GS": "general store",
            "BH": "bath house",
            "GH": "gate house",
        },
        "ruins": {
            "RH": "ruined house",
            "RG": "ruined garage",
            "RO": "ruined office",
            "RS": "ruined street",
        },
        "tower": {"TP": "tower peak", "TE": "tower entrance"},
        "mansion": {
            "MF": "foyer",
            "MK": "kitchen",
            "HW": "hallway",
            "SR": "sun room",
            "LR": "living room",
        },
        "gardens": {},
        "cellar": {"LB": "lab", "WC": "wine casks", "CE": "cellar entrance"},
        "gen back rooms": {
            "WR": "work room",
            "FR": "freezer",
            "WS": "weapon storage",
            "GS": "general storage",
        },
        "upstairs": {"BR": "break room", "MO": "manager office", "GB": "balcony",},
    }

    # accepted locations where you can go
    accepted_locations = (
        "end",
        "exit",
        "town center",
        "general store",
        "gate house",
        "bath house",
        "bar",
        "ruined street",
        "ruined office",
        "ruined house",
        "ruined garage",
        "kitchen",
        "foyer",
        "sun room",
        "living room",
        "hallway",
        "tower entrance",
        "tower peak",
        "cellar entrance",
        "wine casks",
        "lab",
        "manager office",
        "break room",
        "balcony",
        "weapon storage",
        "work room",
        "general storage",
        "freezer",
        "inn entrance",
        "inn room",
    )
    # sections of the map, changes how your map looks.
    accepted_sections = {
        "town": ("town center", "general store", "gate house", "bath house", "bar"),
        "ruins": ("ruined street", "ruined office", "ruined house", "ruined garage"),
        "mansion": ("kitchen", "foyer", "sun room", "living room", "hallway"),
        "upstairs": ("manager office", "break room", "balcony"),
        "gen back rooms": ("weapon storage", "work room", "general storage", "freezer"),
        "tower": ("tower entrance", "tower peak"),
        "cellar": ("cellar entrance", "wine casks", "lab"),
        "gardens": (),
        "inn": ("inn entrance", "inn room"),
    }
    use_remarks = (
        "I was useful after all.",
        "I feel used...",
        "I never knew I could use myself.",
        "At least I didn't ruffle my mane.",
        "I think I'm still in one piece after that.",
    )

    def __init__(self, debug):

        self.inventory = ["self"]
        self.debug = debug
        self.sleep = False
        self.bathed = False
        self.name = "Vern MacCaster"
        # neg
        self.buy_item_values = {"fish": -5, "can": -3}
        # pos
        self.sell_item_values = {"fish": 4, "can": 2, "rock": 1}
        self.__location = "town center"
        self.__section = "town"
        self.changed_location = True
        self.__score = 0
        self.player_wallet = 0
        self.places = []

        self.item_dictionary = {
            "music sheet": "A piece of sheet music. Maybe someone would want this?",
            "fish": "A tasty fish for testing only.",
            "vhs tape": "An old VHS tape that a collector might want somewhere.",
            "movie poster": "An old movie poster. It shows an action hero fighting a monster cat man.",
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nLocation {self.__location}\nSection {self.section}\nScore {self.__score}"""

    # enables changing player room for testing
    def debug_player(self):
        print("\n")
        print("item, wallet, location.")
        pick = input("").lower()

        # debug for changing rooms
        if pick == "location":
            print("\nEnter location?\n")
            for number, place in enumerate(self.accepted_locations):
                print(f"{self.bold+place+self.end}", end=", ")
                if (number + 1) % 4 == 0:
                    print("")
            print("")
            choice = input("").lower()
            self.location = choice

        # debug for adding items to inventory
        elif pick == "item":
            print("\nEnter item?\n")
            for number, place in enumerate(self.item_dictionary):
                print(f"{self.bold+place+self.end}", end=", ")
                if (number + 1) % 4 == 0:
                    print("")
            print("")
            choice = input("").lower()
            if choice in self.item_dictionary:
                self.inventory.append(choice)
            else:
                print("No matching item to add.")
        elif pick == "wallet":
            number = input("Amount? ")
            if number.isdigit():
                number = int(number)
                self.change_player_wallet(number)
            else:
                print("Must be an integer only.")

    @property
    def section(self):
        return self.__section

    @section.setter
    def section(self, new_sec):
        self.__section = new_sec

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        # makes sure that you do not enter a bad location.
        if location not in self.accepted_locations:
            if self.debug:
                print(
                    f"Could not fine {location}... Possible missing spelling in code?"
                )
                print("Could not find matching location. Canceling movement.")
            else:
                raise LocationError(location)

        # should never need to move to own location
        elif location == self.location and not self.debug:
            raise RedundantMoveError(self.name)

        # makes sure not to print if you win or end game
        elif location != "end" and location != "exit":

            # checks if we need to update the section you are in
            if location not in self.accepted_sections.get(self.section):
                for key in self.accepted_sections:
                    if location in self.accepted_sections.get(key):
                        print(f"You have gone to the {location}, in the {key}.")
                        self.changed_location = True
                        self.section = key
                        self.__location = location
                        break
                else:
                    raise ChangeSectionError(location)

            else:
                print(f"You have gone to the {location}.")
                self.changed_location = True
                self.__location = location

        # if you go to the exit or end, does not print anything
        else:
            self.__location = location

    def change_player_wallet(self, new_value):
        if new_value < 0:
            print(f"You lost {abs(new_value)} coins.")
        elif new_value > 0:
            print(f"You got {new_value} coins!")
        else:
            print("Error somehow got 0 dollars.")
        self.player_wallet += new_value
        print(f"You have {self.player_wallet} coins total now.")

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, new_value):
        if new_value < 1:
            raise ValueError(f"Must be x >= 1, {new_value}.")
        else:
            print("You're score went up!")
            self.__score = new_value

    # prints your score
    def print_score(self):
        print(f"Your score is {self.score}.")

    # prints his inventory
    def check_inventory(self):
        # if self is some how removed it will be added back.
        # just in case.
        if "self" not in self.inventory:
            self.inventory.append("self")
        if len(self.inventory) == 1:
            print("My pockets are empty it seems.")
        else:
            print("I have...")
            for item in self.inventory:
                # should not be shown to player as being an item.
                if item != "self":
                    print(
                        f"{self.bold + item + self.end:<25}{self.item_dictionary.get(item, 'Error, Report me pls!'):<5}"
                    )

    # removes items from player
    # can use any number of items.
    def use_item(self, *items):
        # never removes self from inventory.
        for item in items:
            if item != "self":
                print(f"I used the {self.bold + item + self.end}.")
                self.inventory.remove(item)
            else:
                # prints something random when you use yourself
                print(random.choice(self.use_remarks))

    # combines items
    def combine_items(self, *item_list):
        # unpacking the items to use later
        item_1, item_2 = item_list
        if item_1 in self.inventory and item_2 in self.inventory:

            # to do: add combinable items
            if 0:
                pass
            # no matches found
            else:
                print(f"I can't combine {item_1} and {item_2}.")

        # No matching items found
        else:
            print("I don't have all I need.")

    # looking at map
    def look_player_map(self):
        print("Let me check my map.\n*Map crinkling sounds.*")
        places = []
        # should never see a XX on map
        player_room = "XX"
        map_dict = self.map_dict.get(self.section)
        for map_icon in map_dict:
            if map_dict.get(map_icon) == self.location:
                places.append("@@")
                player_room = map_icon
            else:
                places.append(map_icon)
        if "@@" not in places and "XX" in places:
            raise LocationError(self.location)
        time.sleep(1.5)
        if self.section == "town":
            print(
                f"""
                                                   +--------------------+
                                                   |     Town Area      |
                                                   +--------------------+     
                                                   |Legend:             |
                                                   |                    |
                                                   |Ruins Area:      RA |
                      {places[1]} IA                        |Mansion Area:    MA |
                      ||//                         |Back Rooms Area: BA |
                  RA--{places[0]}--{places[4]}--MA                   |Town Center:     TC |
                      ||\\\\                         |Town Bar:        TB |
                      {places[2]} {places[3]}                        |General Store:   GS |
                     //                            |Bath House:      BH |
                     BA                            |Gate House:      GH |
                                                   |Inn Area:        IA |
                                                   |You: @@ in room  {player_room} |
                                                   +--------------------+ 
              """
            )
        elif self.section == "ruins":
            print(
                f"""
                                                   +--------------------+
                                                   |     Ruins Area     |
                                                   +--------------------+
                      {places[2]}                           |Legend:             |
                      ||                           |                    |
                      {places[3]}--TA                       |Town Area:       TA |
                      ||\\\\                         |Upstairs Area:   UA |
                  UA--{places[1]} {places[0]}                        |Ruined House:    RH |
                                                   |Ruined Garage:   RG |
                                                   |Ruined Office:   RO |
                                                   |Ruined Street:   RS |
                                                   |You: @@ in room  {player_room} |
                                                   +--------------------+
              """
            )
        elif self.section == "tower":
            print(
                f"""
                                                   +--------------------+
                                                   |     Tower Area     |
                                                   +--------------------+
                      {places[0]}                           |Legend:             |
                      ||                           |                    |
                      {places[1]}                           |Mansion Area:    MA |
                      ||                           |Tower Peak:      TP |
                      MA                           |Tower Entrance:  TE |
                                                   |You: @@ in room  {player_room} |
                                                   +--------------------+
              """
            )
        elif self.section == "mansion":
            print(
                f"""
                                                   +--------------------+
                                                   |    Mansion Area    |
                                                   +--------------------+
                                                   |Legend:             |
                      MT                           |                    |
                      ||                           |Town Area:       TA |
                      {places[3]}  {places[4]}                       |Mansion Tower:   MT |
                      ||  ||                       |Garden Area:     GA |
                  TA--{places[0]}--{places[2]}--GA                   |Mansion Foyer:   MF |
                      ||                           |Mansion Kitchen: MK |
                      {places[1]}                           |Hallway:         HW |
                      ||                           |Sun Room:        SR |
                      CA                           |Living Room:     LR |
                                                   |You: @@ in room  {player_room} |
                                                   +--------------------+
              """
            )
        elif self.section == "gardens":
            print(
                """
                                                   +--------------------+
                                                   |    Garden Area     |
                                                   +--------------------+
                                                   |Legend:             |
                                                   |                    |
                                                   |Mansion Area:    MA |
                                                   |Room One:        R1 |
                                                   |Room Two:        R2 |
                                                   |Room Three:      R3 |
                                                   |Room Four:       R4 |
                                                   |Room Five:       R5 |
                                                   |Room Six:        R6 |
                                                   |Room Seven:      R7 |
                                                   |You: @@ in room  ?? |
                                                   +--------------------+
              """
            )
        elif self.section == "cellar":
            print(
                f"""
                                                   +--------------------+
                                                   |    Cellar Area     |
                                                   +--------------------+
                                                   |Legend:             |
                      MA                           |                    |
                      ||                           |Mansion Area:    MA |
                      {places[2]}--{places[0]}                       |Lab:             LB |
                      ||                           |Wine Casks:      WC |
                      {places[1]}                           |Cellar Entrance: CE |
                                                   |You: @@ in room  {player_room} |
                                                   +--------------------+
              """
            )
        elif self.section == "gen back rooms":
            print(
                f"""
                                                   +--------------------+
                                                   |  Back Rooms Area   |
                                                   +--------------------+
                        TA                         |Legend:             |
                       //                          |                    |
              {places[2]}--{places[0]}--{places[3]}                           |Town Area:       TA |
                    \\\\||                           |General Storage: GS |
                      {places[1]}                           |Work Room:       WR |
                                                   |Freezer:         FR |
                                                   |Weapons Storage: WS |
                                                   |You: @@ in room  {player_room} |
                                                   +--------------------+
              """
            )
        elif self.section == "upstairs":
            print(
                f"""
                                                   +--------------------+
                                                   |   Upstairs Area    |
                                                   +--------------------+
                                                   |Legend:             |
                                                   |                    |
                   {places[1]}-{places[0]}-RA                        |Ruins Area:      RA |
                    \\\\//                           |Break Room:      BR |
                     {places[2]}                            |Managers Office: MO |
                                                   |Garage Balcony:  GB |
                                                   |You: @@ in room  {player_room} |
                                                   +--------------------+
              """
            )
        elif self.section == "inn":
            # dynamic map
            print(
                f"""
                                                   +--------------------+
                                                   |      Inn Area      |
                                                   +--------------------+
                       TA                          |Legend:             |
                       ||                          |                    |
                       {places[0]}--{places[1]}                      |Town Area:       TA |
                                                   |Inn Entrance:    IE |
                                                   |Inn Room:        IR |
                                                   |You: @@ in room  {player_room} |
                                                   +--------------------+
              """
            )
        else:
            # IF I fail to find a matching map section
            raise MapMatchError(self.section)

    # looking at self
    def look_self(self):
        print(
            "A nervous lion is what you are. Somehow still alive but for how long? Hopefully long enough."
        )
        if not self.bathed:
            print(
                random.choice(
                    [
                        "I could really use a good clean up.",
                        "I'm covered in filth from traveling. I better find somewhere to clean myself up.",
                        "My mane needs a good clean up and brush.",
                    ]
                )
            )
        else:
            print("I'm looking a lot nicer than when I came here.")


class TimeKeeper:
    def __init__(self):
        self.__timer = 700
        self.__am_pm = "AM"
        self.__days_past = 0

    @property
    def days_past(self):
        return self.__days_past

    @days_past.setter
    def days_past(self, new_value):
        if new_value - self.days_past != 1:
            raise ValueError(
                f"Increasing time can only be done with a value of one, {new_value}."
            )
        else:
            self.__days_past = new_value
            print("A new day is here.")

    @property
    def am_pm(self):
        return self.__am_pm

    @am_pm.setter
    def am_pm(self, value):
        if value in ("AM", "PM"):
            self.__am_pm = value
        else:
            print("Error, bad value in AM/PM switcher.")

    @property
    def timer(self):
        return self.__timer

    @timer.setter
    def timer(self, add_time):
        if (self.__timer + add_time) / 2 > 2400:
            add_time = (self.__timer + add_time) % 2400
            self.days_past += 1
            self.am_pm = "AM"
        self.__timer = add_time
        if self.timer == 1200:
            self.am_pm = "PM"

    def __str__(self):
        if self.timer >= 1300:
            clock_time = str(self.timer - 1200)
        else:
            clock_time = str(self.timer)

        # making sure it is always the right length for my string methods
        clock_time = clock_time.zfill(4)
        clock_time = clock_time[0:2] + ":" + clock_time[2:]
        # finds the human readable time
        minutes = str(int(int(clock_time[3:5]) * 3 / 5))
        clock_time = clock_time[0:3] + minutes.zfill(2)

        return f"The time is {clock_time}, {self.am_pm} and {self.days_past} days have past."


class RoomSystem:
    """This starts all the rooms.
    It also will track NPC movements and cross room changes."""

    bold = colorama.Style.BRIGHT
    end = colorama.Style.NORMAL

    def __init__(self, player):
        # room update trackers
        self.room_booleans = {
            "room rented": False,
            "player bathed": False,
            "office opened": False,
        }
        self.entry_events_dict = {
            # first entry events
            "gen work room": False,
            "bath house first": False,
            "garage entry": False,
        }
        # random event seed
        self.random_counter = random.randint(10, 25)
        # clock system being started
        self.clock = TimeKeeper()
        # saving player class for later
        self.player = player
        # back rooms
        self.weapons_storage = rooms.WeaponsStorage(player)
        self.general_storage = rooms.GeneralStorage(player)
        self.freezer = rooms.Freezer(player)
        self.work_room = rooms.WorkRoom(player)
        # town center
        self.center = rooms.TownCenter(player, self.clock)
        self.bar = rooms.TownBar(player)
        self.gen_store = rooms.TownGenStore(player)
        self.bath_house = rooms.TownBathHouse(player)
        self.gate_house = rooms.TownGateHouse(player)
        # ruins
        self.ruin_office = rooms.RuinedOffice(player)
        self.street = rooms.RuinedStreet(player)
        self.house = rooms.RuinedHouse(player)
        self.garage = rooms.RuinedGarage(player)
        # upstairs
        self.gar_office = rooms.UpstairsOffice(player)
        self.break_room = rooms.UpstairsBreakRoom(player)
        self.balcony = rooms.UpstairsBalcony(player)
        # tower rooms
        self.tow_entrance = rooms.TowerEntrance(player)
        self.peak = rooms.TowerPeak(player)
        # mansion rooms
        self.foyer = rooms.MansionFoyer(player)
        self.kitchen = rooms.MansionKitchen(player)
        self.hallway = rooms.MansionHallWay(player)
        self.sun_room = rooms.MansionSunRoom(player)
        self.living_room = rooms.MansionLivingRoom(player)
        # cellar rooms
        self.lab = rooms.CellarLab(player)
        self.cell_entrance = rooms.CellarEntrance(player)
        self.wine_casks = rooms.CellarWineCasks(player)

        # inn rooms
        self.inn_entrance = rooms.InnEntrance(player)
        self.inn_room = rooms.InnRoom(player, self.clock)

        # Loading NPCs
        self.scavenger = npc.ScavengerNPC(self.clock, player)
        self.organ_player = npc.OrganPlayer(self.clock, player)
        self.gen_shop_keeper = npc.GeneralStoreOwner(self.clock, player)
        self.katie = npc.Katie(self.clock, player)
        self.johnson = npc.Johnson(self.clock, player)
        self.collector = npc.CollectorFelilian(self.clock, player)
        self.inn_keeper = npc.InnKeeper(self.clock, player)

        # list NPCs to check if should be moved
        self.npc_roster = {
            # scavenger NPC.
            self.scavenger.name: self.scavenger,
            # organ player NPC
            self.organ_player.name: self.organ_player,
            # general store owner NPC
            self.gen_shop_keeper.name: self.gen_shop_keeper,
            # Katie NPC
            self.katie.name: self.katie,
            # Johnson NPC
            self.johnson.name: self.johnson,
            # collector NPC
            self.collector.name: self.collector,
            # the inn keeper
            self.inn_keeper.name: self.inn_keeper,
        }

        # lists possible rooms to move to
        self.switcher_dictionary = {
            # town center rooms and actions
            "town center": self.center,
            "bar": self.bar,
            "bath house": self.bath_house,
            "general store": self.gen_store,
            "gate house": self.gate_house,
            # ruins rooms and actions
            "ruined street": self.street,
            "ruined office": self.ruin_office,
            "ruined house": self.house,
            "ruined garage": self.garage,
            # garage upstairs rooms and actions
            "break room": self.break_room,
            "managers office": self.gar_office,
            "balcony": self.balcony,
            # back rooms and actions
            "weapons storage": self.weapons_storage,
            "work room": self.work_room,
            "freezer": self.freezer,
            "general storage": self.general_storage,
            # tower rooms and actions
            "tower entrance": self.tow_entrance,
            "tower peak": self.peak,
            # mansion rooms and actions
            "foyer": self.foyer,
            "sun room": self.sun_room,
            "hallway": self.hallway,
            "kitchen": self.kitchen,
            "living room": self.living_room,
            # garden rooms and actions
            # "garden": self.rooms,
            # inn rooms and actions
            "inn entrance": self.inn_entrance,
            "inn room": self.inn_room,
            # cellar rooms and actions
            "cellar entrance": self.cell_entrance,
            "wine casks": self.wine_casks,
            "lab": self.lab,
        }
        self.random_events = rooms.RandomEvent(self.switcher_dictionary)

    def time_wait_events(self):
        # checks if it is your first time
        # will allow time to pass when you sleep or preform some actions
        if self.player.sleep:
            if self.clock.timer == 700:
                rooms.clear()
                print("You wake up feeling rested.")
                print(self.clock)
                self.player.sleep = False

        # moves player out of the general store
        if (2000 <= self.clock.timer <= 2500 or 0 <= self.clock.timer <= 800) and (
            self.player.location == "general store"
            or self.player.section == "gen back rooms"
        ):

            print("Looks like the store is closing. I'll have to leave for the night.")
            time.sleep(1)
            self.player.location = "town center"

        # if one is triggered can not happen again until up to 25 turns have passed
        if not self.player.sleep:
            if self.random_counter <= 0:
                random_event = self.random_events.grab_event(self.player.location)
                if random_event:
                    print(self.bold + random_event + self.end)
                    self.random_counter = random.randint(1, 25)

            else:
                self.random_counter -= 1

    # starts the NPCs where they should be
    def set_up_npc(self):
        for name in self.npc_roster:
            person = self.npc_roster.get(name)
            starting_point = self.switcher_dictionary.get(person.position)

            # errors if no matching location is found for starting point
            if starting_point is None:
                raise NPCLocationError(name, person.position)
            # added them to the rooms action dictionaries
            starting_point.look_dict[name] = person.look_npc
            starting_point.oper_dict[name] = person.talk_to_npc
            starting_point.use_dict[name] = person.use_item

    # moves NPCs around or removes them from the world
    def npc_movement_checker(self):

        # self.time_wait_events()
        # cross room changes checker
        self.cross_room_changes()
        npc_deletion = []
        # checks each NPC that can move
        for name in self.npc_roster:
            person = self.npc_roster.get(name)
            current_local = person.position
            # if NPC is to move and they are not disabled
            if person.check_move() and person.alive:
                if current_local == person.position:
                    # NPC should never move to the same room twice
                    raise RedundantMoveError(name)
                # add to new room
                new_room = self.switcher_dictionary.get(person.position)
                if name not in new_room.look_dict:
                    new_room.look_dict[name] = person.look_npc
                if name not in new_room.oper_dict:
                    new_room.oper_dict[name] = person.talk_to_npc
                if name not in new_room.use_dict:
                    new_room.use_dict[name] = person.use_item

                # delete from old room
                old_room = self.switcher_dictionary.get(current_local)
                if name in old_room.look_dict:
                    del old_room.look_dict[name]
                if name in old_room.oper_dict:
                    del old_room.oper_dict[name]
                if name in old_room.use_dict:
                    del old_room.use_dict[name]

            # if they are marked for deletion
            # we remove them from the game.
            elif not person.alive:
                current_room = self.switcher_dictionary.get(person.position)
                if name in current_room.look_dict:
                    del current_room.look_dict[name]
                if name in current_room.oper_dict:
                    del current_room.oper_dict[name]
                if name in current_room.use_dict:
                    del current_room.use_dict[name]
                npc_deletion.append(name)

        # actually removes them from the game
        for name in npc_deletion:
            if name in self.npc_roster:
                del self.npc_roster[name]

        # counts clock up by a quarter hour every player move
        self.clock.timer += 25

    def first_entered_events(self):
        # if all are triggered it stops running all the checks
        if not all(self.entry_events_dict.values()):
            if (
                self.player.location == "work room"
                and not self.entry_events_dict["gen work room"]
            ):
                print(
                    "As you enter the room an odd looking animal grabs the tool bag and leaps out a window."
                    "\nDamn it. Now how am I going to get that machine fixed? I need to find that creature."
                )
                time.sleep(1)
                self.entry_events_dict["gen work room"] = True
            elif (
                self.player.location == "bath house"
                and not self.entry_events_dict["bath house first"]
            ):
                print(
                    "The large pipe feeding the baths suddenly springs a leak. The owner grumbles and looks you over"
                    "\nIf I didn't know any better I'd think you were a black cat, he mutters."
                    "\nI'll need to fix that before I can get cleaned up from the road."
                )
                self.entry_events_dict["bath house first"] = True
                time.sleep(1)
            elif (
                self.player.location == "ruined garage"
                and not self.entry_events_dict["garage entry"]
            ):
                print(
                    "As you open the door to the inside and walk in, you accidentally knock over a large tool chest."
                    "\nYou're tail frizzes up and you jump back. When you're eyes fall upon the tool chest, you feel"
                    "rather silly."
                )
                self.entry_events_dict["garage entry"] = True
                time.sleep(1)

    def cross_room_changes(self):
        # updates the game rooms if you rent a room
        if self.inn_keeper.room_rented and not self.room_booleans["room rented"]:
            self.katie.home_room = "inn room"
            self.johnson.home_room = "inn room"
            self.inn_entrance.room_rented = True
            self.room_booleans["room rented"] = True

        # opens the office if you find the ghost
        if self.inn_room.ghost_found and not self.room_booleans["office opened"]:
            self.room_booleans["office opened"] = True
            self.street.office_opened = True

    # allows debugging of NPCs
    def debug_npc(self):
        for number, person in enumerate(self.npc_roster):
            print(person, end=", ")
            if (number + 1) % 3 == 0:
                print("")
        print("")
        choice = input("").lower()
        if choice in self.npc_roster:
            pprint.pprint(vars(self.npc_roster.get(choice)))
        else:
            print("No match found.")
