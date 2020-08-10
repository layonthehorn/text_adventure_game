import time
import random
import os
import platform
import colorama
colorama.init()


# allows me to clear the screen when playing
def clear():
    operating = platform.system()
    if operating == 'Linux' or operating == "Darwin":
        os.system("clear")
    elif operating == 'Windows':
        os.system('cls')
    else:
        print("\n" * 100)


# function class for inheritance.
class FunctionClass:
    """Never to be called. Only used for giving all other classes the same methods."""

    # class variables for print formatting
    bold = colorama.Style.BRIGHT
    end = colorama.Style.NORMAL

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
                print(f"I can't look at the {look_at}.")

        else:
            print(f"I can't look at the {look_at}.")

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
                print(f"I can't operate the {operate}.")
        else:
            print(f"I can't operate the {operate}.")

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
                print(f"I can't go to {go}.")
        else:
            print(f"I can't go to {go}.")

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
            if item == "map":
                print(f"Hey a {self.bold + item + self.end}, this might help me out.")
            else:
                print(f"I got the {self.bold + item + self.end}.")
            self.inventory.remove(item)
            self.player_object.inventory.append(item)
        else:
            print(f"There isn't a(n) {item} to get.")

    # dropping item back into room
    def drop_item(self, item):
        if item in self.player_object.inventory and item != "map":
            print(f"I dropped the {self.bold + item + self.end}.")
            self.inventory.append(item)
            self.player_object.inventory.remove(item)
        elif item in self.player_object.inventory and item == "map":
            print("I might need it, I'm not going to drop it.")
        else:
            print(f"I don't have a(n) {item} to drop.")

    # prints items and bolds them for effect.
    def print_items(self):
        if len(self.inventory) > 0:
            for item in self.inventory:
                print(f"There is a(n) ", end="")
                print(self.bold, item, self.end)

    # prints what you can look at
    def print_look(self):
        print("__________________")
        look_list = ""
        print("I could look at...")
        for thing in self.look_dict:
            look_list += f"'{self.bold + thing + self.end}', "
        print(look_list)
        print("_" * len(look_list))

    # prints where you can go
    def print_locations(self):
        go_list = ""
        print("I could go to...")
        for location in self.go_dict:
            go_list += f"'{self.bold + location + self.end}', "
        print(go_list)
        if self.inventory:
            print("_" * len(go_list))


