import pickle
import re
from os import path
from Chapter_One.chapter_one_classes import PlayerClass, Bunker, ComputerRoom, MainPlaza, SmallDen, WestWing, ToyShop, PetShop, Cemetery, UpstairsHallway, AnimalDen, Bathroom, ShoeStore, BasementEntry, BasementGenRoom
import colorama
colorama.init()


class ChapterOne:
    """This is a text adventure game, chapter one. All that is needed is to initialize it with a save directory and a
command to clear the screen."""
    under_line = '\033[4m'
    bold = colorama.Style.BRIGHT
    end = colorama.Style.NORMAL
    commands = 'Verbs look, inv(entory), get, oper(ate), com(bine), drop, score, use, go, save, end, help, stat'

    def __init__(self, save_dir, clear_func, testing=False):

        # setting if we allow debug options
        self.testing = testing
        # pattern matching for actions
        self.use_pattern = re.compile(r"^use\s|\swith\s|\son\s")
        self.combine_pattern = re.compile(r"^com\s|\swith\s|\son\s")

        # saving clear screen function
        self.clear = clear_func
        # getting save file location
        self.save_location = path.join(save_dir, "chapter_one.save")

        # building the rooms and player names
        self.player_name = "player"
        self.main_plaza_name = "plaza"
        self.starting_room_name = "bunker"
        self.side_room_name = "side room"
        self.small_den_name = "small den"
        self.west_wing_name = "west wing"
        self.cemetery_name = "cemetery"
        self.toy_shop_name = "toy shop"
        self.pet_shop_name = "pet shop"
        self.exit_name = "exit"
        self.end_name = "end"
        self.up_stairs_hallway_name = "upstairs hallway"
        self.animal_den_name = "animal den"
        self.shoe_store_name = "shoe store"
        self.bathroom_name = "bathroom"
        self.basement_entryway_name = "basement entry"
        self.basement_gen_room_name = "basement generator room"
        self.stat_dictionary_name = "stat dictionary"
        self.playing = True

        # Main Classes
        # These are loaded below as to not load them twice.
        # self.player - The player character class
        # self.starting_room - the bunker room class
        # self.side_room - the computer room to the side of the bunker class
        # self.main_plaza - the area outside the bunker # self.cemetery - the area north of the west wing.
        # self.west_wing - a side area used to reach more places
        # self.toy_shop - the toy shop off of the west wing
        # self.pet_shop - A pet shot off of the west wing
        # self.up_stairs_hallway - the upstairs hallway
        # self.animal_den - the upstairs den
        # self.shoe_store - the shoe store up stairs
        # self.bathroom - the bathroom upstairs
        # self.basement_entry - where you have to go to finish the game
        # self.basement_gen_room - where you turn on the power.

        choosing = True
        end_game = False
        while choosing:
            print("Chapter One: The Lost Mall")
            player_option = input("Load(l), Start New(s), Quit(q), or How to play(h)?\n").lower()
            if player_option == "s":
                # Loads defaults in classes for game
                self.player = PlayerClass()
                self.starting_room = Bunker(self.player)
                self.side_room = ComputerRoom(self.player)
                self.main_plaza = MainPlaza(self.player)
                self.small_den = SmallDen(self.player)
                self.west_wing = WestWing(self.player)
                self.cemetery = Cemetery(self.player)
                self.toy_shop = ToyShop(self.player)
                self.pet_shop = PetShop(self.player)
                self.up_stairs_hallway = UpstairsHallway(self.player)
                self.animal_den = AnimalDen(self.player)
                self.shoe_store = ShoeStore(self.player)
                self.bathroom = Bathroom(self.player)
                self.basement_entryway = BasementEntry(self.player)
                self.basement_gen_room = BasementGenRoom(self.player)
                # to keep a running toll of all actions preformed
                self.stat_dictionary = {"look": 0,
                                        "inventory": 0,
                                        "get": 0,
                                        "help": 0,
                                        "": 0,
                                        "operate": 0,
                                        "combine": 0,
                                        "drop": 0,
                                        "score": 0,
                                        "use": 0,
                                        "go": 0,
                                        "save": 0,
                                        "hint": 0,
                                        "end": 0,
                                        "unknown": 0,
                                        "stat": 0}
                self.print_intro()
                choosing = False
            elif player_option == "q":
                choosing = False
                end_game = True
            elif player_option == "l":
                self.clear()
                # getting loaded settings
                new_value_dictionary = self.load_game_state()
                # if the dictionary is none it can not load a game
                if new_value_dictionary is None:
                    print("No save games found.")
                else:

                    # loading saved settings for classes
                    # player data
                    self.player = new_value_dictionary.get(self.player_name)
                    # bunker data
                    self.starting_room = new_value_dictionary.get(self.starting_room_name)
                    # side room data
                    self.side_room = new_value_dictionary.get(self.side_room_name)
                    # main plaza data
                    self.main_plaza = new_value_dictionary.get(self.main_plaza_name)
                    # small den data
                    self.small_den = new_value_dictionary.get(self.small_den_name)
                    # west wing data
                    self.west_wing = new_value_dictionary.get(self.west_wing_name)
                    # cemetery data
                    self.cemetery = new_value_dictionary.get(self.cemetery_name)
                    # toy shop data
                    self.toy_shop = new_value_dictionary.get(self.toy_shop_name)
                    # pet shop data
                    self.pet_shop = new_value_dictionary.get(self.pet_shop_name)
                    # upstairs hallway data
                    self.up_stairs_hallway = new_value_dictionary.get(self.up_stairs_hallway_name)
                    # animal den data
                    self.animal_den = new_value_dictionary.get(self.animal_den_name)
                    # bathroom data
                    self.bathroom = new_value_dictionary.get(self.bathroom_name)
                    # shoe store data
                    self.shoe_store = new_value_dictionary.get(self.shoe_store_name)
                    # basement entryway data
                    self.basement_entryway = new_value_dictionary.get(self.basement_entryway_name)
                    # basement generator room data
                    self.basement_gen_room = new_value_dictionary.get(self.basement_gen_room_name)
                    # stat dictionary data
                    self.stat_dictionary = new_value_dictionary.get(self.stat_dictionary_name)

                    # tells player it loaded the game
                    print("Loaded Game.")
                    print(f"You are in the {self.player.location} area.")
                    choosing = False

            # prints instructions
            elif player_option == "h":
                self.print_help()

        # location dictionary
        # used for general actions to run player actions in any room.
        # if the player is going to actually play builds rest of game
        if not end_game:

            # dictionary for saving game state
            self.save_dictionary = {
                # player only here for saving
                self.player_name: self.player,
                self.starting_room_name: self.starting_room,
                self.side_room_name: self.side_room,
                self.main_plaza_name: self.main_plaza,
                self.west_wing_name: self.west_wing,
                self.cemetery_name: self.cemetery,
                self.pet_shop_name: self.pet_shop,
                self.toy_shop_name: self.toy_shop,
                self.small_den_name: self.small_den,
                self.up_stairs_hallway_name: self.up_stairs_hallway,
                self.shoe_store_name: self.shoe_store,
                self.animal_den_name: self.animal_den,
                self.bathroom_name: self.bathroom,
                self.basement_gen_room_name: self.basement_gen_room,
                self.basement_entryway_name: self.basement_entryway,
                self.stat_dictionary_name: self.stat_dictionary
            }

            # switcher dictionary for running actions
            self.switcher_dictionary = {
                self.starting_room_name: self.starting_room,
                self.side_room_name: self.side_room,
                self.main_plaza_name: self.main_plaza,
                self.west_wing_name: self.west_wing,
                self.cemetery_name: self.cemetery,
                self.pet_shop_name: self.pet_shop,
                self.toy_shop_name: self.toy_shop,
                self.small_den_name: self.small_den,
                self.up_stairs_hallway_name: self.up_stairs_hallway,
                self.shoe_store_name: self.shoe_store,
                self.animal_den_name: self.animal_den,
                self.bathroom_name: self.bathroom,
                self.basement_gen_room_name: self.basement_gen_room,
                self.basement_entryway_name: self.basement_entryway
            }

        # main game play loop
        while self.playing and not end_game:

            # if you reach the exit then don't ask for actions from player
            if self.player.location != self.exit_name:

                if self.player.changed_location:

                    # displays the look rooms result when you change rooms
                    loc_name = self.switcher_dictionary.get(self.player.location)
                    loc_name.print_description_room()
                    self.player.changed_location = False
                print("_" * len(self.commands))
                print(f"{self.bold + self.commands + self.end}")
                player_choice = input("").lower()
                self.clear()
                # general actions shared by rooms
                self.general_actions(player_choice)

            # gets the room the player is in
            p_local = self.player.location
            if p_local != self.end_name and p_local != self.exit_name:

                # if the player is in the animal den it checks if it needs to run the
                # checking if they placed the meat in the animal den
                if p_local == self.up_stairs_hallway_name:
                    result = self.animal_den.drug_animal()
                    if result == "meat":
                        self.small_den.give_item("meat")
                    elif result == "drugged":
                        self.player.increase_score()

            elif p_local == self.end_name:
                # ends game after player asks to
                self.end_game()
            else:
                # Winning game ending
                self.clear()
                self.exit_game()
            print("")

