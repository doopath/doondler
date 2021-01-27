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
./dist/install_dependencies
./make -pi -deps -b -i
```
****

**If you want to build it (in arch-linux):**
```shell
# Cloning the repo
git clone https://github.com/sha1om/doondler.git
cd doondler
git checkout to-build
git pull

# Install python using your package manager
sudo pacman -S python python2.7 pip

# Python dependencies
pip install pyinstaller
pip install -r requirements.txt

# If your pyinstaller start looks like
# "pyinstaller: command not found"
# then find the pyinstaller binary (it may be in .local/bin)
# and move to /usr/bin to start it easy

# Building
mkdir build && cd build
pyinstaller --onefile ../main.py -n doondler
sudo mv ./dist/doondler /usr/bin/
```