""" Main script handling any commands """
import sys
from modules.action_handler import ActionHandler


# If the flags weren't gotten
if len(sys.argv) < 2:
    print("Incorrect parameters set! Try to run doondler --help")
    sys.exit()


if __name__ == "__main__":
    action_handler = ActionHandler(sys.argv)
    action_handler.reduce()
