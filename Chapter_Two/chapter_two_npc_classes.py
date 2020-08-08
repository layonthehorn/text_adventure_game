from abc import ABC, abstractmethod
from Chapter_Two.exception_class import ReadOnlyError, ChangeNPCLocationError
import os
import platform


# allows me to clear the screen when playing
def clear():
    operating = platform.system()
    if operating == 'Linux' or operating == "Darwin":
        os.system("clear")
    elif operating == 'Windows':
        os.system('cls')


# a shop class for inheritance
class ShopFunctions:
    """A class for giving shops the needed functions."""
    # class variables for print formatting
    bold = '''\033[1m'''
    end = '''\033[0;0m'''

    # general shop keeper function
    def shop_keeper(self, message="Welcome to my shop!"):
        talking = True
        print(message)
        while talking:
            print("\nSell(s), Buy(b), or Quit(q)?")
            choice = input("").lower()
            clear()
            if choice == "s":
                self.sell_items()
            elif choice == "b":
                self.buy_items()
            elif choice == "q":
                print("Please come again.")
                talking = False
            else:
                print(f"What do you mean by {choice}.")

    # allows you to sell things
    def sell_items(self):
        talking = True
        while talking:
            if len(self.player.inventory) > 1:
                items_sell = []
                for item in self.player.inventory:
                    if item in self.player.sell_item_values:
                        items_sell.append(item)
                # if list is not empty allow selling
                if items_sell:
                    for number, item in enumerate(items_sell):
                        print(item, end=", ")
                        if (number + 1) % 4 == 0:
                            print("")
                    print("\n")
                    choice = input("\nSell what? q to quit. ").lower()
                    clear()
                    # if you do not have the thing you are trying to sell
                    if choice not in self.player.inventory and choice != "q":
                        print(f"You don't have a(n) {self.bold + choice + self.end} to sell")
                    # if the item has a value in game
                    elif choice in self.player.sell_item_values:
                        print("I'll take that. Thank you!")
                        # sells it
                        self.sell(choice)
                    elif choice == "q":
                        talking = False
                    else:
                        print(f"I don't want to buy a(n) {self.bold + choice + self.end}")
                else:
                    print("You don't have anything I want to buy.")
                    talking = False

            else:
                print("You don't have anything to sell.")
                talking = False

    # allows you to buy things
    def buy_items(self):
        talking = True
        while talking:
            if len(self.shop_inventory) > 0:
                for number, item in enumerate(self.shop_inventory):
                    print(item, end=", ")
                    if (number + 1) % 4 == 0:
                        print("")
                print("\n")
                choice = input("\nBuy what? q to quit. ").lower()
                clear()
                # if they have it to sell you
                if choice in self.shop_inventory:
                    # if you have enough money
                    if self.player.player_wallet >= self.player.buy_item_values.get(choice):
                        self.buy(choice)
                    else:
                        # if you are too poor
                        print(f"You can't afford the {self.bold + choice + self.end}. You need {self.player.buy_item_values.get(choice) - self.player.player_wallet}.")
                elif choice == "q":
                    talking = False
                else:
                    print(f"I don't have a(n) {self.bold + choice + self.end} to sell you.")
            else:
                print("I am totally out of things to sell you.")
                talking = False

    # controls selling items
    def sell(self, item):
        self.player.inventory.remove(item)
        if item in self.player.buy_item_values:
            self.shop_inventory.append(item)
        print(f"You sold the {self.bold + item + self.end}.")
        self.player.change_player_wallet(self.player.sell_item_values.get(item, 0))

    # controls buying items
    def buy(self, item):
        self.player.inventory.append(item)
        self.shop_inventory.remove(item)
        print(f"You bought the {self.bold + item + self.end}.")
        self.player.change_player_wallet(self.player.buy_item_values.get(item, 0))