# end init function

    # saves games
    def save_game_state(self):
        try:
            # writes data to save file with pickle
            with open(self.save_location, 'wb+') as db_file:
                pickle.dump(self.save_dictionary, db_file)
            print("Game has been saved!")
        except IOError:
            print("Could not open file for saving...")

    # loading saved game
    def load_game_state(self):
        try:
            with open(self.save_location, 'rb') as db_file:
                pickle_db = pickle.load(db_file)
                return pickle_db
        except FileNotFoundError:
            return None

    # general actions that can be done anywhere
    def general_actions(self, action):
        # finds player location
        # this makes all your actions dependent on the room you are in
        loc_name = self.switcher_dictionary.get(self.player.location)
        # splits the input on the first space
        general_list = action.split(" ", 1)

        # prints inventory
        if general_list[0] == "inv":
            self.stat_dictionary["inventory"] += 1
            self.player.check_inventory()

        # lists the stats of what commands you have used
        elif general_list[0] == "stat":
            self.stat_dictionary["stat"] += 1
            self.print_stats()

        # gives a hint
        elif general_list[0] == "hint":
            self.stat_dictionary["hint"] += 1
            self.hint_system()

        # prints help page
        elif general_list[0] == "help":
            self.stat_dictionary["help"] += 1
            self.print_help()

        # for debugging only
        # disabled by default
        elif general_list[0] == "debug":
            if self.testing:
                pick = input("Player or room? ").lower()
                if pick == "player":
                    self.clear()
                    print(self.player)
                    self.player.debug_player()
                elif pick == "room":
                    self.clear()
                    print(loc_name)
                else:
                    self.clear()
                    print("Cannot debug print that.")
            else:
                print(f"I don't know how to {general_list[0]}.")

        # saves the game
        elif general_list[0] == "save":
            self.stat_dictionary["save"] += 1
            self.save_game_state()

        # prints score
        elif general_list[0] == "score":
            self.stat_dictionary["score"] += 1
            self.player.print_score()

        # in case input is blank
        elif action == "":
            self.stat_dictionary[""] += 1
            print("Vern taps his foot on the ground. \n'I get so sick of waiting for something to happen.'")

        # ends game and asks to save
        elif general_list[0] == "end":
            self.stat_dictionary["end"] += 1
            save = input("Save game? (y/n) ").lower()
            if save == 'y':
                self.stat_dictionary["save"] += 1
                print('Saved!')
                self.save_game_state()
            input("Press enter to quit. Goodbye! ")
            self.player.location = self.end_name

        # looking at things
        elif general_list[0] == "look":
            self.stat_dictionary["look"] += 1
            try:
                if general_list[1] == "map":
                    self.player.look_player_map()
                # looks at self
                elif general_list[1] == "self":
                    self.player.look_self()
                else:
                    loc_name.get_look_commands(general_list[1])
            except IndexError:
                print("Look at what?")

        # gets an item from the current room
        elif general_list[0] == "get":
            self.stat_dictionary["get"] += 1
            try:
                loc_name.get_item(general_list[1])
            except IndexError:
                print("Get what?")

        # drops item to current room
        elif general_list[0] == "drop":
            self.stat_dictionary["drop"] += 1
            try:
                # if player tries to drop self print message.
                if general_list[1] != 'self':
                    loc_name.drop_item(general_list[1])
                else:
                    print("Now how would I do that?")
            except IndexError:
                print("Drop what?")

        # combining items
        elif general_list[0] == "com":
            self.stat_dictionary["combine"] += 1
            # tries to combine items
            choice_list = self.combine_pattern.split(action)
            if '' in choice_list:
                choice_list.remove('')
            try:
                self.player.combine_items(choice_list[0], choice_list[1])
            except IndexError:
                print("Combine what with what?")

        # using items on objects
        elif general_list[0] == "use":
            self.stat_dictionary["use"] += 1
            try:
                choice_list = self.use_pattern.split(action)
                if '' in choice_list:
                    choice_list.remove('')
                loc_name.get_use_commands(choice_list)

            except IndexError:
                print("Use what with what?")

        # operating objects
        elif general_list[0] == "oper":
            self.stat_dictionary["operate"] += 1
            try:
                loc_name.get_oper_commands(general_list[1])

            except IndexError:
                print("Operate what?")

        # going to new areas.
        elif general_list[0] == "go":
            self.stat_dictionary["go"] += 1
            try:
                loc_name.get_go_commands(general_list[1])
            except IndexError:
                print("Go where?")

        # in case you did not have match
        else:
            self.stat_dictionary["unknown"] += 1
            print(f"I don't know how to {general_list[0]}.")

    # a winning game function
    def exit_game(self):
        self.print_outro()
        self.player.print_score()
        input("Press enter to exit Chapter One.\nThank you for playing! ")
        self.end_game()

    # a end game function
    def end_game(self):
        self.playing = False

    # hint system for cheaters
    def hint_system(self):
        if not self.starting_room.robot_fixed:
            print("You should find a way to get that fuse loose.")
        elif not self.starting_room.fuse_box:
            print("Keep playing for more hints.")
        elif not self.starting_room.door_opened:
            print("Keep playing for more hints.")
        elif not self.main_plaza.car_looked:
            print("You should look over that car.")
        elif not self.toy_shop.crane_fixed:
            print("Keep playing for more hints.")
        elif not self.toy_shop.crane_won:
            print("Keep playing for more hints.")
        elif not self.main_plaza.upstairs_unlocked:
            print("Maybe you have some keys that would help you now.")
        elif not self.small_den.animal_cut:
            print("Getting some meat would be a good idea.")
        elif not self.bathroom.cabinet_looked:
            print("Keep playing for more hints.")
        elif not self.animal_den.animal_drugged:
            print("Maybe place that meat somewhere?")
        elif not self.west_wing.pet_shop_unlocked:
            print("What can you use to unlock the pet store?")
        elif not self.cemetery.found_rope:
            print("Keep playing for more hints.")
        elif not self.pet_shop.rope_fixed:
            print("What is like a leash?")
        elif not self.shoe_store.elevator_opened:
            print("Keep playing for more hints.")
        elif not self.shoe_store.elevator_roped:
            print("What would help with getting down long falls?")
        elif not self.basement_entryway.door_unlocked:
            print("There's a code somewhere, or you could try and fry the lock.")
        elif len(self.basement_gen_room.generator_inventory) < 4:
            print("You need to get four fuses to fix the generator")
            print("Check around the other places you have been before.")
        elif self.main_plaza.exit_unlocked:
            print("The exit is open now.")
        else:
            print("Keep playing for more hints.")

    # prints usage statement to players in game
    @staticmethod
    def print_help():
        print("How to play.")
        print("look {item}: Looks at things. room, map, objects."
              "\ninv(entory): Checks your inventory and prints descriptions out."
              "\nget {item}: Gets items from room."
              "\noper(ate) {object}: How you use/read objects: doors, computers, etc."
              "\ncom(bine) {item} with/on {item}: allows you to combine items. Use 'self' to use an item on you."
              "\ndrop {item}: Allows you to get rid of an item."
              "\nscore: Allows the player to check current progress in-game."
              "\nuse {item} With/on {item}: how you use things with other things."
              "\ngo {location}: How you change rooms."
              "\nsave: How you save your game."
              "\nend: Exit game and will ask to save or not."
              "\nhint: This will give you a hint on how to continue."
              "\nhelp: This menu."
              "\nstat: Prints stats on commands used.")

    def print_intro(self):
        self.clear()
        print(""" 
    Vern the lion was traveling with his friend Johnson and his daughter Katie. 
    On their way to Harrisburg, they stopped for the night and he shared a drink with his friend. 
    Things got out of hand and one drink turned into many. 
    The next thing Vern knew he woke up with a massive headache in a strange place.

    You wake up, alone and afraid in an old fallout shelter, built some time in the past, but abandoned 
    long ago. It appears a group had set themselves up here before the end, judging by the things that were left 
    behind. The room smells of mould and rust. There is a disabled robot in the corner, an entry to a smaller 
    room and there is a door that appears to be locked.
    """)

    def print_outro(self):
        if "toy lion tail" in self.player.inventory:
            print("""
Vern escapes the mall and reunites with Johnson and Katie. After a debriefing between them 
and giving Katie the toy lion tail, they continued onwards to Harrisburg. 
Hopefully, There would be no complications there.""")
        else:
            print("""
Vern escapes the mall and reunites with Johnson and Katie. After a debriefing between them, 
they continued onwards to Harrisburg. Hopefully, There would be no complications there.""")
        self.print_stats()

    # a formatted print of all commands that have been used
    def print_stats(self):
        print(f"""
\t\t\t\t\tStatistics Of Command Usage

{"Used 'look'":<16} {self.stat_dictionary["look"]:<4} times. {"":>6} {"Used 'get'":<16} {self.stat_dictionary["get"]:<4} times.
{"Used 'inventory'":<16} {self.stat_dictionary["inventory"]:<4} times. {"":>6} {"Used 'help'":<16} {self.stat_dictionary["help"]:<4} times.
{"Used 'end'":<16} {self.stat_dictionary[""]:<4} times. {"":>6} {"Used 'operate'":<16} {self.stat_dictionary["operate"]:<4} times.
{"Used 'combine'":<16} {self.stat_dictionary["combine"]:<4} times. {"":>6} {"Used 'drop'":<16} {self.stat_dictionary["drop"]:<4} times.
{"Used 'score'":<16} {self.stat_dictionary["score"]:<4} times. {"":>6} {"Used 'use'":<16} {self.stat_dictionary["use"]:<4} times.
{"Used 'go'":<16} {self.stat_dictionary["go"]:<4} times. {"":>6} {"Used 'save'":<16} {self.stat_dictionary["save"]:<4} times.
{"Used 'hint'":<16} {self.stat_dictionary["hint"]:<4} times. {"":>6} {"Used 'stat'":<16} {self.stat_dictionary["stat"]:<4} times.
{"Unknown command":<16} {self.stat_dictionary["unknown"]:<4} times. {"":>6} {"Entered nothing":<16} {self.stat_dictionary[""]:<4} times.""")
