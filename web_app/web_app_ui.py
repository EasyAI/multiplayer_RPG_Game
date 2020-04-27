#! /usr/bin/env python3

import random
import os
import time
import json
import copy
from . import engine
from . import entity_objects
from . import world_gen
import logging
import threading
from flask_socketio import SocketIO
from flask import Flask, render_template, url_for, request


MONSTER_AREA_ZONES = [[20, 10, 15, 15], [40, 20, 15, 15]]

BOLT_RANGE      = [0, 500] 
MONSTER_RANGE   = [500, 750]
LOOT_BAG_RANGE  = [750, 1000]
PLAYER_RANGE    = [1000]
TILE_SIZE       = 10


app = Flask(__name__)
socketio = SocketIO(app)
running = True

screen_dimentions = {'x':900, 'y':700}

game_engine = engine.Game_Engine_2D(screen_dimentions, TILE_SIZE)
mainLoop = None
game_engine.monster_zones = MONSTER_AREA_ZONES


@app.context_processor
def override_url_for():
    return(dict(url_for=dated_url_for))


def dated_url_for(endpoint, **values):
    '''
    This is uses to overide the normal cache for loading static resources.
    '''
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                    endpoint,
                                    filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/', methods=['GET', 'POST'])
def searchApp_page():
    global mainLoop
    
    if mainLoop == None:
        mainLoop = main_loop()
        mainLoop.start_loop()

    return(render_template('main_page.html'))


@app.route('/rest-api/v1/player_logon', methods=['GET'])
def player_logon():
    return()


@app.route('/rest-api/v1/get_shop_stock', methods=['GET'])
def get_shop_stock():
    return({'data':[[1,1],[7,1],[2,1],[4,1]]})


@socketio.on('socket/v1/get_player_data')
def s_player_data(data):

    playerID = data

    if playerID > PLAYER_RANGE[0]:
        if not(playerID in mainLoop.exist_player_IDs):
            start_x = 50
            start_y = 50

            mainLoop.player_objects.update({playerID:entity_objects.Player(
                playerID, 
                start_x, 
                start_y)})
            mainLoop.exist_player_IDs.append(playerID)

        give_player_data(playerID, mainLoop.player_objects[playerID].get_info(False))


@socketio.on('socket/v1/update_player_data')
def a_player_data(data):

    playerID = data['player_id']
    action = data['action']

    if action == 'attack':
        collision_IDs = game_engine.check_damage_area(
            mainLoop.player_objects[playerID].get_info(False),
            playerID, 
            data['direction'])

        if collision_IDs != []:
            for collision_ID in collision_IDs:
                if collision_ID in mainLoop.exist_monster_IDs:
                    mainLoop.monster_objects[collision_ID].is_attacked(100)

    elif action == 'shoot':
        ## For the bolt shooting.
        start_x = mainLoop.player_objects[playerID].position['x']
        start_y = mainLoop.player_objects[playerID].position['y']

        boltId = random.randint(BOLT_RANGE[0], BOLT_RANGE[1])
        mainLoop.bolt_objects.update({boltId:entity_objects.Bolt(
            boltId, 
            playerID, 
            data['direction'], 
            start_x, 
            start_y)})
        mainLoop.exist_bolt_IDs.append(boltId)


    elif (action == 'interact' or action == 'inventory' or action == 'esc'):
        ## User interaction with objects.
        can_update = True

        if action == 'interact' and not(mainLoop.player_objects[playerID].interactionZone == 'shop'):
           can_update = False

        if can_update:
            mainLoop.player_objects[playerID].inMenu = data['inMenu']
            mainLoop.player_objects[playerID].currMenu = data['currMenu']


@socketio.on('socket/v1/get_player_action')
def get_player_action(data):

    playerID = data['player_id']
    action = data['action']

    if action == 'move':
        newPos = game_engine.move(
            playerID,
            data['direction'],
            TILE_SIZE*1)
        
        collision_entity_id = newPos[3]
        if newPos[0]:
            update_position = False
            collision_entity_id = newPos[3]

            if type(collision_entity_id) != str:
                if collision_entity_id >= LOOT_BAG_RANGE[0] and collision_entity_id <= LOOT_BAG_RANGE[1]:
                    loot_bag_items = mainLoop.loot_bag_objects[collision_entity_id].inventory

                    ##
                    for item in loot_bag_items:
                        if item in mainLoop.player_objects[playerID].inventory:
                            mainLoop.player_objects[playerID].inventory[item]+=loot_bag_items[item]
                        else:
                            mainLoop.player_objects[playerID].inventory.update({item:loot_bag_items[item]})

                    ##
                    mainLoop.player_objects[playerID].gold += mainLoop.loot_bag_objects[collision_entity_id].gold
                    mainLoop.exist_loot_bag_IDs.remove(collision_entity_id)
                    update_position = True

            elif type(collision_entity_id) == str:
                mainLoop.player_objects[playerID].interactionZone = collision_entity_id
                update_position = True

        else:
            if newPos[3] != -1:
                update_position = True

        if update_position:
            mainLoop.player_objects[playerID].interactionZone = collision_entity_id

            mainLoop.player_objects[playerID].position['x'] = newPos[1]
            mainLoop.player_objects[playerID].position['y'] = newPos[2]
            give_player_data(playerID, mainLoop.player_objects[playerID].get_info(False))

    elif action == 'use':
        item_to_use = data['item']

        if item_to_use in mainLoop.player_objects[playerID].inventory:
            current_item = mainLoop.ITEMS_LIST[item_to_use]

            mainLoop.player_objects[playerID].inventory[item_to_use] -= 1

            if mainLoop.player_objects[playerID].inventory[item_to_use] <= 0:
                del mainLoop.player_objects[playerID].inventory[item_to_use]

            if current_item[0] == 'damage':
                mainLoop.player_objects[playerID].upgrade_damage(current_item[1])
            elif current_item[0] == 'armour':
                mainLoop.player_objects[playerID].upgrade_armour(current_item[1])
            elif current_item[0] == 'heal':
                mainLoop.player_objects[playerID].is_healed(current_item[1])