class NPC(ABC):
    """A base class to create NPCs from.

    init should look like this.

    def __init__(self, timer, player):
        self.player = player
        self.clock = timer
        self.__position = "ruined street"
        self.__alive = True
        self.name = "scavenger"
        self.inventory = []
  """

    @abstractmethod
    def talk_to_npc(self):
        pass

    @abstractmethod
    def look_npc(self):
        pass

    def check_move(self):
        return False

    @abstractmethod
    def use_item(self, item):
        pass

    def __str__(self):
        return f"My name is {self.name}, I'm in {self.position}, and it is {self.clock}."

    @property
    @abstractmethod
    def position(self):
        pass

    @position.setter
    @abstractmethod
    def position(self, value):
        pass

    @property
    @abstractmethod
    def alive(self):
        pass

    @alive.setter
    @abstractmethod
    def alive(self, new_value):
        pass


class ScavengerNPC(NPC):
    """A scavenger that moves from the ruins to the general store and back."""
    def __init__(self, timer, player):
        self.player = player
        self.clock = timer
        self.__position = "ruined street"
        self.__alive = True
        self.name = "scavenger"
        self.inventory = []

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, new_value):
        if new_value is True or new_value is False:
            self.__alive = new_value
        else:
            raise ValueError(f"Need a pure boolean only. {new_value}, on {self.name}.")

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        if value in ("town center", "ruined street", "general store"):
            self.__position = value
        else:
            raise ChangeNPCLocationError(self.name, value)

    def check_move(self):
        # 9:00 AM
        if self.clock.timer == 900:
            # move to town center
            self.position = "town center"
            return True
        # 10:00 AM
        elif self.clock.timer == 1000:
            # move to general store
            self.position = "general store"
            return True
        # 1:00 PM
        elif self.clock.timer == 1300:
            # move back to town center
            self.position = "town center"
            return True
        # 2:00 PM
        elif self.clock.timer == 1400:
            # move to ruined street again
            self.position = "ruined street"
            return True
        else:
            return False

    def use_item(self, item):
        print("It won't help.")
        return False

    def talk_to_npc(self):
        print("You should be able to talk to me. Hello!")

    def look_npc(self):
        print("It's a scavenger.")


class OrganPlayer(NPC):
    """An organ player that starts in the mansion and you can give items."""
    def __init__(self, timer, player):
        self.clock = timer
        self.player = player
        self.__position = "tower peak"
        self.__alive = True
        self.name = "organ player"
        self.inventory = []

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, new_value):
        if new_value is True or new_value is False:
            self.__alive = new_value
        else:
            raise ValueError(f"Need a pure boolean only. {new_value}, on {self.name}.")

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        if value in ("tower peak", "tower entrance"):
            self.__position = value
        else:
            raise ChangeNPCLocationError(self.name, value)

    def check_move(self):
        if "music sheet" in self.inventory and self.position == "tower peak":
            self.position = "tower entrance"
            return True
        else:
            return False

    def use_item(self, item):
        if item == "music sheet":
            print("That's what I needed! Thank you!")
            print("I must go and read it right away!")
            self.inventory.append(item)
            self.player.inventory.remove(item)
            self.player.score += 1
        else:
            print("No, no no. This won't do at all. I need music, my oddly furred man.")

    def talk_to_npc(self):
        if self.position == "tower peak":
            print("Hello I am playing music up here. Perfect for a puzzle, huh?")
            print(f"My name is {self.name}, I'm in {self.position}, and it is {self.clock.timer}, {self.clock.am_pm}")
        else:
            print("Think of them moving to this new location after I get what I want.")
            print(f"My name is {self.name}, I'm in {self.position}, and it is {self.clock.timer}, {self.clock.am_pm}")

    def look_npc(self):
        if self.position == "tower peak":
            print("It's a organ player. He is busy playing his organ.")
        else:
            print("It's a organ player. He's standing around waiting for something.")


