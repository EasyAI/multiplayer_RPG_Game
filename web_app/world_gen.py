
image =[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 2, '#', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 2, '#', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 2, '#', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
            for pixel in row:
                ## 
                update_pixel_id     = False
                back_draw           = False
                current_Object_ID   = pixel

                ##
                x_range = x
                y_range = y
                x_size  = 1
                y_size  = 1
                ind     = 0

                check_Y_obj = False
                check_X_obj = False

                update_x_size = False

                ##
                if y > 0:
                    if image[y-1][x] == current_Object_ID:
                        check_Y_obj = True

                ##
                if y+1 < len(image):
                    if image[y+1][x] == current_Object_ID:
                        if check_Y_obj:
                            check_Y_obj = False

                if check_Y_obj:
                    while True:

                        if y-ind >= 0:
                            if image[y-ind][x] == current_Object_ID:
                                y_size += 1
                            else:
                                y_range = y-ind
                                break
                        else:
                            y_range = y-ind
                            break

                        ind += 1

                    y_size -= 1
                    y_range += 1

                else:
                    while True:
                        check_X_obj = False

                        if x+ind < len(image[y]):
                            if image[y][x+ind] == current_Object_ID:
                                check_X_obj = True

                            if y+1 < len(image):
                                if image[y+1][x+ind] == current_Object_ID:
                                    check_X_obj = False

                            if y > 0:
                                if image[y-1][x+ind] == current_Object_ID:
                                    check_X_obj = False
                        
                        if check_X_obj:
                            x_size += 1
                        else:
                            x_range = x
                            break

                        ind += 1
                    x_size -= 1

                if ind != 0:
                    if pixel == 1:
                        update_pixel_id = True
                        generated_objects.update({i:self.object_list.structure(
                            i, 
                            'wall', 
                            (x_range*Tile), 
                            (y_range*Tile), 
                            size_x=(x_size*Tile), 
                            size_y=(y_size*Tile))})

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

                        generated_objects.update({i:self.object_list.structure(
                            i, 
                            'shop', 
                            (x_range*Tile), 
                            (y_range*Tile), 
                            size_x=(x_size*Tile), 
                            size_y=(y_size*Tile), 
                            interactable=True, 
                            inter_x=(intZone[0]*Tile), 
                            inter_y=(intZone[1]*Tile))})

                    if update_pixel_id:
                        wall_ids.append(i)
                        i += 1

                x += 1
            y += 1

            x=0
        return(generated_objects, wall_ids)

