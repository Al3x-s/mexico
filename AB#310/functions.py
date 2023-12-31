import time
import random
import json
import sys
import threading
import os

move = ["move", "go", "travel", "run", "m"]
talk = ["talk", "speak", "chat", "ta", "ask"]
look = ["examine", "look", "focus", "observe", "inspect", "l"]
take = ["grab", "take", "t", "pickup"]
use = ["use", "interact"]

allpossible = ["move", "go", "travel", "run", "m", "talk", "speak", "chat", "ta", "ask", "examine", "look", "focus", "observe", "inspect", "l", "grab", "take", "t", "pickup", "use", "interact"]

f = open(os.path.abspath('gamedata.json'))
gamedata = json.load(f)

def check_action(given_action):
    if given_action in allpossible:
        if given_action in move:
            return 'm'
        elif given_action in talk:
            return 'ta'
        elif given_action in look:
            return 'l'
        elif given_action in take:
            return 't'
        else:
            return 'u'
    else:
        return 'invalid'

def check_location(wanted_room, adjacent_rooms):
    if wanted_room.isnumeric():
        if int(wanted_room) in range(1,7) and int(wanted_room) in adjacent_rooms:
            return True
    else:
        return False
        
def help_message():
    return "this print help screen"


def ps(description, delay=0.02):     
    def input_listener():
        nonlocal skip_print
        while True:
            key = sys.stdin.read(1)
            if key == 's':
                skip_print.set()
                break

    skip_print = threading.Event()

    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()


    for char in description:         
        if skip_print:
            break
        print(char, end='', flush=True)         
        time.sleep(delay)
    print()

def start_menu():
    print("1.New Game")
    print("2.Quit")
    player_choice = input("Enter your choice '1 or 2'> ")
    if player_choice == "1":
        start_game()
    elif player_choice == "2":
        print("Goodbye!")
        sys.exit()
    else:
        print("invalid answer, try again")
        start_menu()
def start_game():
    main()


def display_look(oobject):
    npc = oobject[0]['nameOfNpc']
    items = ' and '.join(oobject[1].keys())

    print(f"you look around and see {npc} and {items}")
    #this code may break when we alter the format the gamedata.json file
    #return to this to validate the length of the item lists and npcs lists
    #if there isnt anything say that instead of presenting nothing the .join
    #word

class Submarine:
    def __init__(self):
        self.rooms = {}
        for i in range(1, 7):
            self.rooms[i] = {'adjacent': [], 'content': []}
            connections = [(1,3),(2,4),(3,5,4,1),(4,2,3,6),(5,6,3),(6,5,4)]
        for room, *adjacent in connections:
            self.rooms[room]['adjacent'] = adjacent

    def place_content(self, content, chosen_room):
        self.rooms[chosen_room]['content'].append(content)

    def get_adjacent_rooms(self, room):
        return self.rooms[room]['adjacent']

    def get_room_content(self, room):
        return self.rooms[room]['content']

class Player:
    def __init__(self):
        self.current_room = 1
        self.sanity = 30 # everymove subtracts 1
        self.has_advil = False
        self.has_key = False
        self.has_bathroom_access = False
        self.inventory = []
    def found_key(self):
        self.has_key = True
    def found_advil(self):
        self.has_advil = True
    def has_bathroom_access(self):
        self.has_bathroom_access = True
    def add_to_inventory(self, item):
        self.inventory.append(item)
    def move(self, room):
        self.current_room = room
        self.sanity = self.sanity - 1

def main():
    submarine = Submarine()
    player = Player()
    for i in range(len(gamedata['rooms'])):
        stuffinroom = gamedata['rooms'][i]['content'].keys()
        npc_data = gamedata['rooms'][i]['content']['npc']
        item_data = gamedata['rooms'][i]['content']['items']
        submarine.place_content(npc_data, i+1)
        submarine.place_content(item_data, i+1)

    while True:
        adjacent_rooms = submarine.get_adjacent_rooms(player.current_room)       
        room_content = submarine.get_room_content(player.current_room)
        print("=-=-=-=-=-=-=-=-=Location Data=-=-=-=-=-=-=-=-=")
        print(f"you are in room {player.current_room}")
        print(f"Adjacent rooms {adjacent_rooms}\n")
        print("=-=-=-=-=-=-=-=-=Player Data=-=-=-=-=-=-=-=-=") 
        print(f"Your sanity is at {player.sanity}")
        print("=-=-=-=-=-=-=-=-=Inventory Data=-=-=-=-=-=-=-=-=")
        print(f"Things in your inventory {player.inventory}")

        pair = input("What do you want to do\n>")
        if pair.lower() == 'help':
            print("you can do the following actions Move (M) Take (T) Look (L) Talk (TA)\nAt any point, you can type in 'quit' to exit the game.")
            continue
        if pair.lower() == 'quit':
            ps("Goodbye...")
            sys.exit()
        pair = pair.split()
        action = pair[0] 
        action = check_action(action)
        if action == 'invalid':
            print("That is not a valid action")
            print("Valid options are 'move' 'talk' 'take' 'use' and 'look'")
            continue
        #action = input("\n> ").lower()
        if action == "m":
            room_choice = check_location(pair[1], adjacent_rooms) 
            if room_choice:
                player.move(int(pair[1]))
            else:
                print("you cannot move there\n")
                continue
        elif action == 'l':
            display_look(room_content)
        else:
            print(submarine)
            break