class GeneralStoreOwner(NPC, ShopFunctions):
    """An organ player that starts in the mansion and you can give items."""
    def __init__(self, timer, player):
        self.clock = timer
        self.player = player
        self.__position = "general store"
        self.__alive = True
        self.name = "shop keeper"
        self.shop_inventory = []

    def look_npc(self):
        print("She's a friendly lioness shop keeper. Very attractive if I say so myself.", end=" ")
        if self.shop_inventory:
            print("Looks like there are thing to buy if I wanted.")
        else:
            print("She's all sold out of everything.")

    def talk_to_npc(self):

        while True:
            print("You want to 'talk' or 'shop'? (q to exit)")
            choice = input("").lower()
            clear()
            if choice == "talk":
                print("Some talking function here.")
            elif choice == "shop":
                self.shop_keeper("The lioness shows you her stock of goods.")
            elif choice == "q":
                break
            else:
                print("Do what now?")

    def use_item(self, item):
        print(f"She won't want the {item}.")

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, new_value):
        # cannot be killed or removed from game
        raise ReadOnlyError(new_value, self.name)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        raise ReadOnlyError(value, self.name)


class Johnson(NPC):
    """The NPC that gives your first mission and the one to end the game."""
    def __init__(self, timer, player):
        self.player = player
        self.clock = timer
        self.__home_room = "town center"
        self.__position = "town center"
        self.__alive = True
        self.name = "johnson"
        self.inventory = []

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, new_value):
        # cannot remove Johnson from game
        raise ReadOnlyError(new_value, self.name)

    @property
    def home_room(self):
        return self.__home_room

    @home_room.setter
    def home_room(self, new_value):
        if new_value not in ["town center", "inn room"]:
            raise ValueError(f"{new_value} not accepted as a home for Johnson.")
        else:
            self.__home_room = new_value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        if value in ["town center", "inn room"]:
            self.__position = value
        else:
            raise ChangeNPCLocationError(self.name, value)

    def check_move(self):
        if self.position != self.home_room:
            self.position = self.home_room
            return True
        else:
            return False

    def use_item(self, item):
        print("He doesn't want it.")

    def talk_to_npc(self):
        if self.home_room == "inn room":
            print("Good job on the room. Much better than a child out on the streets.")
        if self.player.player_wallet < 15000:
            print("Hello Vern. You should keep collecting money. Don't lose it this time OK?")
        else:
            # winning game condition
            print("Hey, you actually got the amount we need to get out of here, nice.")
            self.player.location = "exit"

    def look_npc(self):
        print("It's Johnson. I hope he's not too sore about the money thing...")
        if self.home_room == "town center":
            print("I need to figure out a place for us to stay.")


class Katie(NPC):
    """The main character's daughter."""
    def __init__(self, timer, player):
        self.player = player
        self.clock = timer
        self.follow = False
        self.__home_room = "town center"
        self.__position = "town center"
        self.__alive = True
        self.name = "katie"
        self.inventory = []

    @property
    def home_room(self):
        return self.__home_room

    @home_room.setter
    def home_room(self, new_value):
        if new_value not in ["town center", "inn room"]:
            raise ValueError(f"{new_value} not accepted as a home for Katie.")
        else:
            self.__home_room = new_value

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, new_value):
        # cannot remove Katie from game
        raise ReadOnlyError(new_value, self.name)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        if value in self.player.accepted_locations:
            self.__position = value
        else:
            raise ChangeNPCLocationError(self.name, value)

    def check_move(self):
        if self.follow:
            if self.player.location != self.position:
                self.position = self.player.location
                return True
            else:
                return False
        elif self.position != self.home_room:
            self.position = self.home_room
            return True
        else:
            return False

    def use_item(self, item):
        print("She won't want it.")

    def talk_to_npc(self):
        print("Hi, Dad! I love you!\nShe gives you a large hug.")
        if self.home_room == "inn room":
            print("Thank you for getting us a room to stay in dad!")
        while True:
            choice = input("follow, quit, hug.\nDid you need something? ").lower()
            clear()
            if choice == "quit" or choice == "q":
                break
            elif choice == "follow":
                self.follow = not self.follow
                if self.follow:
                    print("OK! I'm right behind you.")
                else:
                    print(f"Ok, I'll head back to the {self.home_room}!")
            elif choice == "hug":
                print("You share a large hug and feel much better.")

    def look_npc(self):
        print("It's my wonderful daughter Katie. She's wearing that lion tail I found in the mall."
              "\nI adore her in every way. I can't wait to see how she grows up.")
        if self.home_room == "town center":
            print("I need a safe place for her. I can't have her spend the night outside.")


