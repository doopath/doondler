""" Main script handling any commands """
import sys

from modules.config import Config



if __name__ == "__main__":
    # If the flags weren't gotten
    if len(sys.argv) < 2:
        print("Incorrect parameters set! Try to run doondler --help")
        sys.exit()

    if "--init" in sys.argv:
        Config().make()

    from modules.action_handler import ActionHandler
    action_handler = ActionHandler(sys.argv)
    action_handler.reduce()
