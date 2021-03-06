

class Game_Engine_2D(object):

    def __init__(self, screen_size, tile_size):
        self.screen_size = screen_size
        self.tile = tile_size

        self.monster_zones = []


    def update_entity_list(self, entity_list, entityID=None):
        if entityID != None:
            self.entity_list.update({entityID:entity_list})
        else:
            self.entity_list = entity_list


    def check_damage_area(self, entity_full_data, entityID, direction):

        ## get the attacker details
        pos_x           = entity_full_data['position']['x']
        pos_y           = entity_full_data['position']['y']
        size_x          = entity_full_data['size']['x']
        size_y          = entity_full_data['size']['y']
        attack_range    = (entity_full_data['attackRange']*self.tile)

        ## attack distance
        if direction == 'up':
            attack_section = [
                pos_x, 
                pos_y-attack_range, 
                pos_x+size_x, 
                pos_y]

        elif direction == 'down':
            attack_section = [
                pos_x, 
                pos_y+size_y, 
                pos_x+size_x, 
                ((pos_y+size_y)+attack_range)]

        elif direction == 'left':
            attack_section = [
                pos_x-attack_range, 
                pos_y, 
                pos_x, 
                (pos_y+size_y)]

        elif direction == 'right':
            attack_section = [
                ((pos_x+size_x)), 
                pos_y, 
                ((pos_x+size_x)+attack_range), 
                (pos_y+size_y)]

        hitEntities = []
        for entity in self.entity_list:
            if entityID != entity['id'] and entity['type'] == 'monster':
                entitySizeX = entity['x']+entity['sizeX']
                entitySizeY = entity['y']+entity['sizeY']

                if (entity['x'] >= attack_section[0]) and (entitySizeX <= attack_section[2]):
                    if (entity['y'] >= attack_section[1]) and (entitySizeY <= attack_section[3]):
                        hitEntities.append(entity['id'])

        return(hitEntities)


    def move(self, entityID, direction, speed):
        foundEntity = False

        for entity in self.entity_list:
            if entityID == entity['id']:
                foundEntity = True
                pos_x   = entity['x']
                pos_y   = entity['y']
                size_x  = entity['sizeX']
                size_y  = entity['sizeY']
                break

        if not foundEntity:
            return(False, None, None, -1)

        if direction == 'up':
            pos_y -= speed
        elif direction == 'down':
            pos_y += speed
        elif direction == 'left':
            pos_x -= speed
        elif direction == 'right':
            pos_x += speed
        else:
            return(-1)

        collisionID = self._check_collisions(entityID, pos_x, pos_y, size_x, size_y)

        if collisionID or (type(collisionID) == int and collisionID == 0):
            if type(collisionID) == int:
                return(True, pos_x, pos_y, collisionID)
            if type(collisionID) == str:
                return(True, pos_x, pos_y, collisionID)

        return(False, pos_x, pos_y, None)


    def _check_collisions(self, entityID, pos_x, pos_y, size_x, size_y):

        for entity in self.entity_list:

            if entityID != entity['id']:

                ## 
                if 'interactable' in entity:
                    if (pos_x >= entity['interX']) and ((pos_x+size_x) <= (entity['interX']+entity['interSizeX'])):
                        if (pos_y >= entity['interY']) and ((pos_y+size_y) <= (entity['interY']+entity['interSizeY'])):
                            return(entity['type'])
                            break

                ## 
                if (pos_x >= entity['x']) and ((pos_x+size_x) <= (entity['x']+entity['sizeX'])):
                    if (pos_y >= entity['y']) and ((pos_y+size_y) <= (entity['y']+entity['sizeY'])):
                        return(entity['id'])
                        break
            else:
                if entity['type'] == 'monster':
                    zoneID = entity['zone']
                else:
                    zoneID = None
        
        if self._check_boundry_collision(pos_x, pos_y, size_x, size_y, zoneID):
            return(0)

        return(False)


    def _check_boundry_collision(self, pos_x, pos_y, size_x, size_y, mZone=None):

        if mZone != None:
            ## Check for monster zone boundery collision
            if (self.monster_zones[mZone][0]*self.tile > pos_x) or (pos_x+size_x > (self.monster_zones[mZone][0]+self.monster_zones[mZone][2])*self.tile): 
                return(True)

            if (self.monster_zones[mZone][1]*self.tile > pos_y) or (pos_y+size_y > (self.monster_zones[mZone][1]+self.monster_zones[mZone][3])*self.tile):
                return(True)

        ## Check forscreen edge collision
        if (0 > pos_x) or (pos_x+size_x > self.screen_size['x']): 
            return(True)

        if (0 > pos_y) or (pos_y+size_y > self.screen_size['y']):
            return(True)

        return(False)