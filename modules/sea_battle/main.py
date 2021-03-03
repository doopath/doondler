""" A module of the SeaBattle game. """
from modules.sea_battle.ship import Ship
from modules.sea_battle.playground import Playground

#  if __name__ == "__main__":
pg = Playground(is_hidden=True)
pg.create()

fields_list = [
    [pg.fields_list["A"][0], pg.fields_list["B"][0], pg.fields_list["C"][0]],
    [pg.fields_list["A"][1], pg.fields_list["B"][1], pg.fields_list["C"][1]],   # Incorrect
    [pg.fields_list["E"][0], pg.fields_list["F"][0], pg.fields_list["G"][0]],
    [pg.fields_list["C"][4], pg.fields_list["D"][4], pg.fields_list["E"][4]],
    [pg.fields_list["C"][7], pg.fields_list["D"][7], pg.fields_list["E"][7]],
    [pg.fields_list["I"][6], pg.fields_list["I"][7]],
    [pg.fields_list["B"][5], pg.fields_list["B"][6]],  # Incorrect
    [pg.fields_list["G"][4], pg.fields_list["H"][4]]
]

ships = [Ship(fields) for fields in fields_list]

pg.fill(ships)
pg.validate()

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