# Player Class
class PlayerClass:
    """This is the main player class. It holds the player inventory and score among other things."""

    # class variables for print formatting
    bold = '\033[1m'
    end = '\033[0;0m'

    def __init__(self):

        self.inventory = ["self"]
        self.__location = "bunker"
        self.player_score = 0
        self.mane_brushed = False
        self.generator_working = False
        self.changed_location = False
        self.fish_counter = 0
        self.use_remarks = ("I was useful after all.", "I feel used...", "I never knew I could use myself.",
                            "At least I didn't ruffle my mane.", "I think I'm still in one piece after that.")
        self.places = ["MP", "UH", 'PS', 'SS', 'RR', 'AD', 'SD', 'WW', 'TS', 'C ', 'FS', 'CR']
        self.accepted_locations = ("plaza", "bunker",
                                   "side room", "small den", "west wing", "cemetery", "toy shop",
                                   "pet shop", "exit", "end", "upstairs hallway", "animal den",
                                   "shoe store", "bathroom", "basement entry", "basement generator room")
        self.map_dictionary = {
            "plaza": "MP",
            "bunker": "FS",
            "side room": "CR",
            "small den": "SD",
            "west wing": "WW",
            "cemetery": "C ",
            "toy shop": "TS",
            "pet shop": "PS",
            "upstairs hallway": "UH",
            "animal den": "AD",
            "shoe store": "SS",
            "bathroom": "RR",
        }

        self.item_dictionary = {
            "wrench": "Used for unstucking random things. Always handy with robots.",
            "fuse": "Lots of old world tech uses this to keep power flowing.",
            "bag of catnip": "Hey now. You need to stay sober.",
            "lion plush": "A cute lion plush. I wonder who left this here?",
            "keys": "These might be handy for reaching high places.",
            "strange keys": "For some reason you recognise them. Maybe they belong to a friend?",
            "meat": "Maybe something will want this?",
            "toy raygun": "It's flashing random colors. Not useful but fun!",
            "knife": "It cuts. I mean what else do you think it does?",
            "fur sample": "It's fur. Maybe you could use it to get in the pet store?",
            "map": "A map to the mall! Someone must have updated it recently.",
            "drugged meat": "This would knockout anything that eats it.",
            "battery": "This could be used to power something, or overpower it.",
            "mane brush": "You could use this on your mane. Not that you ever need it.",
            "self": "It's you... You should not see this item in your inventory. Please report it!",
            "cheetah keyring": "It's a cheetah keyring. Cute but not really useful to you right now.",
            "cat toy": "A lion plush stuff with catnip. You druggie...",
            # in toy shop
            "red fuse": "It's a red fuse. Much larger than the one from the bunker.",
            # in side room
            "green fuse": "It's a green fuse. Much larger than the one from the bunker.",
            # in cemetery
            "gold fuse": "It's a gold fuse. Much larger than the one from the bunker.",
            # in main plaza
            "blue fuse": "It's a blue fuse. Much larger than the one from the bunker.",
            "fish": "A very tasty if small fish. Should you?.. Eat it?",
            "bones": "Bones are all that's left of the little fish you ate. How could you?",
            "rope": "A length of rope. Might be useful to get somewhere lower.",
            "long rope": "A long length of rope. This should reach the bottom.",
            "soda": "An old flat soda. Not something you want to drink.",
            "shovel": "It's an old entrenching tool. Useful for digging and many other things.",
            "soldering iron": "It's used to repair wires and circuits.",
            "soldering wire": "Used to fix circuits and connections.",
            "capacitor": "A part to a circuit board, might be handy.",
            "circuit board": "A repaired part to a machine somewhere.",
            "toy lion tail": "A toy tail for a child to wear. I guess even humans wanted to be lions...",
            "owl figurine": "A nice little owl toy. Has hoot hoot written on the bottom.",
            "coin": "Useful for just about nothing now that the human world has fallen.",
            "screw driver": "Useful for taking things apart and also breaking them open."
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nLocation {self.location}\nScore {self.player_score}\nMane brushed {self.mane_brushed}\nFish counter {self.fish_counter}"""

    # enables changing player room for testing
    def debug_player(self):
        print("\nEnter location?\n")
        for number, place in enumerate(self.accepted_locations):
            print(f"{self.bold+place+self.end}", end=", ")
            if (number + 1) % 4 == 0:
                print("")
        print("")
        choice = input("").lower()
        self.location = choice

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        # makes sure that you do not enter a bad location.
        if location not in self.accepted_locations:
            print(f"Could not fine {location}... Possible missing spelling in code?")
            print("Could not find matching location. Canceling movement.")

        # makes sure not to print if you win or end game
        elif location != "end" and location != "exit":
            print(f"You have gone to the {location}.")
            self.__location = location
            self.changed_location = True

        # if you go to the exit or end, does not print anything
        else:
            self.__location = location

    # prints your score
    def print_score(self):
        print(f"Your score is {self.player_score}.")

    # sets player score
    def increase_score(self):
        print("Your score went up!")
        self.player_score += 1

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
                        f"{self.bold + item + self.end:<20}{self.item_dictionary.get(item, 'Error, Report me pls!'):<5}")

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

            # item crafting results
            if "meat" in item_list and "drugs" in item_list:
                self.use_item(item_1, item_2)
                self.inventory.append("drugged meat")
                print("I made drugged meat. Still nasty after that.")
                self.increase_score()

            elif "lion plush" in item_list and "bag of catnip" in item_list:
                self.use_item(item_1, item_2)
                self.inventory.append("cat toy")
                print("I am so ashamed of myself for this...")

            # all using items on self reactions
            elif "self" in item_list and "cat toy" in item_list:
                self.use_item(item_1, item_2)
                print("purrrrr Mmmmm catnip.")

            elif "self" in item_list and "mane brush" in item_list:
                self.use_item(item_1, item_2)
                print("Hey, I'm looking better now. That's good too.")
                self.mane_brushed = True
                self.increase_score()

            elif "self" in item_list and "drugs" in item_list:
                print("I'm not eating them...")

            elif "self" in item_list and "meat" in item_list:
                print("Nasty. I love meat but this is not appetizing at all.")

            elif "self" in item_list and "drugged meat" in item_list:
                print("Eating rotten meat is not any safer with medication in it.")

            elif "self" in item_list and "soda" in item_list:
                print("I hate sugary things...")

            elif "self" in item_list and "bag of catnip" in item_list:
                print("I need to stay sober right now... \nIf it was in a little cute toy I might... No, I better not.")

            elif "self" in item_list and "knife" in item_list:
                print("I don't think that's a great plan...")

            elif "self" in item_list and "toy lion tail" in item_list:
                print("I already have a tail thank you. Might save this for my daughter though.")

            # small thing for player repeating the eat fish command
            elif "self" in item_list and "fish" in item_list:
                if self.fish_counter == 0:
                    print("I really shouldn't. Though it is tasty looking...")
                    self.fish_counter += 1
                elif self.fish_counter == 1:
                    print("Still shouldn't eat it.")
                    self.fish_counter += 1
                elif self.fish_counter == 2:
                    print("No, I need to get rid of it. I keep getting temped.")
                    self.fish_counter += 1
                else:
                    print("Vern finally gives in and eats the little fish.")
                    print("Oh no! I couldn't resist anymore...")
                    print("Now all I have is a pile of bones.")
                    self.inventory.append("bones")
                    self.use_item(item_1, item_2)
            # no matches found
            else:
                print(f"I can't combine {item_1} and {item_2}.")

        # No matching items found
        else:
            print("I don't have all I need.")

    # looking at map
    def look_player_map(self):
        if "map" in self.inventory:
            print("Let me check my map.\n*Map crinkling sounds.*")
            time.sleep(1.5)
            if self.location == "basement entry" or self.location == "basement generator room":
                print("\nThis place is not on the map at all.\n")
            rooms = []
            p_local = "??"
            for room in self.places:
                if self.map_dictionary.get(self.location, "") == room:

                    # if the player is on the map it changes that room to the player symbol
                    rooms.append("@@")
                    # then puts the room symbol in the legend
                    p_local = room
                else:
                    # other wise just puts rooms there normally
                    rooms.append(room)
            print(f"""
              ---------MAP----------
                                                   +--------------------+
                       {rooms[3]}                          |Legend:             |
                       ||                          |                    |
                   {rooms[5]}--{rooms[1]}--{rooms[4]}                      |Main Plaza: MP      |
                {rooms[9]}  {rooms[6]} ||                          |Upper Hall: UH      |
                ||   \\\\||                          |Pet Shop: PS        |
            {rooms[2]}--{rooms[7]}-----{rooms[0]}----EXIT                  |Shoe Store: SS      |
                ||     ||                          |Restroom: RR        |
                {rooms[8]}     {rooms[10]}--{rooms[11]}                      |Animal Den: AD      |
                                                   |Small Den: SD       |
                                                   |West wing: WW       |
                                                   |Toy Shop: TS        |
                                                   |Cemetery: C         |
                                                   |Fallout Shelter: FS |
                                                   |Computer Room: CR   |
                                                   |You: @@ in room {p_local}  |
                                                   +--------------------+  
                   """)

        else:
            print("I don't have one.")

    # looking at self
    def look_self(self):
        print("A nervous lion is what you are. Somehow still alive but for how long? Hopefully long enough.")
        if "meat" in self.inventory or "drugged meat" in self.inventory:
            print("This meat smells awful...")
        if self.mane_brushed:
            print("At least I'm cleaned up now.")


# Bunker Areas
class Bunker(FunctionClass):
    """This is the bunker class. It acts as the starting room for the player."""

    def __init__(self, player_object):
        self.inventory = []
        self.player_object = player_object
        self.fuse_box, self.door_opened, self.robot_fixed = (False, False, False)
        self.look_dict = {
            "room": self.print_description_room,
            "fuse box": self.print_description_box,
            "exit door": self.print_description_door,
            "robot": self.print_description_robot
        }

        self.go_dict = {
            "side room": self.go_sideroom,
            "outside": self.go_outside
        }
        self.oper_dict = {
            "door": self.oper_door
        }

        self.use_dict = {
            "robot": self.fix_robot,
            "fuse box": self.fix_fuse_box
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nFuse fixed {self.fuse_box}\nRobot fixed {self.robot_fixed}\nDoor opened {self.door_opened}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("The room is dark and blasted out.")
        print("The room smells of mould and rust. There is a disabled 'robot' in the corner, an entry to \na side room "
              "\nand there is a 'door' that appears to be locked. Maybe it’s connected to that fuse 'box'?.")
        if self.door_opened:
            print("The door to 'outside' is open.")
        self.print_look()
        self.print_locations()
        self.print_items()

    # this prints a description of the fuse box
    def print_description_box(self):
        if not self.fuse_box:
            print("It's an old fuse box....")
            time.sleep(1)
            print("And of course it's lacking a fuse.")
        else:
            print("Hey, it's working now!")

    def print_description_door(self):
        print("It's an old bunker door. Looks like it has a power lock.")
        if not self.fuse_box:
            print("I need to find a way to power it.")
        elif not self.door_opened:
            print("I need to open it I think now that it has power again.")
        else:
            print("I hope it stays working as long as I need it.")

    def print_description_robot(self):
        if not self.robot_fixed:
            print("It's a robot and it has a fuse!")
        elif 'fuse' in self.inventory and self.robot_fixed:
            print("I can get the fuse now.")
        else:
            print("I took the robots fuse.")

    def go_outside(self):
        if self.door_opened:
            self.player_object.location = "plaza"
        elif self.fuse_box and not self.door_opened:
            print("I need to open the door first.")
        elif not self.fuse_box:
            print("I need to power the door and open it first.")

    def go_sideroom(self):
        self.player_object.location = "side room"

    # attempts to fix fuse box
    def fix_fuse_box(self, item):
        if not self.fuse_box:
            if item == "fuse":
                print("the fuse box is now working!")
                self.player_object.use_item(item)
                self.player_object.increase_score()
                self.fuse_box = True
            else:
                print(f"I can't use {item} with the fuse box.")
        else:
            print("There is nothing else I need to do here.")

    # used to get fuse loose from robot
    def fix_robot(self, item):
        if not self.robot_fixed:
            if item == "wrench":
                print("The robot's fuse is loose!")
                self.robot_fixed = True
                self.inventory.append("fuse")
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"I can't use {item} with the robot.")
        else:
            print("I don't have to mess with it anymore.")

    # tries to open door will fail if fuse box is not working.
    def oper_door(self):
        if not self.fuse_box:
            print("The door is stuck. Looks like it's out of power.")
        elif self.door_opened:
            print("The door is already opened.")
        elif self.fuse_box and not self.door_opened:
            print("The door has opened! Now I can go outside!")
            self.player_object.increase_score()
            self.door_opened = True


class ComputerRoom(FunctionClass):
    """The side room to the bunker."""

    def __init__(self, player_object):

        self.inventory = ["wrench"]
        self.player_object = player_object
        self.light_switch, self.safe_opened = (False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "light switch": self.print_description_light,
            "computer": self.print_description_computer,
            "safe": self.print_description_safe
        }

        self.go_dict = {
            "bunker": self.go_bunker
        }
        self.oper_dict = {
            "light switch": self.turn_on_switch,
            "computer": self.use_computer,
            "safe": self.operate_safe
        }

        self.use_dict = {}

    def __str__(self):
        return f"""Inventory {self.inventory}\nLight switch {self.light_switch}\nSafe ready to open {self.safe_opened}"""

    # this prints a description along with a item list
    def print_description_room(self):
        if self.light_switch:
            print("You walk into a small room. It is dark and doesn’t smell any better than the rest of the bunker. "
                  "\nThere is a 'light' switch by the entryway. In the corner is an old 'computer' which appears to still "
                  "\nbe operational. You can get back to the 'bunker' too.")
            print("There is an old 'safe' of some sort too.")
            self.print_look()
            self.print_locations()
            self.print_items()
        else:
            print("There's a 'light switch' on the wall and an exit back to the 'bunker' \nbut otherwise it's too dark "
                  "to see.")

    def print_description_light(self):
        print("It's a light switch.")
        if self.light_switch:
            print("I hope there is power in here still.")
        else:
            print("I can't believe there is still power here.")

    def print_description_computer(self):
        if self.light_switch:
            print("An old but still working 'computer'.\nMaybe someone left some information on it.")
        else:
            print("It's too dark to see.")

    def print_description_safe(self):
        if self.light_switch:
            print("An old safe. Looks like it uses a biometric lock of some sort.")
            if not self.safe_opened:
                print("I wonder how I get into it?")
            elif "green fuse" in self.inventory:
                print("I might need that fuse.")
            else:
                print("I got the dumb thing open at least.")
        else:
            print("It's too dark to see.")

    def go_bunker(self):
        self.player_object.location = "bunker"

    def operate_safe(self):
        if self.light_switch:
            if not self.safe_opened:
                if self.player_object.mane_brushed:
                    print("I SUPPOSE YOU ARE CLEAN ENOUGH... FINE I'LL OPEN.\n")
                    print("Piece of junk... About damn time.")
                    self.inventory.append("green fuse")
                    self.player_object.increase_score()
                    self.safe_opened = True
                else:
                    print("The safe buzzes and a voice barks out.")
                    print("HEY, A SCRUFFY THING LIKE YOU CAN'T OPEN ME.\n")
                    print("What The fuck?\n")
                    print("YES, YOU. CLEAN YOURSELF UP IF YOU WANT ME TO OPEN.\n")
                    print("Great a talking safe. Always happy to find new pains in my tail.")
            else:
                print("It's already opened and I would prefer never to deal with it again.")
        else:
            print("It's too dark to see.")

    # gives item to player
    def get_item(self, item):
        if not self.light_switch:
            print("It's too dark to see.")
        elif item in self.inventory:
            if item == "map":
                print("Hey a map, this might help me out.")
            else:
                print(f"I got the {self.bold + item + self.end}.")
            self.inventory.remove(item)
            self.player_object.inventory.append(item)
        else:
            print(f"There isn't a(n) {item} to get.")

    # turns on light switch
    def turn_on_switch(self):
        if not self.light_switch:
            print("The light is on now!")
            self.light_switch = True
            self.player_object.increase_score()
        else:
            print("The switch is already on.")

    # uses computer in side room
    def use_computer(self):
        if self.light_switch:
            reading = True
            while reading:
                print("You have three emails. Select 1-4 and q to exit.")
                player_option = input("").lower()
                clear()
                if player_option == "q":
                    reading = False
                elif player_option == "1":
                    print("""The only way to save messages on ths computer is to email them to myself.
Oh well, It's something to help pass the time as I try and stay human.""")
                elif player_option == "2":
                    print("""We've managed to keep those mutants out for the time being. 
I hope that we can continue to survive down here. It's going to be a rough couple of months 
before the radiation dies down up top.""")
                elif player_option == "3":
                    print("""The damn door fuse blew again. We only have a few left and the fuse box is not 
getting any younger. I hope that Mike returns before too long.""")
                elif player_option == "4":
                    print("""I've used the last fuse in that robot out there. You'll need so strong tools to remove it.
Hopefully we don't need it for the door.""")
                else:
                    print("I should select a usable option. Stupid computers.")
        else:
            print("You can't see anything to use it.")


# Main Plaza Areas
class MainPlaza(FunctionClass):
    """Main plaza class. Acts as the hub that connects all the other areas together."""

    def __init__(self, player_object):
        self.inventory = ["map"]
        self.player_object = player_object
        self.upstairs_unlocked, self.car_looked, self.car_oper, self.desk_opened, self.phone_used = (False, False, False, False, False)
        self.look_dict = {
            "room": self.print_description_room,
            "car": self.print_description_car,
            "desk": self.print_description_desk,
            "pay phone": self.print_description_phone,
            "gate": self.print_description_door
        }

        self.go_dict = {
            "bunker": self.go_bunker,
            "exit": self.go_exit,
            "upstairs": self.go_upstairs,
            "west wing": self.go_west_wing,
            "small den": self.go_small_den
        }

        self.oper_dict = {
            "car": self.operate_car
        }

        self.use_dict = {
            "desk": self.open_desk,
            "gate": self.unlock_gate,
            "pay phone": self.use_phone
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nUpstairs unlocked {self.upstairs_unlocked}\nCar looked{self.car_looked}\nCar operated {self.car_oper}\nDesk opened {self.desk_opened}\nPhone used {self.phone_used}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("It's a large Main Plaza of the mall. There is a path to the 'west wing' too.")
        print("You emerge into the plaza of an old shopping mall. It is falling apart, "
              "\nwith much of the furnishings removed or smashed. Nature is starting to reclaim it too, judging by all "
              "\nthe foliage that’s popped up. There is an old 'car' parked nearby, for some strange reason."
              "\nThere is a 'desk' over by the main entrance near a 'payphone'.")
        if self.player_object.generator_working:
            print("The 'exit' is open! I can get out.")
        else:
            print("The 'exit' is locked and I'm trapped.")
        if self.upstairs_unlocked:
            print("I can get 'upstairs' now at least. The 'gate' is unlocked now.")
        else:
            print("The path 'upstairs' is shut for now. The 'gate' is locked.")
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_door(self):
        if not self.upstairs_unlocked:
            print("The gate is locked. You need to figure out how to open it.")
        elif self.upstairs_unlocked:
            print("You can go upstairs now at least.")
        else:
            print("It's open and you can go upstairs.")

    def print_description_desk(self):
        if not self.desk_opened:
            print("There's a old locked drawer here. I wonder how to get in.")
        elif "coin" in self.inventory:
            print("That coin is still there.")
        else:
            print("There's nothing else in the rotting desk.")

    def print_description_phone(self):
        if not self.phone_used:
            print("I wonder if it still works?")
        elif "blue fuse" in self.inventory:
            print("How did that get in there?")
        else:
            print("I know it does not work now...")

    def print_description_car(self):
        print("It's an old beat up Nissan Laurel. Not that you know what that is. It's seen better days.")
        if not self.car_looked:
            print("Hey this thing has a battery in it!")
            self.inventory.append("battery")
            self.car_looked = True
        elif "battery" in self.inventory:
            print("I should get the battery. Might come in handy.")
        else:
            print("I think I'm done messing with it.")

    def open_desk(self, item):
        if not self.desk_opened:
            if item == "screw driver":
                print("I got it open!")
                self.inventory.append("coin")
                self.desk_opened = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"I can't open it with a(n) {item}.")
        else:
            print("It's already opened.")

    def use_phone(self, item):
        if not self.phone_used:
            if item == "coin":
                print("Hey, something fell out when I tried to use it!")
                self.inventory.append("blue fuse")
                self.phone_used = True
                self.player_object.use_item(item)
                self.player_object.increase_score()

            else:
                print(f"I can use a(n) {item} with it.")
        else:
            print("It's not going to work all now.")

    def unlock_gate(self, item):
        if not self.upstairs_unlocked:
            if item == "keys":
                self.upstairs_unlocked = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"I can't unlock it with {item}.")
        else:
            print("The gate is unlocked already.")

    def go_upstairs(self):
        if self.upstairs_unlocked:
            self.player_object.location = "upstairs hallway"
        else:
            print("It's locked. I'll have to figure out how to get up there.")

    def go_exit(self):
        if self.player_object.generator_working:
            self.player_object.location = "exit"
        else:
            print("Right now the power is out, I'm trapped.")

    def go_west_wing(self):
        self.player_object.location = "west wing"

    def go_small_den(self):
        self.player_object.location = "small den"

    def go_bunker(self):
        self.player_object.location = "bunker"

    def operate_car(self):
        if not self.car_oper:
            print("It won't start but there are some odd keys in here.")
            self.inventory.append("strange keys")
            self.car_oper = True
        else:
            print("No point in trying to start it again.")


