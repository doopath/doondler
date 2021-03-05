# Doondler
****

## What is doondler?
**doondler is an awesome linux system handler that helps you manage your time
  install popular packages from open repositories and build it, make desktop modules
  and other stuff.**
****

## How to install doondler?
**You have a few ways to install it:**
  + **At first you can build it with a make script. It can install all dependencies and build tools.**
  + **Also, you can build it from sources, but you need to install any dependencies.**
****

**The easiest way is use the make script:**
```shell
git clone https://github.com/sha1om/doondler.git
cd doondler
chmod +x make
chmod +x install_dependencies
./install_dependencies

# The first way to compile doondler is using pyinstaller
# Compilation process pretty fast but the target binary 
# works a little bit slower than second way
./make -pi -deps -pb -i

# Or this one. It's using nuitka - https://github.com/Nuitka/Nuitka.
# Compilation process is slower than first method, but it takes less
# memory and works faster.
./make -pi -deps -nb -i
```
****

**If you want to build it (in arch-linux):**
```shell
# Cloning the repo
git clone https://github.com/sha1om/doondler.git
cd doondler
git pull

# Install python using your package manager
sudo pacman -S python3 python2.7 pip

# Python dependencies
pip3 install pyinstaller
pip3 install -r requirements.txt

# If your pyinstaller start looks like
# "pyinstaller: command not found"
# then find the pyinstaller binary (it may be in .local/bin)
# and move to /usr/bin to start it easy

# Building
mkdir build && cd build
pyinstaller --onefile ../main.py -n doondler
sudo mv ./dist/doondler /usr/bin/
```
