# Adventure-Game
A WIP adventure game built in python. There should be no hard or soft locks on winning. 
If you find one then it's a bug and needs to be reported to the github repo as an
issue.

This is largely inspired by the text adventures of old and wanting to make my own game
but lacking any graphical art producing skills. So I figured I'd make a 
text adventure with my own brand of humor and adventure. You can't die and 
there are no failure states so just keep trying and you'll figure it out.

## Setting Up
This game does require at least Python 3.7 for the F-strings to function. Otherwise, you will encounter hard crashes.
<br>You'll need to install _colorama_ for all systems and then _xdg_ if you are using Linux.

I have create two setup scripts, one for linux and one for windows. They are both designed to be run within their default positions.
- The ps1 script should be run in PowerShell and requires you have enabled unsigned scripts "set-executionpolicy remotesigned" Then right click and select run in PowerShell.
- The Linux script should work for most installations. 

<br>On Windows you should run this in either CMD or PowerShell for the screen clearing to work.
<br>On Linux it should work out of the box independent of what terminal emulator you're using.
<br>Mac users should run it in their terminal of choice. I don't have a Mac to test with sadly.
## How to play
Use the commands listed to go room to room and solve puzzles.

- Chapter One: You have to try and get out of a mall and join your friends outside. 
- Chapter Two: You need to collect enough money to leave town.
### Commands
- look {item}: Looks at things. room, map, objects. 
<br>**Examples**, "look room", "look map", "look robot"
- get {item}: Gets items from room.
<br>**Examples**, "get fuse", "get map", "get wrench"
- oper(ate) {object}: How you use objects: doors, computers, and talk to NPCs.
<br>**Examples**, "oper door", "oper robot", "oper shopkeeper"
- com(bine) {item} with/on {item}: allows you to combine items. Use 'self' to use an item on you.
<br>**Examples**, "com box with cat", "com gun with ammo", "com gun on self"
- drop {item}: Allows you to get rid of an item.
<br>**Examples**, "drop meat", "drop self", "drop grenade"
- use {item} With/on {object}: how you use things with other things.
<br>**Examples**, "use gun on guard", "use wrench on robot", "use self on lock"
- go {location}: How you change rooms.
<br>**Examples**, "go side room", "go bunker", "go outside"
- inv(entory): Checks your inventory and prints descriptions out.
- score: Allows player to check current progress in game.
- save: How you save your game.
- hint: Gives you a hint towards finishing the game.
- help: Prints this list of commands.
- stat: Prints stats on commands used.
- end: Exit game and will ask to save or not.

### Credits
- Thanks to my friend DisposedTalent for the room descriptions and help with ideas.
- Thanks to my parents for loving me and supporting me.
- Thanks to the user for reading this before complaining about commands in game.
