""" View help list if parameters weren't given or gotten something incorrect. """

ACTIONS_LIST = """
               --init:  Initialize or reinitialize your local config
               --make-note <message> <deadline>s/m/h:  Make a notification with a deadline
               --help: Show help message
               -install <program>: Install a program using your package manager
               -i <program>: A short version of -install
               -uninstall <program>: Uninstall a program using your package manager
               --sys-update: Update system packages and repositories
               -su: A short version of --sys-update
               --gen-password <prefix> <length>: Generate unique random password
               -gp <prefix> <length>: A short version of --gen-password
               -weather: Get a current weather info: temperature, humidity, pressure etc
               --performance-boost: Set performance CPU mode
               --performance-powersave: Set powersave CPU mode
               \n
               """


def show_help_list():
    """ Print a doondler parameters to user """
    print("Doondler available parameters:")
    print(ACTIONS_LIST)
    print("Select a few of these parameters and try again!")
