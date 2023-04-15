# custom tile class for Clue-less
# import enum

# custom class creation reference
# https://learnpython.com/blog/custom-class-python/

class Tile:

    # initialize an object of class tile
    def __init__(self, tile_name, tile_type, tile_num_players, is_occupied, adjacent_tiles):
        self.tile_name = tile_name
        # room, corner_room, hallway
        self.tile_type = tile_type
        self.tile_num_players = tile_num_players
        self.is_occupied = is_occupied
        self.adjacent_tiles = adjacent_tiles
        # need to define this attribute separately

    def set_occupied(self):
        # set the Tile's is_occupied to TRUE *if it is not already occupied*
        #
        # KT note, might need to change to accommodate changing an old location?
        # or a more robust check of whether or not there is at least one character
        if self.is_occupied == True:
            return  # is this pass or return?
        else:
            self.is_occupied = True
    
    def set_unoccupied(self):
        # set the Tile's is_occupied to FALSE *if it is not already unoccupied*
        #
        # KT note, might need to change to accommodate changing an old location?
        # or a more robust check of whether or not there is at least one character
        if self.is_occupied == False:
            return  # is this pass or return?
        else:
            self.is_occupied = False

    def get_tile_name(self):
        print(self.tile_name)


    def check_occupancy(self):
        pass
    # def check_occupancy
    # check all player current locations
    # if location matches tile name
    # increment tile counter
    # else if no match found
    # set number of occupying players to zero

    def set_occupancy(self):
        if self.tile_num_players == 0:
            self.set_unoccupied
            print(self.set_unoccupied)
        else:
        # this is incomplete, need to check for room type and also update
        # player location
            self.set_occupied
            print(self.set_occupied)




# "main"
# instantiate tiles in Board class, import into Board