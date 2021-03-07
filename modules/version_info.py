""" A module which show some information about build and version. """

# build_number: TYPE-DATE-DAILY_UPDATE

# Build types:
#   UCB - Unstable Changes Build
#   UFB - Unstable Full Build
#   SCB - Stable Changes Build
#   SFB - Stable Full Build

# Dates example: DAY-MONTH-YEAR:
#   31st of January 2021 - 31012021

# Daily update example: NUMBER of updates count
#   Sometimes you can make a few updates per one day so it shows how many updates you've made.
#   First - 00; Second - 01; etc.


info = {
    "build_number": "UCB-06032021-02",
    "version": "0.5.11",
    "kernel": "linux 5.11.2",
    "platform": "AMD Ryzen 3600U",
    "os": "Ubuntu-20.04"
}


def show_version_info():
    """ Show information about doondler. """
    print("Doondler is a linux system handler by doopath.")
    print("Developed in 2020. Russia. Nizhny Novgorod.")
    print(f"Current version: {info['version']} | Current build number: {info['build_number']}.")
    print(f"Was built on {info['os']} & {info['kernel']} {info['platform']}.\n")