class SmallDen(FunctionClass):
    """A small animal pen that holds a dead animal and a workbench."""

    def __init__(self, player_object):

        self.inventory = []
        self.player_object = player_object
        self.workbench_items_needed = ("soldering iron", "soldering wire", "capacitor")
        self.workbench_inventory = []
        self.animal_cut, self.barn_looked, self.tool_repaired, self.have_parts = (False, False, False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "barn": self.print_description_barn,
            "animal": self.print_description_animal_body,
            "work bench": self.print_description_workbench
        }

        self.go_dict = {
            "main plaza": self.go_main_plaza
        }
        self.oper_dict = {
            "work bench": self.operate_work_bench
        }

        self.use_dict = {"work bench": self.give_missing_part,
                         "animal": self.animal_cutting
                         }

    def __str__(self):
        return f"""Inventory {self.inventory}\nWorkbench inventory {self.workbench_inventory}\nAnimal cut {self.animal_cut}\nBarn looked {self.barn_looked}\nHave parts {self.have_parts}\nTool fixed {self.tool_repaired}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print(
            "It's some small den... or maybe a corral? It's not totally clear. \nThere is a exit back the 'main plaza'.")
        print("There is a small 'barn' of some kind built from old doors and scrap.")
        print("There is a dead body of an 'animal' here.")
        if self.barn_looked:
            print("And a 'work bench' too.")
        self.print_look()
        self.print_locations()
        self.print_items()

    # print description of dead body
    def print_description_animal_body(self):
        print("It's a dead body of some grazing animal. Not one I really recognize.")
        if not self.animal_cut:
            print("Could be useful if I cut some meat off it.")
        elif "meat" in self.inventory:
            print("I might need that meat. Though I don't want to touch it.")
        else:
            print("There's a chunk missing now.")

    # prints description of barn
    def print_description_barn(self):
        print("It's a old barn of some sort.")
        if not self.barn_looked:
            self.barn_looked = True
            print("Hey, there's an old 'work bench' here.\nI bet I could repair something on it.")
        else:
            print("I wonder what the 'work bench' was for.")

    # prints description of work bench
    def print_description_workbench(self):
        print("It's a work bench with assortment of tools and materials.")
        if not self.tool_repaired:

            if len(self.workbench_inventory) < 3:
                print("I wonder if I can fix that circuit board?")
                print("Looks like I need...")
                for item in self.workbench_items_needed:
                    if item not in self.workbench_inventory:
                        print(f"a(n) {item}")
            else:
                print("I can fix the board now!")
        elif "circuit board" in self.inventory:
            print("I repaired it.")
        else:
            print("I don't think there's anything else to do here.")

    # gets missing parts to work bench
    def give_missing_part(self, item):
        if len(self.workbench_inventory) < 3:
            if item in self.workbench_items_needed:
                print("That's one part of this.")
                self.workbench_inventory.append(item)
                if len(self.workbench_inventory) == 3:
                    print("Hey, that's all I need!")
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"The {item} wouldn't help me.")
        else:
            print("It has everything it needs.")

    # if you have the parts you can repair the item
    def operate_work_bench(self):
        if not self.tool_repaired:
            if len(self.workbench_inventory) == 3:
                print("You fixed the board!")
                self.inventory.append("circuit board")
                self.tool_repaired = True
                self.player_object.increase_score()
            else:
                print("I still need more parts.")
        else:
            print("The board is fixed now.")

    # player trying to get a chunk of meat
    def animal_cutting(self, item):
        if not self.animal_cut:
            if item == "knife":
                print("I cut off a chunk of meat. Gross...")
                self.inventory.append("meat")
                self.animal_cut = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"I can't do any thing with the {item}.")
        else:
            print("It's already cut up. I'm done with it.")

    def go_main_plaza(self):
        self.player_object.location = "plaza"


# West Wing Areas
class WestWing(FunctionClass):
    """A hallway that connects to the western rooms."""

    def __init__(self, player_object):

        self.inventory = []
        self.player_object = player_object
        self.pet_shop_unlocked, self.vend_looked = (False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "vending machine": self.print_description_vending,
            "kiosk": self.print_description_kiosk
        }

        self.go_dict = {
            "main plaza": self.go_main_plaza,
            "pet shop": self.go_pet_shop,
            "toy shop": self.go_toy_shop,
            "cemetery": self.go_cemetery
        }
        self.oper_dict = {
        }

        self.use_dict = {"kiosk": self.unlock_pet_shop
                         }

    def __str__(self):
        return f"""Inventory {self.inventory}\nPet shop unlocked {self.pet_shop_unlocked}\nVending looked {self.vend_looked}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("To the west of the plaza sits the west wing. While it is quite dilapidated, it appears someone has "
              "\nmade an effort to clean the wing up a fair bit. There is a 'kiosk' nearby and a 'vending machine'.")
        if not self.pet_shop_unlocked:
            print("There is a 'kiosk' in front of the pet shop.")
            print("It is asking for a pet to allow entry.")
        else:
            print("The 'kiosk' is happy with your offering.")
        print("You can go to 'toy shop', 'main plaza', 'pet shop', and 'cemetery.")
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_kiosk(self):
        if not self.pet_shop_unlocked:
            print("It's a terminal to submit a pet for entering the shop. Old world store had theses a lot.")
            print("I usually just use my 'self' to fake my way past.")
        else:
            print("It's happy with the fur sample. Stupid thing...")

    def print_description_vending(self):
        print("It's a old and cracked machine. There is a flap on the front for getting things from it.")
        if not self.vend_looked:
            print("There's soda laying in it.")
            self.inventory.append("soda")
            self.vend_looked = True
        elif "soda" in self.inventory:
            print("That old soda is still here.")
        else:
            print("there's nothing else of value within it.")

    def go_pet_shop(self):
        if self.pet_shop_unlocked:
            self.player_object.location = "pet shop"
        else:
            print("The 'kiosk' is demanding something.")
            return False

    def go_toy_shop(self):
        self.player_object.location = "toy shop"

    def go_cemetery(self):
        self.player_object.location = "cemetery"

    def go_main_plaza(self):
        self.player_object.location = "plaza"

    def unlock_pet_shop(self, item):
        if not self.pet_shop_unlocked:
            if item == "fur sample":
                print("The shop accepted the sample as being a pet. You're in!")
                print("The doors slide open and allow you through.")
                self.pet_shop_unlocked = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            elif item == "self":
                print("Error. Exotic pets are not allowed. Including but not limited too: lions, bears, etc...")
                print("I guess I will have to find something else to get in...")
            else:
                print(f"It doesn't like the {item}.")
        else:
            print("It's already unlocked.")


