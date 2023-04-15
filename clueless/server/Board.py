from Tile import *
# from Player import *


##### TILE_NAME : TILE DICTIONARY #####
# dictionary referenced from
# https://www.pythonpool.com/adjacency-list-python/


################
################
##### MAIN #####
################
################


##### INITIALIZE TILES #####
# to initialize an object of class tile
# tile_name, tile_type, tile_num_players, is_occupied, adjacent_tiles
#
# INITIALIZE ROOM TILES
# with their str name, "ROOM", 0 players on tile, not occupied, and adj tiles
tile_study = Tile("Study", "ROOM", 0, False, ["hw_01", "hw_03", "Kitchen"])
tile_hall = Tile("Hall", "ROOM", 0, False, ["hw_01", "hw_02"])
tile_lounge = Tile("Lounge", "ROOM", 0, False, ["hw_02", "hw_05", "Conservatory"])
tile_library = Tile("Library", "ROOM", 0, False, ["hw_03", "hw_06", "hw_08"])
tile_billiard_room = Tile("Billiard Room", "ROOM", 0, False, ["hw_06", "hw_04", "hw_09", "hw_07"])
tile_dining_room = Tile("Dining Room", "ROOM", 0, False, ["hw_05", "hw_07", "hw_10"])
tile_conservatory = Tile("Conservatory", "ROOM", 0, False, ["hw_08", "hw_11", "Lounge"])
tile_ballroom = Tile("Ballroom", "ROOM", 0, False, ["hw_11", "hw_09", "hw_12"])
tile_kitchen = Tile("Kitchen", "ROOM", 0, False, ["hw_12", "hw_10", "Study"])

# INITIALIZE HALLWAY TILES
# with their str name, "HALLWAY", 0 players on tile, not occupied, and adj tiles
tile_hw_01 = Tile("hw_01", "HALLWAY", 0, False, ["Study", "Hall"])
tile_hw_02 = Tile("hw_02", "HALLWAY", 0, False, ["Hall", "Lounge"])
tile_hw_03 = Tile("hw_03", "HALLWAY", 0, False, ["Study", "Library"])
tile_hw_04 = Tile("hw_04", "HALLWAY", 0, False, ["Hall", "Billiard Room"])
tile_hw_05 = Tile("hw_05", "HALLWAY", 0, False, ["Lounge", "Dining Room"])
tile_hw_06 = Tile("hw_06", "HALLWAY", 0, False, ["Library", "Billiard Room"])
tile_hw_07 = Tile("hw_07", "HALLWAY", 0, False, ["Billiard Room", "Dining Room"])
tile_hw_08 = Tile("hw_08", "HALLWAY", 0, False, ["Library", "Conservatory"])
tile_hw_09 = Tile("hw_09", "HALLWAY", 0, False, ["Billiard Room", "Dining Room"])
tile_hw_10 = Tile("hw_10", "HALLWAY", 0, False, ["Dining Room", "Kitchen"])
tile_hw_11 = Tile("hw_11", "HALLWAY", 0, False, ["Conservatory", "Ballroom"])
tile_hw_12 = Tile("hw_12", "HALLWAY", 0, False, ["Ballroom", "Kitchen"])

# initialize dictionary of tile_name to tile object
board_tiles = {
  # ROOMS
  'Study': tile_study,
  'Hall': tile_hall,
  'Lounge': tile_lounge,
  'Library': tile_library,
  'Billiard Room': tile_billiard_room,
  'Dining Room': tile_dining_room,
  'Conservatory': tile_conservatory,
  'Ballroom': tile_ballroom,
  'Kitchen': tile_kitchen,
  # HALLWAYS
  'hw_01' : tile_hw_01,
  'hw_02' : tile_hw_02,
  'hw_03' : tile_hw_03,
  'hw_04' : tile_hw_04,
  'hw_05' : tile_hw_05,
  'hw_06' : tile_hw_06,
  'hw_07' : tile_hw_07,
  'hw_08' : tile_hw_08,
  'hw_09' : tile_hw_09,
  'hw_10' : tile_hw_10,
  'hw_11' : tile_hw_11,
  'hw_12' : tile_hw_12}


# function to check if tile player is in (moving FROM) is adjacent 
# to the tile they want to go to (moving TO)
def check_valid_adjacency(tile_from, tile_to):
  if tile_to in board_tiles.get(tile_from).adjacent_tiles:
    print (tile_to, " and ", tile_from, " are adjacent!")
  else:
    print (tile_to, " and ", tile_from, " are not adjacent!")



# print statements for testing
print("This is the room: ", board_tiles.get('Study').tile_name)
print("It's adjacent to: ", board_tiles.get('Study').adjacent_tiles)
check_valid_adjacency('Study', 'hw_01')
check_valid_adjacency('Study', 'Conservatory')
check_valid_adjacency('hw_04', 'Billiard Room')
check_valid_adjacency('hw_04', 'Hall')