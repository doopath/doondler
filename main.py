""" Main script handling any commands """
import sys
from modules.config import Config


# If the init flag was gotten then make configuration file and exit.
if "--init" in sys.argv:
    Config().make()


def nothing():
    pass


# If the flags weren't gotten
if len(sys.argv) < 2:
    print("Incorrect parameters set! Try to run doondler --help")
    sys.exit()


from modules.action_handler import ActionHandler

action_handler = ActionHandler(sys.argv)

if __name__ == "__main__":
    action_handler.reduce()