class PetShop(FunctionClass):
    """The petshop class. attached to the west wing."""

    def __init__(self, player_object):
        self.inventory = ["mane brush"]
        self.player_object = player_object
        self.fish_looked, self.rope_fixed, self.fridge_checked = (False, False, False)
        self.look_dict = {
            "room": self.print_description_room,
            "fish": self.print_description_fish,
            "leash machine": self.print_description_leash_machine,
            "fridge": self.print_description_fridge,
            "shelves": self.print_description_selves
        }

        self.go_dict = {
            "west wing": self.go_west_wing
        }

        self.oper_dict = {}

        self.use_dict = {
            "leash machine": self.lengthen_rope
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nFish looked {self.fish_looked}\nRope fixed {self.rope_fixed}\nFridge checked {self.fridge_checked}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("It’s an old pet shop. Humans would go here with their pets to buy care products for whatever animal "
              "\nthey owned. While the pet 'displays' are now empty and smashed to bits, there are still plenty of useful "
              "\nthings for a lion like you. Though you aren’t too fond of having to go to a pet store to get anything "
              "\neven remotely useful for you. In the back room of the store there is a fish display 'tank'. You seem "
              "\noddly attracted to it...")
        print("There is a 'leash machine' off in one of the corners and a small 'fridge'.")
        if "mane brush" in self.inventory:
            print("I might need a clean up and that brush looks handy.")

        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_fish(self):
        if not self.fish_looked:
            self.inventory.append("fish")
            self.fish_looked = True
            print("Oh, there's a fish still alive in there.")
        elif "fish" in self.inventory:
            print("That fish looks tasty... No, Vern resist it.")
        else:
            print("I feel bad for taking the fish. Damn it.")

    def print_description_fridge(self):
        print("It's an old fridge and it's not very clean inside.")
        if not self.fridge_checked:
            print("Hey, what is this thing?")
            self.inventory.append("capacitor")
            print("And some catnip? uh on...")
            self.inventory.append("bag of catnip")
            self.fridge_checked = True

    @staticmethod
    def print_description_selves():
        print("They are ruined and there is nothing to get from them. Just old junk and random dog care products.")

    def go_west_wing(self):
        self.player_object.location = "west wing"

    def print_description_leash_machine(self):
        print("It's a machine to repair leases.")
        if self.rope_fixed:
            print("It broke after extending my rope. It's no good now.")
        else:
            print("It looks like it's still working.")

    def lengthen_rope(self, item):
        if not self.rope_fixed:
            if item == "rope":
                print("Suddenly, the motor in the machine starts to struggle, and then with a large bang, ceases to "
                      "work.")
                print("Hey, I got a much longer rope now!")
                self.inventory.append("long rope")
                self.rope_fixed = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"It rejected the {item}.")
        else:
            print("It's very broken and there's nothing else I can do with it.")


