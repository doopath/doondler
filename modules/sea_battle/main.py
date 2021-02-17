""" A module of the SeaBattle game. """
from modules.sea_battle.ship import Ship
from modules.sea_battle.playground import Playground


#  if __name__ == "__main__":
pg = Playground()
pg.create()

fields_1 = [pg.fields_list["A"][0], pg.fields_list["A"][1], pg.fields_list["A"][2]]
fields_3 = [pg.fields_list["D"][0], pg.fields_list["D"][1], pg.fields_list["D"][2]]
fields_2 = [pg.fields_list["E"][5], pg.fields_list["F"][5], pg.fields_list["G"][5]]

ships = [Ship(fields_1), Ship(fields_2), Ship(fields_3)]

pg.fill(ships)

    #  print(pg.blow_up("A1"), "\n")
    #  print(pg.blow_up("A2"), "\n")
    #  print(pg.blow_up("A3"), "\n")
    #  print(pg.blow_up("A4"), "\n")
    #  print(pg.blow_up("A4"), "\n")
    #
    #  for letter, row in pg.fields_list.items():
    #      for field in row:
    #          if field.is_busy and field.ship is not None:
    #              print()
    #              print("Index: " + field.index)
    #              print("Is blown up: " + str(field.is_blown_up))