def give_env_data(entity_list):
    print(entity_list)
    socketio.emit('env_entities', entity_list)


def give_player_data(playerID, players_data):
    new_list = []

    print(players_data)
    for key in players_data['inventory']:
        new_list.append([key, players_data['inventory'][key]])

    players_data['inventory'] = new_list

    socketio.emit('player_data', {'id':playerID, 'data':players_data})


class main_loop(object):

    def __init__(self):
        self.ITEMS_LIST = (
            ## category     stat    value   drop%
            ['damage',      10,     10,     50],    # BRONZE_SWORD
            ['armour',      10,     10,     50],    # BRONZE_ARMOUR
            ['heal',        15,     10,     50],    # MINOR_HP_POTION
            ['damage',      25,     10,     50],    # IRON_SWORD
            ['armour',      25,     10,     50],    # IRON_ARMOUR
            ['heal',        50,     10,     50],    # NORMAL_HP_POTION
            ['damage',      40,     10,     50],    # STEEL_SWORD
            ['armour',      40,     10,     50],    # STEEL_ARMOUR
            ['heal',        75,     10,     50],    # GREAT_HP_POTION
            )

        ## Loot bag related
        self.loot_bag_objects   = {}
        self.exist_loot_bag_IDs = []

        ## Player Related
        self.player_objects     = {}
        self.exist_player_IDs   = []

        ##  Monster Related.
        self.monster_objects    = {}
        self.exist_monster_IDs  = []
        self.maxMonsters        = 10
        
        ## Bolt related
        self.bolt_objects       = {}
        self.exist_bolt_IDs     = []
        self.maxBoltsPerPlayer  = 5

        ## World generation.
        worldGen = world_gen.World_Generator(entity_objects)
        genEls = worldGen.get_world()
        self.world_objects      = genEls[0]
        self.exist_world_IDs    = genEls[1]


    def start_loop(self):
        loop_thread = threading.Thread(target=self._start)
        loop_thread.start()
        

    def _start(self):
        current_tick = 0
        initial_setup = True

        while running:
            current_tick += 1
            entity_list = []

            ## Udater for bolts.
            self.bolt_updater(current_tick, initial_setup)

            ## updater for monsters.
            self.monster_updater(current_tick, initial_setup)

            ## Update the players with the data
            for playerID in self.exist_player_IDs:
                give_player_data(playerID, self.player_objects[playerID].get_info(False))

            ## update engine entity list.
            for playerID in self.exist_player_IDs:
                entity_list.append(self.player_objects[playerID].get_info())

            for monsterID in self.exist_monster_IDs:
                entity_list.append(self.monster_objects[monsterID].get_info())

            for loot_bagID in self.exist_loot_bag_IDs:
                entity_list.append(self.loot_bag_objects[loot_bagID].get_info())

            for boltID in self.exist_bolt_IDs:
                entity_list.append(self.bolt_objects[boltID].get_info())

            for worldID in self.exist_world_IDs:
                entity_list.append(self.world_objects[worldID].get_info())

            game_engine.update_entity_list(entity_list)

            give_env_data(entity_list)
            time.sleep(0.1)
            initial_setup = False


    def monster_updater(self, current_tick, initial_setup):
        monsterSleep = 10

        ## Maintain the monster count to the set value in maxMonsters.
        while len(self.exist_monster_IDs) != self.maxMonsters:
            monster_spawn_area = random.randint(0, len(MONSTER_AREA_ZONES)-1)

            x = (random.randint(MONSTER_AREA_ZONES[monster_spawn_area][0], (MONSTER_AREA_ZONES[monster_spawn_area][0]+MONSTER_AREA_ZONES[monster_spawn_area][2]))*TILE_SIZE)
            y = (random.randint(MONSTER_AREA_ZONES[monster_spawn_area][1], (MONSTER_AREA_ZONES[monster_spawn_area][1]+MONSTER_AREA_ZONES[monster_spawn_area][3]))*TILE_SIZE)

            monsterID = random.randint(MONSTER_RANGE[0], MONSTER_RANGE[1]) # Generate a new ID for the monster that does not already exist.

            if not(monsterID in self.exist_monster_IDs):
                ## Create the new monster object.
                self.monster_objects.update({monsterID:entity_objects.Monster(
                    monsterID, 
                    monster_spawn_area,
                    x, 
                    y)})
                self.exist_monster_IDs.append(monsterID)

                ## Setup the monster to start with a inventory that can be picked up.
                numItems = random.randint(0, 3) # Random to decied the amount of items in the monsters inventory.

                for i in range(numItems): # Loop for each item to again randomly pick the item the monster will recive
                    self.monster_objects[monsterID].inventory.update({random.randint(0, len(self.ITEMS_LIST)-1):1})

                self.monster_objects[monsterID].gold = random.randint(1, 100) # GIve the monster base gold to also be picked up.

        if initial_setup:
            return

        ## Movement for monsters.
        monsters_to_remove = []
        for monsterID in self.exist_monster_IDs:

            ## If the monster still has health then it can move.
            if self.monster_objects[monsterID].health >= 1:
                if not(current_tick % monsterSleep == 0):
                    continue

                i = random.randint(1, 4)

                if i == 1:
                    direction='up'
                elif i == 2:
                    direction='down'
                elif i == 3:
                    direction='left'
                elif i == 4:
                    direction='right'

                newPos = game_engine.move(
                    monsterID,
                    direction,
                    TILE_SIZE*1)

                update_position = False
                if newPos[0]:
                    collision_entity_id = newPos[3]

                    if collision_entity_id in self.exist_loot_bag_IDs:
                        update_position = True
                    else:
                        update_position = False

                else:
                    if newPos[3] != -1:
                        update_position = True

                if update_position:
                    self.monster_objects[monsterID].position['x'] = newPos[1]
                    self.monster_objects[monsterID].position['y'] = newPos[2]
            else:
                ## If monster has 0 HP its dead.
                pos_x       = self.monster_objects[monsterID].position['x']
                pos_y       = self.monster_objects[monsterID].position['y']
                gold        = self.monster_objects[monsterID].gold
                inventory   = self.monster_objects[monsterID].inventory

                self.spawn_loot_bag(gold, inventory, pos_x, pos_y)
                monsters_to_remove.append(monsterID)

        self.remove_monsters(monsters_to_remove)


    def bolt_updater(self, current_tick, initial_setup):
        boltSleep = 1

        if initial_setup:
            return

        if current_tick % boltSleep == 0:
            bolts_to_remove = []
            for boltID in self.exist_bolt_IDs:
                if self.bolt_objects[boltID].traveled >= self.bolt_objects[boltID].maxDistance:
                    bolts_to_remove.append(boltID)
                    continue

                newPos = game_engine.move(
                    boltID,
                    self.bolt_objects[boltID].direction,
                    TILE_SIZE*1)

                update_position = False
                if newPos[0]:
                    collision_entity_id = newPos[3]

                    ## Bolt dosent exist or has collied with its owner. (JUST PASS)
                    if (collision_entity_id == self.bolt_objects[boltID].owner):
                        update_position = True

                    if collision_entity_id in self.exist_loot_bag_IDs:
                        update_position = True

                    if not update_position:
                        ## Check for bolt collisions on PLAYERS.
                        if collision_entity_id in self.exist_player_IDs:
                            pass

                        ## Check for bolt collisions on MONSTERS.
                        if collision_entity_id in self.exist_monster_IDs:
                            self.monster_objects[collision_entity_id].is_attacked(100)
                            bolts_to_remove.append(boltID)

                else:
                    if newPos[3] != -1:
                        update_position = True

                if update_position:
                    self.bolt_objects[boltID].traveled += 1
                    self.bolt_objects[boltID].position['x'] = newPos[1]
                    self.bolt_objects[boltID].position['y'] = newPos[2]

            self.remove_bolt(bolts_to_remove)


    def spawn_loot_bag(self, gold, inventory, pos_x, pos_y):

        while True:
            loot_bagID = random.randint(LOOT_BAG_RANGE[0], LOOT_BAG_RANGE[1])

            if not(loot_bagID in self.exist_loot_bag_IDs):
                self.loot_bag_objects.update({loot_bagID:entity_objects.Loot_Bag(
                    loot_bagID,
                    gold,
                    inventory,
                    pos_x, 
                    pos_y)})
                self.exist_loot_bag_IDs.append(loot_bagID)
                break


    def remove_bolt(self, remove_boltID):

        if type(remove_boltID) == int:
            remove_boltID = [remove_boltID]

        for boltID in remove_boltID:
            self.exist_bolt_IDs.remove(boltID)


    def remove_monsters(self, remove_monsterID):

        if type(remove_monsterID) == int:
            remove_monsterID = [remove_monsterID]

        for monsterID in remove_monsterID:
            self.exist_monster_IDs.remove(monsterID)


def start(ip="127.0.0.1", port=5000):
    socketio.run(app, host=ip, port=port, debug=True)