class ToyShop(FunctionClass):
    """The toyshop class. attached to the west wing."""

    def __init__(self, player_object):
        self.inventory = ["soldering wire"]
        self.player_object = player_object

        self.crane_fixed, self.crane_won, self.shelves_looked, self.locker_opened = (False, False, False, False)
        self.look_dict = {
            "room": self.print_description_room,
            "crane": self.print_description_crane,
            "locker": self.print_description_locker,
            "shelves": self.print_description_shelves
        }

        self.go_dict = {
            "west wing": self.go_west_wing
        }

        self.oper_dict = {
            "crane": self.operate_crane
        }

        self.use_dict = {
            "locker": self.open_locker,
            "crane": self.fix_crane
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nCrane fixed {self.crane_fixed}\nCrane won {self.crane_won}\nShelves looked {self.shelves_looked}\nLocker opened {self.locker_opened}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("It’s an old toy shop, full of things a parent would buy for their children. It’s a mess with old toys "
              "\nstrewn across the floor and 'shelves', many of which are now broken. There is a 'crane' machine that’s still "
              "\noperational after so long. As well as an old 'locker' behind the registers.")
        if "soldering wire" in self.inventory:
            print("There's old wire used to repair things here too.")
        print("You can go back to the 'west wing' from here.")
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_crane(self):
        print("It's an old crane machine.")
        if self.crane_won and "keys" not in self.inventory:
            print("You won the keys from it already.")
        elif "keys" in self.inventory:
            print("I should grab those keys.")
        else:
            print("There are a set of keys in the machine.")
        if self.crane_fixed:
            print("You have got the battery attached to it now.")
        elif not self.crane_won:
            print("There is a spot to attach things.")

    def print_description_shelves(self):
        print("There are a load of old toys and other bits and bobs.")
        print("What a pile of junk.")
        if not self.shelves_looked:
            print("There's a silly toy raygun. For some reason it makes you a little nervous.")
            self.inventory.append("toy raygun")
            self.shelves_looked = True
        elif "toy raygun" in self.inventory:
            print("That odd raygun is still here.")
        else:
            print("Just junk left now.")

    def print_description_locker(self):
        if not self.locker_opened:
            print("locked cabinet of sorts, with old toys from the old world, and there's a fuse in there")
        elif "red fuse" in self.inventory:
            print("I wonder what the fuse is for.")
        else:
            print("I beat the lock after all.")

    def go_west_wing(self):
        self.player_object.location = "west wing"

    def open_locker(self, item):
        if not self.locker_opened:
            if item == "circuit board":
                print("Hey it opened up!")
                self.locker_opened = True
                self.inventory.append("red fuse")
                print("And a tail? What is this?")
                self.inventory.append("toy lion tail")
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"This {item} is not helpful here.")
        else:
            print("It's already unlocked now.")

    def fix_crane(self, item):
        if not self.crane_fixed:
            if item == "battery":
                print("The crane is rigged to be won.\nNow I should try it again.")
                self.crane_fixed = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"I can't fix it was a(n) {item}.")
        else:
            print("It's working for the moment.")

    def operate_crane(self):
        if not self.crane_won:
            if self.crane_fixed:
                print("The keys dropped into the pail in the front.")
                self.inventory.append("keys")
                self.crane_won = True
                self.player_object.increase_score()
            else:
                print("You tried to get the keys out but the claw let them slip away.")
        else:
            print("There's nothing else in it you want.")