class CollectorFelilian(NPC):
    """A collector of oddities that resides in the inn entrance."""
    def __init__(self, timer, player):
        self.player = player
        self.clock = timer
        self.quest_taken = False
        self.__position = "inn entrance"
        self.__alive = True
        self.name = "bored jaguar"
        self.inventory = []

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, new_value):
        if new_value is True or new_value is False:
            self.__alive = new_value
        else:
            raise ValueError(f"Need a pure boolean only. {new_value}, on {self.name}.")

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        raise ReadOnlyError(value, self.name)

    def use_item(self, item):
        if self.quest_taken:
            if item == "vhs tape":
                print("Whoa, a tape? This is perfect! But... how do I play it?")
                self.inventory.append(item)
                self.player.score += 1
                self.player.inventory.remove(item)
                # check if should leave game
                self.leave_game()
            elif item == "movie poster":
                print("Wow, look at that! A real Felilian, he even looks a bit like you."
                      "\nThis will shake things up a bit for sure!")
                self.inventory.append(item)
                self.player.score += 1
                self.player.inventory.remove(item)
                # check if should leave game
                self.leave_game()
            else:
                print("No that's not what I am looking for. I need things that prove we were always here."
                      "\nDisprove those lunnies that say we showed up out of nowhere.")
        else:
            print("Hey, are you a scavenger? If so let's talk.")

    def talk_to_npc(self):
        if not self.quest_taken:
            print("Hey, you. would you mind helping me with something?")
            choice = input("(y/n) ").lower()
            clear()
            if choice == "y":
                print("Oh wonderful!")
                print("I need to try and collect a few oddities from human history."
                      "\n")
                self.quest_taken = True
            else:
                print("Oh, well if you change your mind, I'll be right here.")
        elif "movie poster" in self.inventory:
            print("That movie poster is great! Can you keep an eye out for more?")
        elif "vhs tape" in self.inventory:
            print("I just need a few more things. The tape is exciting and I hope it plays still.")
        else:
            print("You still looking for those items? Try the ruins outside of town.")

    def look_npc(self):
        if not self.quest_taken:
            print("It's a young looking jaguar. Seems to be focused on reading a book.")
        else:
            print("He's that guy I'm looking for relics for.")

    def leave_game(self):
        if len(self.inventory) == 2:
            print("That's all I needed! Thanks my friendly lion.")
            print("The jaguar quickly runs off with the items you collected but not before"
                  "\npaying you handsomely for your efforts."
                  "\nI wonder if I'll ever see him again, odd fellow.")
            self.player.change_player_wallet(50)
            self.alive = False


class InnKeeper(NPC):
    """The inn keeper that rents the rooms out."""
    def __init__(self, timer, player):
        self.player = player
        self.clock = timer
        self.room_rented = False
        self.__position = "inn entrance"
        self.__alive = True
        self.name = "inn keeper"
        self.inventory = []

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, new_value):
        raise ReadOnlyError(new_value, self.name)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        raise ReadOnlyError(value, self.name)

    def use_item(self, item):
        print("He won't want it.")

    def talk_to_npc(self):
        if not self.room_rented:
            print("Would you like to rent a room? It's only 5 coins for your whole stay.")
            choice = input("y/n ").lower()
            if choice == "y":
                if self.player.player_wallet >= 5:
                    print("Ok, the room's all yours. Please don't get fur on everything?")
                    self.player.change_player_wallet(-5)
                    self.room_rented = True
                    print("Katie and Johnson move to the inn's room you rented.")
                else:
                    print(f"Sorry, you'll need more money. about {5 - self.player.player_wallet} more in fact.")
            else:
                print("Well if you change your mind, it's still open.")
        else:
            print("How's you and your group doing?")

    def look_npc(self):
        print("An older human inn keeper.", end=" ")
        if self.room_rented:
            print("He rented me a room to stay in.")
        else:
            print("I should ask about renting a room for my stay.")
