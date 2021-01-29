""" A module which show some information about build and version. """


info = {
    "build_number": "UCB-29012021-00",
    "version": "0.4.3",
    "kernel": "linux 5.4.0-64-generic",
    "platform": "AMD Ryzen 3600U",
    "os": "Ubuntu-20.04"
}

def show_version_info():
    """ Show information about doondler. """
    print("Doondler | a linux system handler by doopath")
    print("Developed in 2020. Russia. Nizhniy Novgorod.")
    print(f"Current version: {info['version']} | Current build number: {info['build_number']}")
    print(f"Was built on {info['os']} & {info['kernel']} {info['platform']}.")