class Cemetery(FunctionClass):
    """The cemetery class. attached to the west wing."""

    def __init__(self, player_object):
        self.inventory = ["lion plush"]
        self.player_object = player_object
        self.first_entered, self.found_rope, self.grave_dug_up = (False, False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "graves": self.print_description_graves

        }

        self.go_dict = {
            "west wing": self.go_west_wing
        }

        self.oper_dict = {}

        self.use_dict = {
            "graves": self.dig_grave
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nFirst entered {self.first_entered}\nFound rope {self.found_rope}\nDug graves {self.grave_dug_up}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("You stumble into a makeshift cemetery. The atmosphere of the room makes you uneasy. At some point it "
              "\nused to be an outdoors food court, but it has become a 'grave' site for someone’s loved ones. The "
              "\nheadstones are made from old objects such as old car doors and hoods and signs.")
        print("You can go back to the 'west wing'.")
        if not self.first_entered:
            print("You don't think you should remove anything from here.")
            self.first_entered = True
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_graves(self):
        print("There are a lot of different graves here. Seems a large community both lived and died here.")
        if "lion plush" in self.inventory:
            print("On a child's grave hangs a little lion plushy.")
        if not self.found_rope:
            print("Hey, there's an old 'rope' here. Might come in handy if you dare to steal from a graveyard.")
            self.inventory.append("rope")
            self.found_rope = True
        elif "rope" in self.inventory:
            print("That rope is still here. I wonder what it was from.")
        else:
            print("There's not much here of value now.")

    def dig_grave(self, item):
        if not self.grave_dug_up:
            if item == "shovel":
                print("Please forgive me for this.")
                print("digging sounds...")
                time.sleep(2)
                print("Hey, this is not a grave it's a cache!")
                print("A fuse!")
                self.inventory.append("gold fuse")
                self.grave_dug_up = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"I can do anything with the {item}.")
        else:
            print("I have already dug that up.")

    def go_west_wing(self):
        self.player_object.location = "west wing"


# Upstairs Areas
class UpstairsHallway(FunctionClass):
    """The upstairs hallway that connects to the animal den, shoe store, and bathroom."""

    def __init__(self, player_object):
        self.inventory = []
        self.player_object = player_object
        self.book_looked, self.furniture_looked = (False, False)
        self.look_dict = {
            "room": self.print_description_room,
            "book": self.print_description_book,
            "furniture": self.print_description_furniture
        }

        self.go_dict = {
            "main plaza": self.go_main_plaza,
            "bathroom": self.go_bathroom,
            "shoe store": self.go_shoe_store,
            "animal den": self.go_animal_den
        }

        self.oper_dict = {
            "book": self.read_book}

        self.print_look()
        self.print_locations()
        self.use_dict = {}

    def __str__(self):
        return f"""Inventory {self.inventory}\nBook looked {self.book_looked}\nFurniture looked {self.furniture_looked}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("You climb up the old escalator onto the upper plaza of the mall. It appears someone lived here for "
              "\nsome time, judging by the repurposed 'furniture' and empty food packaging all over the floor. Whoever "
              "\nlived here defended it fiercely, judging by all the old casings and bullet holes.")
        print("You can go to 'down stairs', 'shoe store', 'animal den', and 'bathroom'.")
        self.print_look()
        self.print_locations()
        self.print_items()

    # for look furn
    def print_description_furniture(self):
        print("It's a bunch of stacked furniture made into a barricade. Someone was trying to defend this place.")
        if not self.furniture_looked:
            print("Hey, what is this this? A keyring?")
            self.inventory.append("cheetah keyring")
            self.furniture_looked = True
            print("And an old 'book' too...")
            if not self.book_looked:
                print("I wonder what's in it?")
        else:
            if "cheetah keyring" in self.inventory:
                print("What an odd keyring.")
            print("There is an old 'book'.")
            if not self.book_looked:
                print("I wonder what's in it?")

    # for look book
    def print_description_book(self):
        print("It's an old cracked 'book' that's stained with blood.")
        if not self.book_looked:
            print("I might want to read it. Maybe There's something useful inside.")

    # for oper book
    def read_book(self):
        reading = True
        if not self.book_looked:
            print("Time to take a look at this thing.")
            self.book_looked = True
        while reading:
            page = input("What page to read? (one, two, three, four, and end to quit reading.)\n")
            clear()
            if page == "one":
                print("This page looks earlier than the rest.")
                print("Martha changed today. She's one of those felines now. \nWe had to lock the pet shop for her own "
                      "good. We had to lock it against exotic animals. \nI'm still surprised it had that functionality "
                      "built in.")
                print("She's still the same woman I fell in love with but still. It feels wrong she's supposed to be "
                      "a human.")
                print("I'll have to make sure the others don't hurt her. They are getting worried and I don't like "
                      "\nhow they are looking at her.")

            elif page == "two":
                print(
                    "Things have gone well so far. I've helped Martha get used to not eating meat all the time again.")
                print("Poor sweetheart. She doesn't even remember being human at all.")
                print("What am I going to do?")

            elif page == "three":
                print("Others are changing too now. This is getting out of hand.")
                print(
                    "I had convinced the others that Martha couldn't infect them but now they aren't listening to me.")
                print("I can't let them hurt her. We survived the end together and")
                print("The journal ends suddenly here...")

            elif page == "four":
                print("This page is dated much older than the rest.")
                print(
                    "Hey, I found a sweet new place to live for a while. Gotta clean out all the old bodies first though.")
                print("Weird cat things. Everywhere they show up things go to shit.")
                # Vern talking to himself
                print("\nVern taps his foot on the ground and growls to himself.")
                print("Hey! jackass... Humans always seem to think themselves wonderful.")

            elif page == "end":
                print("I guess that's all I need from it.")
                reading = False
            else:
                print(f"I can't find page {page}.")

    def go_main_plaza(self):
        self.player_object.location = "plaza"

    def go_shoe_store(self):
        self.player_object.location = "shoe store"

    def go_animal_den(self):
        self.player_object.location = "animal den"

    def go_bathroom(self):
        self.player_object.location = "bathroom"


class AnimalDen(FunctionClass):
    """A upstairs animal den. Connected to the upstairs hallway."""

    def __init__(self, player_object):
        self.inventory = []
        self.player_object = player_object
        self.animal_counter = 0
        self.animal_drugged, self.entered_after_drugged, self.found_fur, self.meat_just_taken, self.hole_tried = (
            False, False, False, False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "animal": self.print_description_animal,
            "hole": self.print_description_hole
        }

        self.go_dict = {
            "hallway": self.go_hallway,
            "hole": self.enter_hole
        }

        self.oper_dict = {}

        self.use_dict = {}

    def __str__(self):
        return f"""Inventory {self.inventory}\nAnimal drugged {self.animal_drugged}\nEntered after drugged {self.entered_after_drugged}\nFound fur {self.found_fur}\nMeat just taken {self.meat_just_taken}\nHole tried {self.hole_tried}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("Once an old utility cabinet, it has now been claimed by some kind of animal. Judging by the sounds "
              "\ncoming from the den's 'hole' of a entrance, you feel you should probably avoid going in there directly.")
        if "meat" not in self.inventory and "drugged meat" not in self.inventory and not self.animal_drugged:
            print("With some sort of animal here I could lay a trap for it.")
        if not self.entered_after_drugged and self.animal_drugged:
            print("Hey, my trap worked!")
            self.entered_after_drugged = True
        if self.animal_drugged:
            print("Hey, looks like some sort of shaggy dog. Kinda fuzzy too, weird looking 'animal'.")
        elif self.meat_just_taken:
            print("It took my meat and left. I'll have to get more and use something on it.")
            self.meat_just_taken = False
        print("You can go back to the 'hallway'.")
        self.print_look()
        self.print_locations()
        self.print_items()

    # Vern talking about the odd hole in the wall
    def print_description_hole(self):
        if self.hole_tried:
            print("I'm never going in there again.")
        else:
            print("I wonder what's inside?")

    # talks about the animal
    def print_description_animal(self):
        if self.animal_drugged:
            print("it's a small animal. Pretty fuzzy too.")
            if not self.found_fur and "fur sample" in self.inventory:
                print("Hey, that fur might help me out.")
                self.found_fur = True
        else:
            print("I'm sure it's around but I can't see it right now.")

    # Vern enters the hole once and never again
    def enter_hole(self):
        if self.hole_tried:
            print("Nope. Never again...")
        else:
            print("Well I need to try everything I can.")
            print("Vern enters the hole only for a lot of yelling and roaring to echo out of it.")
            print("You Died...")
            time.sleep(5)
            print("Suddenly Vern crawls from the hole and drops to the ground.")
            print("Wow, that thing was not nice. It's a good thing that us lions can fight.")
            self.hole_tried = True

    # if this returns true it does not add the meat item back to the other room.
    # if it returns false then it adds it for the player to try again.
    def drug_animal(self):
        if "meat" in self.inventory:
            print("I should see if something took my bate in the animal den.")
            self.inventory.remove("meat")
            self.meat_just_taken = True
            return "meat"
        elif "drugged meat" in self.inventory:
            print("I should check my trap in the animal den.")
            self.inventory.remove("drugged meat")
            self.inventory.append("fur sample")
            self.animal_drugged = True
            return "drugged"
        else:
            return "none"

    def go_hallway(self):
        self.player_object.location = "upstairs hallway"


