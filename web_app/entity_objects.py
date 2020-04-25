'''

The class for MONSTER characeters within the game.

'''
class Monster:

    def __init__(self, entityID, x, y, size_x=10, size_y=10):
        # Base definitions
        self.entity_type        = 'monster'
        self.is_solid           = True
        self.health             = 100
        self.attack             = 20
        self.armour             = 0
        self.inventory          = []
        self.gold               = 0

        # Variable definitions
        self.entityID           = entityID
        self.position           = {'x':x, 'y':y}
        self.size               = {'x':size_x, 'y':size_y}

        self.attack_range       = 1


    def is_attacked(self, damage):
        self.health -= damage


    def get_info(self, briefData=True):

        if briefData:
            return({
                'id':       self.entityID,
                'isSolid':  self.is_solid,
                'type':     self.entity_type,
                'x':        self.position['x'],
                'y':        self.position['y'],
                'sizeX':    self.size['x'],
                'sizeY':    self.size['y']
            })

        else:
            return({
                'health':           self.health,
                'gold':             self.gold,
                'inventory':        self.inventory,
                'position':         self.position,
                'size':             self.size,
                'attackRange':      self.attack_range
            })


'''

The class for PLAYER characeters within the game.

'''
class Player:

    def __init__(self, entityID, x, y, size_x=10, size_y=10):
        # Base definitions
        self.entity_type        = 'player'
        self.is_solid           = True
        self.inMenu             = False
        self.currMenu           = None
        self.interactionZone    = None
        self.health             = 100
        self.attack             = 5
        self.gold               = 0
        self.armour             = 0
        self.inventory          = []
        self.is_solid           = True

        # Variable definitions
        self.entityID           = entityID
        self.name               = 'bob'
        self.position           = {'x':x, 'y':y}
        self.size               = {'x':size_x, 'y':size_y}

        # Attack range field:
        self.attack_range       = 2


    def is_attacked(self, damage):
        self.health -= damage


    def is_healed(self, health):

        self.health += health

        if self.health > 100:
            self.health = 100


    def upgrade_damage(self, new_damage):
        self.attack += new_damage


    def upgrade_armour(self, new_armour):
        self.armour += new_armour


    def get_info(self, briefData=True):

        if briefData:
            return({
                'id':       self.entityID,
                'isSolid':  self.is_solid,
                'type':     self.entity_type,
                'x':        self.position['x'],
                'y':        self.position['y'],
                'sizeX':    self.size['x'],
                'sizeY':    self.size['y']
            })

        else:
            return({
                'health':           self.health,
                'attack':           self.attack,
                'armour':           self.armour,
                'gold':             self.gold,
                'inventory':        self.inventory,
                'inMenu':           self.inMenu,
                'currMenu':         self.currMenu,
                'interactionZone':  self.interactionZone,
                'position':         self.position,
                'attackRange':      self.attack_range,
                'size':             self.size
            })


'''

The class for PLAYER characeters within the game.

'''
class Loot_Bag:

    def __init__(self, entityID, gold, inventory, start_x, start_y, size_x=10, size_y=10):
        # Base definitions
        self.entity_type    = 'loot_bag'
        self.is_solid       = False

        # Variable definitions
        self.entityID       = entityID
        self.gold           = gold
        self.inventory      = inventory
        self.position       = {'x':start_x, 'y':start_y}
        self.size           = {'x':size_x, 'y':size_y}


    def get_info(self):
        return({
            'id':       self.entityID,
            'isSolid':  self.is_solid,
            'type':     self.entity_type,
            'x':        self.position['x'],
            'y':        self.position['y'],
            'sizeX':    self.size['x'],
            'sizeY':    self.size['y']
        })


'''

The class for STRUCTURE characeters within the game.

'''
class structure:

    def __init__(self, entityID, ent_type, start_x, start_y, size_x=10, size_y=10, interactable=False, inter_x=0, inter_y=0, inter_size_x=10, inter_size_y=10):
        # Base definitions
        self.interactable   = interactable
        self.is_solid       = True

        # Variable definitions
        self.entityID       = entityID
        self.entity_type    = ent_type
        self.position       = {'x':start_x, 'y':start_y}
        self.size           = {'x':size_x, 'y':size_y}

        ## Interaction Zones
        self.interaction_zone_position  = {'x':inter_x, 'y':inter_y}
        self.interaction_zone_size      = {'x':inter_size_x, 'y':inter_size_y}


    def get_info(self):
        entity_info = {
            'id':       self.entityID,
            'isSolid':  self.is_solid,
            'type':     self.entity_type,
            'x':        self.position['x'],
            'y':        self.position['y'],
            'sizeX':    self.size['x'],
            'sizeY':    self.size['y']
        }

        if self.interactable:
            entity_info.update({
                'interactable': self.interactable,
                'interX':       self.interaction_zone_position['x'],
                'interY':       self.interaction_zone_position['y'],
                'interSizeX':   self.interaction_zone_size['x'],
                'interSizeY':   self.interaction_zone_size['y']
            })

        return(entity_info)


'''

The class for BOLT characeters within the game.

'''
class Bolt:

    def __init__(self, entityID, owner, direction, start_x, start_y, size_x=10, size_y=10):
        # Base definitions
        self.entity_type    = 'bolt'
        self.is_solid       = True
        self.speed          = 0
        self.hasHit         = False
        self.maxDistance    = 10

        # Variable definitions
        self.entityID       = entityID
        self.position       = {'x':start_x, 'y':start_y}
        self.size           = {'x':size_x, 'y':size_y}
        self.owner          = owner
        self.direction      = direction


    def get_info(self):
        return({
            'id':       self.entityID,
            'isSolid':  self.is_solid,
            'type':     self.entity_type,
            'x':        self.position['x'],
            'y':        self.position['y'],
            'sizeX':    self.size['x'],
            'sizeY':    self.size['y']
        })