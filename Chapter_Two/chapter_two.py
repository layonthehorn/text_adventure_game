import pickle
import re
from os import path
import Chapter_Two.chapter_two_section_classes as sections
import pprint
import colorama

colorama.init()


class ChapterTwo:
    """This is a text adventure game, chapter one. All that is needed is to initialize it with a save directory and a
command to clear the screen."""

    under_line = "\033[4m"
    bold = colorama.Style.BRIGHT
    end = colorama.Style.NORMAL
    commands = "Verbs: look, inv(entory), time, wallet, get, oper(ate), com(bine), drop, score, use, go, save, end, help, stat"

    def __init__(self, save_dir, clear_func, testing=False):

        # setting if we allow debug options
        self.testing = testing
        self.playing = True
        # pattern matching for actions
        self.use_pattern = re.compile(r"^use\s|\swith\s|\son\s")
        self.combine_pattern = re.compile(r"^com\s|\swith\s|\son\s")

        # saving clear screen function
        self.clear = clear_func
        # getting save file location
        self.save_location = path.join(save_dir, "chapter_two.save")

        # player name
        self.player_name = "player"

        # special names
        self.exit_name = "exit"
        self.end_name = "end"
        self.stat_dictionary_name = "stat dictionary"

        choosing = True
        end_game = False
        while choosing:
            print("Chapter Two: Vern in the Big City.")
            player_option = input(
                "Load(l), Start New(s), Quit(q), or How to play(h)?\n"
            ).lower()
            if player_option == "s":
                # Loads defaults in classes for game
                self.player = sections.PlayerClass(testing)
                self.rooms = sections.RoomSystem(self.player)
                # sets NPC position
                self.rooms.set_up_npc()

                # to keep a running toll of all actions preformed
                self.stat_dictionary = {
                    "look": 0,
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
                    "stat": 0,
                    "time": 0,
                    "wallet": 0,
                }
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
                    # section data
                    self.rooms = new_value_dictionary.get("rooms")

                    # stat dictionary data
                    self.stat_dictionary = new_value_dictionary.get(
                        self.stat_dictionary_name
                    )

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
                # saving player
                self.player_name: self.player,
                # saving sections
                "rooms": self.rooms,
                # saving stats of actions made
                self.stat_dictionary_name: self.stat_dictionary,
            }

        # main game play loop
        while self.playing and not end_game:

            # if you reach the exit then don't ask for actions from player
            # or if he is asleep
            if self.player.location != self.exit_name and not self.player.sleep:
                if self.player.changed_location:

                    # displays the look rooms result when you change rooms
                    loc_name = self.rooms.switcher_dictionary.get(self.player.location)
                    loc_name.print_description_room()
                    self.player.changed_location = False

                # sleeping event checker
                self.rooms.time_wait_events()
                print("_" * len(self.commands))
                print(f"{self.bold + self.commands + self.end}")
                # checks for special events
                self.rooms.first_entered_events()
                player_choice = input("").lower()
                self.clear()
                # general actions shared by rooms
                self.general_actions(player_choice)

            # gets the room the player is in
            p_local = self.player.location

            if p_local == self.end_name:
                # ends game after player asks to
                self.end_game()
            elif p_local == self.exit_name:
                # Winning game ending
                self.clear()
                self.exit_game()

            # see if NPCs should move or not
            self.rooms.npc_movement_checker()
            if not self.player.sleep:
                print("")

    # end init function

    # saves games
    def save_game_state(self):
        try:
            # writes data to save file with pickle
            with open(self.save_location, "wb+") as db_file:
                pickle.dump(self.save_dictionary, db_file)
            print("Game has been saved!")
        except IOError:
            print("Could not open file for saving...")

    # loading saved game
    def load_game_state(self):
        try:
            with open(self.save_location, "rb") as db_file:
                pickle_db = pickle.load(db_file)
                return pickle_db
        except FileNotFoundError:
            return None

    # general actions that can be done anywhere
    def general_actions(self, action):
        # finds player location
        # this makes all your actions dependent on the room you are in
        loc_name = self.rooms.switcher_dictionary.get(self.player.location)
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

        # allows you to check how much cash you have
        elif general_list[0] == "wallet":
            self.stat_dictionary["wallet"] += 1
            print(f"I have {self.player.player_wallet} coins.")

        # gives a hint
        elif general_list[0] == "hint":
            self.stat_dictionary["hint"] += 1
            self.hint_system()

        # prints help page
        elif general_list[0] == "help":
            self.stat_dictionary["help"] += 1
            self.print_help()

        elif general_list[0] == "time":
            print(self.rooms.clock)
            self.stat_dictionary["time"] += 1

        # for debugging only
        # disabled by default
        elif general_list[0] == "debug":
            if self.testing:
                pick = input("Player, room, or npc? ").lower()
                if pick == "player":
                    self.clear()
                    pprint.pprint(vars(self.player))
                    self.player.debug_player()
                elif pick == "room":
                    self.clear()
                    pprint.pprint(vars(loc_name))
                elif pick == "npc":
                    self.clear()
                    self.rooms.debug_npc()
                else:
                    self.clear()
                    print("Cannot debug print that.")
            else:
                self.stat_dictionary["unknown"] += 1
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
            print(
                "Vern taps his foot on the ground. \n'I get so sick of waiting for something to happen.'"
            )

        # ends game and asks to save
        elif general_list[0] == "end":
            self.stat_dictionary["end"] += 1
            save = input("Save game? (y/n) ").lower()
            if save == "y":
                self.stat_dictionary["save"] += 1
                print("Saved!")
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
                if general_list[1] != "self":
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
            if "" in choice_list:
                choice_list.remove("")
            try:
                self.player.combine_items(choice_list[0], choice_list[1])
            except IndexError:
                print("Combine what with what?")

        # using items on objects
        elif general_list[0] == "use":
            self.stat_dictionary["use"] += 1
            try:
                choice_list = self.use_pattern.split(action)
                if "" in choice_list:
                    choice_list.remove("")
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
        pass

    # prints usage statement to players in game
    @staticmethod
    def print_help():
        print("How to play.")
        print(
            "look {item}: Looks at things. room, map, objects."
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
            "\nstat: Prints stats on commands used."
        )

    def print_intro(self):
        self.clear()
        print(
            """
After a week of travelling from the abandoned mall, Vern, Johnson and Katie arrived at the city of Harrisburg. 
They were relieved to have finally arrived, as they were in need of supplies, a clean up and a feed. 
However, this relief was short lived, when Vern realised that his money pouch had got a hole along the way, 
and had managed to lose all the money they had. After a short argument, the group agreed to try 
and make back the money they lost by seeing what they could do for the residents of the city, 
hoping to raise $5000 to get them through to their next destination.
"""
        )

    def print_outro(self):

        print("""""")
        self.print_stats()

    # a formatted print of all commands that have been used
    def print_stats(self):
        print(
            f"""
\t\t\t\t\tStatistics Of Command Usage

{"Used 'look'":<16} {self.stat_dictionary["look"]:<4} times. {"":>6} {"Used 'get'":<16} {self.stat_dictionary["get"]:<4} times.
{"Used 'inventory'":<16} {self.stat_dictionary["inventory"]:<4} times. {"":>6} {"Used 'help'":<16} {self.stat_dictionary["help"]:<4} times.
{"Used 'end'":<16} {self.stat_dictionary[""]:<4} times. {"":>6} {"Used 'operate'":<16} {self.stat_dictionary["operate"]:<4} times.
{"Used 'time'":<16} {self.stat_dictionary["time"]:<4} times. {"":>6} {"Used 'wallet'":<16} {self.stat_dictionary["wallet"]:<4} times.
{"Used 'combine'":<16} {self.stat_dictionary["combine"]:<4} times. {"":>6} {"Used 'drop'":<16} {self.stat_dictionary["drop"]:<4} times.
{"Used 'score'":<16} {self.stat_dictionary["score"]:<4} times. {"":>6} {"Used 'use'":<16} {self.stat_dictionary["use"]:<4} times.
{"Used 'go'":<16} {self.stat_dictionary["go"]:<4} times. {"":>6} {"Used 'save'":<16} {self.stat_dictionary["save"]:<4} times.
{"Used 'hint'":<16} {self.stat_dictionary["hint"]:<4} times. {"":>6} {"Used 'stat'":<16} {self.stat_dictionary["stat"]:<4} times.
{"Unknown command":<16} {self.stat_dictionary["unknown"]:<4} times. {"":>6} {"Entered nothing":<16} {self.stat_dictionary[""]:<4} times."""
        )