class Bathroom(FunctionClass):
    """A upstairs bathroom. Connected to the upstairs hallway."""

    def __init__(self, player_object):
        self.inventory = ["knife"]
        self.player_object = player_object

        self.looked_dryer, self.cabinet_looked = (False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "dryer": self.print_description_dryer,
            "graffiti": self.print_description_graffiti,
            "mirror": self.print_description_mirror,
            "medical cabinet": self.print_description_medical

        }

        self.go_dict = {
            "hallway": self.go_hallway,
        }

        self.oper_dict = {}

        self.use_dict = {}

    def __str__(self):
        return f"""Inventory {self.inventory}\nDryer looked {self.looked_dryer}\nCabinet looked {self.cabinet_looked}\n"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("It’s an old restroom. You can probably guess what "
              "\nwent on in here yourself. The old toilet blocks are heavily damaged and covered in 'graffiti'. The smell "
              "\nisn’t much better either. There is an old first aid 'cabinet' on the wall and a 'hand dryer' along side it. ")
        print("There is an old nasty looking 'mirror' on the wall.")
        print("You can go back to the 'hallway'.")
        self.print_look()
        self.print_locations()
        self.print_items()

    # bool will be if player has brushed mane
    def print_description_mirror(self):
        print("It's an old cracked mirror. Kinda dirty too...")
        if self.player_object.mane_brushed:
            print("At least I look nicer than I thought I did.")
        else:
            print("My mane needs to be cleaned up pretty badly.")

    def print_description_dryer(self):
        if not self.looked_dryer:
            print("You look over the dryer and accidentally turn it on.")
            print("Yikes!")
            print("Vern's fur frizzes up and he jumps back.")
            time.sleep(1)
            print("Dumb thing...")
            self.looked_dryer = True
        else:
            print("I'm not messing with it again.")

    @staticmethod
    def print_description_graffiti():
        print("It's a lot of crudely drawn shapes and messages.")
        print("You look it and try to make something out.")
        time.sleep(1)
        print("I respect your political beliefs even if I do not share them.")
        print("You look nice today!\nAnd 404167")
        print("Huh? Much nicer than you'd think it would have been.")

    def print_description_medical(self):
        if not self.cabinet_looked:
            print("Lots of nasty old bandages and... wait!\nSome useful drugs remain.")
            self.inventory.append("drugs")
            self.cabinet_looked = True
        elif "drugs" in self.inventory:
            print("I should get those drugs. Might need them for something.")
        else:
            print("There's nothing else of value here.")

    def go_hallway(self):
        self.player_object.location = "upstairs hallway"


class ShoeStore(FunctionClass):
    """A upstairs shoe store. Connected to the upstairs hallway."""

    def __init__(self, player_object):
        self.inventory = ["owl figurine", "screw driver"]
        self.player_object = player_object
        self.first_entered, self.elevator_opened, self.elevator_roped, self.weak_roped = (False, False, False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "elevator": self.print_description_elevator

        }

        self.go_dict = {
            "hallway": self.go_hallway,
            "elevator": self.go_elevator
        }

        self.oper_dict = {
            "elevator": self.operate_elevator_doors
        }

        self.use_dict = {
            "elevator": self.fix_elevator
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\n First entered {self.first_entered}\nElevator opened {self.elevator_opened}\nElevator roped {self.elevator_roped}\nWeak roped {self.weak_roped}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("It’s an old shoe store. It smells of musty leather and fabric. It used to be where a human would go to "
              "\nget some footwear, but now it appears someone had turned it into a living space, judging by the mess "
              "they’ve left.")
        if "screw driver" in self.inventory:
            print("There's a screw driver on the old shelves around the place.")

        if self.elevator_opened:
            print("The 'elevator' shaft is opened now.")
            if self.elevator_roped:
                print("You can climb down it now.")
            elif "rope" in self.inventory and self.weak_roped:
                print("I used a rope on it but I don't think it's long enough.")
            else:
                print("There's no way down just yet. You'll have to figure that out.")
        else:
            print("There is an old 'elevator' shaft but the doors are closed.")
        if not self.first_entered:
            print("You doubt anything would fit your digitigrade feet from this place.")
            self.first_entered = True

        print("You can go back the the 'hallway' from here.")
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_elevator(self):
        if not self.elevator_opened:
            print("It's closed right now. I wonder what's inside.")
        elif self.weak_roped:
            print("It's got a rope but I don't think it's long enough.")
        elif self.elevator_roped:
            print("I should be safe to go down now.")
        else:
            print("I need to figure out how to descend it.")

    # gives item to player
    def get_item(self, item):
        if item in self.inventory:
            if item == "rope" and self.weak_roped:
                print("I removed the short rope from the elevator.")
                self.weak_roped = False
            else:
                print(f"I got the {self.bold + item + self.end}.")
            self.inventory.remove(item)
            self.player_object.inventory.append(item)
        else:
            print(f"There isn't a(n) {item} to get.")

    def operate_elevator_doors(self):
        if not self.elevator_opened:
            print("I got the doors opened now.")
            self.elevator_opened = True
            self.player_object.increase_score()
        else:
            print("The doors are already opened.")

    # to fix the elevator
    # if you used the weak rope it adds it to the room inventory and flags you as having used the weak rope
    # if you use the strong rope it just removes the item and does marks you as having used the strong rope
    def fix_elevator(self, item):
        if not self.elevator_opened:
            print("I should open it first.")
        # if you have used either the weak or strong rope
        if self.weak_roped or self.elevator_roped:
            if self.weak_roped:
                print("I used a rope already but I should try and make the rope stronger.")
            else:
                print("It's ok for me to climb down now.")
        else:
            # if the item is the rope it adds to room inventory and flips the flag variable
            if item == "rope":
                print(f"I used the {item}. Maybe I can climb down.")
                self.inventory.append(item)
                self.weak_roped = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            # if strong rope just flips the strong rope flag
            elif item == "long rope":
                print(f"I used the {item}. Maybe I can climb down now.")
                self.elevator_roped = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print(f"I can use the {item} on the elevator.")

    # tries to go down the shaft. Fails if the strong rope is not used
    def go_elevator(self):
        # if the elevator has not being opened fail
        if not self.elevator_opened:
            print("I should open it first.")
        # if weak rope has been used and
        if self.weak_roped:
            print("I'm not going down that rope. It's not safe at all.")
        # if you used the strong rope then you can go
        elif self.elevator_roped:
            print("Ok, it looks safe... Maybe not but here I go.")
            self.player_object.location = "basement entry"
        else:
            print("I'll have to find a way to climb down it.")

    def go_hallway(self):
        self.player_object.location = "upstairs hallway"


# Basement Areas
class BasementEntry(FunctionClass):
    """A basement room that is attached to the shoe store."""

    def __init__(self, player_object):
        self.inventory = ["shovel"]
        self.player_object = player_object
        self.door_unlocked, self.soda_used = (False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "note": self.print_description_note,
            "pad": self.print_description_pad

        }

        self.go_dict = {
            "shoe store up": self.go_shoe_store,
            "generator room": self.go_gen_room
        }

        self.oper_dict = {
            "pad": self.entering_code
        }

        self.use_dict = {
            "pad": self.entering_code
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nDoor unlocked {self.door_unlocked}\n Soda used {self.soda_used}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("It's a dark basement lit only by emergency lights. There is a door with a electronic 'pad' lock across "
              "from you.")
        print("This place is not on the map... How strange.")
        if self.door_unlocked:
            print("The door is open and you can enter the 'generator room'.")
        else:
            print("You'll have to figure out how to open the door.")
        print("You can go back 'up' to the 'shoe store'.")
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_pad(self):
        print("It's an old electronic lock of some kind.")
        print("There's a small 'note' near it.")
        if not self.door_unlocked:
            print("I can't believe I found that password.")
        elif self.door_unlocked and self.soda_used:
            print("It's open now and pretty gross from the soda.")
        else:
            print("It's asking for a password.")

    def print_description_note(self):
        print("It reads: Don't get anything on this new lock you morons.")
        print("I have replaced it, but next time it's on your paycheck.")
        if self.soda_used:
            print("The note is splattered with soda.")
            print("The soda worked... Who knew?")
        else:
            print("I wonder what that means.")

    def go_gen_room(self):
        if self.door_unlocked:
            self.player_object.location = "basement generator room"
        else:
            print("The door is locked. I can't go there yet.")

    def go_shoe_store(self):
        self.player_object.location = "shoe store"

    # tries to enter codes or items to bypass the door.
    def entering_code(self, item=None):

        # only allows attempting to unlock if door is locked.
        if not self.door_unlocked:
            # if no item is give it asks for a password
            if item is None:
                password = ""
                print("It's asking for a password.")
                while len(password) < 6:
                    number = input("")
                    # counts through the player input and makes sure are only numbers.

                    if not number.isdigit():
                        print("ERROR!")
                        print("Oops! Wrong button.")

                    else:
                        password += number

                if password == "404167":
                    print("That Password is accepted. The door is open now!")
                    self.player_object.increase_score()
                    self.door_unlocked = True
                else:
                    print("That was not accepted... I wonder what the code is?")
            # if they used a soda.
            elif item == "soda":
                print("You dump the soda on the code box.")
                print("It fizzles and sparks. The door opens.\nHuh? Can't believe that worked.")
                self.door_unlocked = True
                self.soda_used = True
                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print("That doesn't help me...")
        else:
            print("It's open. I don't have to do anything else with it.")


class BasementGenRoom(FunctionClass):
    """A basement generator room that is attached to the shoe store."""

    def __init__(self, player_object):
        self.generator_inventory = []
        self.player_object = player_object
        self.inventory = ["soldering iron"]
        self.fuses_needed = ("green fuse", "red fuse", "blue fuse", "gold fuse")
        self.fuses_fixed, self.generator_working = (False, False)

        self.look_dict = {
            "room": self.print_description_room,
            "generator": self.print_description_generator,
            "spec sheet": self.print_description_spec
        }

        self.go_dict = {
            "basement entry": self.go_basement_entry
        }

        self.oper_dict = {
            "generator": self.operate_generator
        }

        self.use_dict = {
            "generator": self.add_item_generator
        }

    def __str__(self):
        return f"""Inventory {self.inventory}\nGenerator Inventory {self.generator_inventory}\nFuses fixed {self.fuses_fixed}"""

    # this prints a description along with a item list
    def print_description_room(self):
        print("This place is not on the map either... Maybe it just was not entered by the previous owners?.")
        print("Hey a large 'generator', maybe you can get it working?")
        print("There's a workbench with some scattered tools on it.")
        if "soldering iron" in self.inventory:
            print("That iron looks useful still.")
        if self.fuses_fixed:
            print("The power is on somewhere now. You should look around for it!")
        else:
            print("There is a large panel with spaces for four large fuses. You should keep your eyes out for them.")
            print("There is a 'spec' sheet by it you might want to take note of.")
        print("You can go back to the 'basement entry'")
        self.print_look()
        self.print_locations()
        self.print_items()

    def print_description_generator(self):
        print("It's a back up generator.")
        if self.generator_working:
            print("I got it working. I should check around and see what opened up. Maybe the exit is working again.")
        else:
            print("There are slots for four fuses. I need to find and insert them.")

    def print_description_spec(self):
        print("It lists the fuses I will need to fix the generator.")
        if len(self.generator_inventory) < 4:
            print("You still need:")
            for fuse in self.fuses_needed:
                if fuse not in self.generator_inventory:
                    print(f"A {fuse}")
        else:
            print("I got them all. Took long enough too...")

    def add_item_generator(self, item):
        if len(self.generator_inventory) < 4:
            if item in self.fuses_needed:
                if len(self.generator_inventory) < 3:
                    self.generator_inventory.append(item)
                    print(f"I added the {item} to the generator. Only {4 - len(self.generator_inventory)} Left to add.")
                else:
                    self.generator_inventory.append(item)
                    print(f"I added the {item} to the generator. That's the last one!")

                self.player_object.use_item(item)
                self.player_object.increase_score()
            else:
                print("I can't use that on the generator.")
        else:
            print("It's got all it needs. You should run it now.")

    def operate_generator(self):
        if not self.generator_working and len(self.generator_inventory) == 4:
            print("You flip the massive switch and the generator roars to life!")
            self.player_object.generator_working = True
            self.generator_working = True
            self.player_object.increase_score()
        elif not self.generator_working and len(self.generator_inventory) < 4:
            remainder = 4 - len(self.generator_inventory)
            print(f"It's missing {remainder} fuses still. You'll have to find them somewhere first.")
        else:
            print("It's already running.")

    def go_basement_entry(self):
        self.player_object.location = "basement entry"
