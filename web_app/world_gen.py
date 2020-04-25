
image =[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 2, '#', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 2, '#', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, '#', 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, '#', 2, '#', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, '#', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

Tile = 10
pixel_Range = [1000, 3000]

class World_Generator(object):

    def __init__(self, world_objects):
        self.object_list = world_objects


    def get_world(self):
        generated_objects = {}
        wall_ids = []
        i = 1000

        x=0
        y=0

        for row in image:
            y += 1
            for pixel in row:
                x+= 1
                update_pixel_id = False

                if pixel == 1:
                    update_pixel_id = True
                    generated_objects.update({i:self.object_list.structure(i, 'wall', x*Tile, y*Tile)})

                elif pixel == 2:
                    update_pixel_id = True

                    if image[y][(x-1)] == '#':
                        intZone = [x-1, y]
                    elif image[y][(x+1)] == '#':
                        intZone = [x+1, y]
                    elif image[(y-1)][(x)] == '#':
                        intZone = [x, y-1]
                    elif image[(y+1)][(x)] == '#':
                        intZone = [x, y+1]

                    generated_objects.update({i:self.object_list.structure(i, 'shop', x*Tile, y*Tile, interactable=True, inter_x=(intZone[0]*Tile)+Tile, inter_y=(intZone[1]*Tile)+Tile)})

                if update_pixel_id:
                    wall_ids.append(i)
                    i += 1

            x=0
        return(generated_objects, wall_ids)

