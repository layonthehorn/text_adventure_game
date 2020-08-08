#!/usr/bin/python3
from Chapter_One.chapter_one import ChapterOne
from Chapter_Two.chapter_two import ChapterTwo
import os
from os import environ
import platform
import getpass

# Temporary ascii art from https://ascii.co.uk/art/lion
ascii_image = """                 
                ,  ,, ,
           , ,; ; ;;  ; ;  ;
        , ; ';  ;  ;; .-''\\ ; ;
     , ;  ;`  ; ,; . / /7b \\ ; ;
     `; ; .;'         ;,\\7 |  ;  ;
      ` ;/   / `_      ; ;;    ;  ; ;
         |/.'  /0)    ;  ; `    ;  ; ;
        ,/'   /       ; ; ;  ;   ; ; ; ;
       /_   /         ;    ;  `    ;  ;
      `?7P"  .      ;  ; ; ; ;     ;  ;;
      | ;  .:: `     ;; ; ;   `  ;  ;
      `' `--._      ;;  ;;  ; ;   ;   ;
       `-..__..--''   ; ;    ;;   ; ;   ;
                   ;    ; ; ;   ;     ;

"""


operating = platform.system()
if (operating == 'Linux' or operating == "Darwin") and not ('ANDROID_ARGUMENT' in environ or 'ANDROID_STORAGE' in environ):
    print("Found Linux or Mac.")
    # save location and clear if on linux or mac
    save_dir = f"/home/{getpass.getuser()}/.config/vern_saves"
    def clear(): os.system("clear")

elif operating == 'Windows':
    print("Found Windows.")
    # save location and clear if on windows
    save_dir = f"C:/Users/{getpass.getuser()}/Documents/vern_saves"
    def clear(): os.system("cls")

elif 'ANDROID_ARGUMENT' in environ or 'ANDROID_STORAGE' in environ:
    print("Found Android.")
    # android system found
    save_dir = os.path.join(os.getcwd(), "vern_saves")
    def clear(): os.system("clear")

else:
    # unknown system clear screen command
    # set to print a lot of new lines
    print("Found Unknown.")
    save_dir = os.path.join(os.getcwd(), "vern_saves")
    # I can't tell what system it is so
    # I use a lot of new lines instead.
    def clear(): print("\n" * 100)

try:
    # makes sure the save directory is a thing
    if not os.path.isdir(save_dir):
        print(f"Need save directory at, {save_dir}")
        pick = input("OK, to create? (y/n) ").lower()
        if pick == "y":
            os.makedirs(save_dir)
            print("Save folder created successfully.")
            input("Press Enter...")
        else:
            print("Saving will not be possible.")
            input("Press Enter...")

except IOError:
    print("Could not create save folder. Save feature will not work.")
    input("Press Enter...")

clear()
choosing = True
while choosing:
    print(ascii_image)
    print("Welcome to my game!")
    user_input = input("Which Chapter to play? (1, 2, or q to quit) ").lower()
    if user_input == "1":
        clear()
        # add True as parameter to enable debugging commands
        ChapterOne(save_dir, clear)
        clear()
    elif user_input == "2":
        clear()
        ChapterTwo(save_dir, clear, True)
    elif user_input == "q":
        clear()
        print("Goodbye!")
        choosing = False
        input("Press Enter...")
