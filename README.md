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
# works a little bit slower than the second one
./make -pi -pyinstaller -deps -b -i

# Or this one. It's using nuitka - https://github.com/Nuitka/Nuitka.
# Compilation process is slower than first method, but it takes less
# memory and works faster.
./make -pi -nuitka -deps -b -i
```
****

**If you want to build it (in arch-linux):**
```shell
# -> Installling sources:

# Cloning the repo
git clone https://github.com/sha1om/doondler.git
cd doondler
git pull

# -> Installing dependencies:

# Install python using your package manager
sudo pacman -S python3 python2.7 pip

# Choose one of these:
python3 -m pip install pyinstaller
python3 -m pip install nuitka

python3 -m pip install -r requirements.txt

# -> Building:
mkdir build && cd build

# Choose your build tool:
python3 -m pyinstaller --onefile ../main.py -n doondler
python3 -m nuitka --follow-imports ../main.py && mkdir ../dist && mv main.bin ../dist/doondler

# Installing
sudo mv ./dist/doondler /usr/bin/
```
