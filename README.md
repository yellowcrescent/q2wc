# q2wc

**Quixel to World Creator 2**

This is a simple CLI script to batch-generate XML descriptor files for Quixel Megascans textures, so that they can be used from within World Creator 2. It uses the JSON files that are saved with each texture set, and uses them to generate an XML file for World Creator to define the Albedo (Diffuse), Normal, and Displacement textures.

## Installation

### Prerequsites
* Python 3.4+

### Install from git (Linux)

On Linux:
```
git clone https://git.ycnrg.org/scm/bpy/q2wc.git
cd q2wc
sudo ./setup.py install
```

### Use without installation (Windows)

Download the script from the link below, and save as "q2wc":
https://git.ycnrg.org/projects/BPY/repos/q2wc/raw/q2wc.py

## Usage

Usage is simple-- run the script with the path to your Quixel Library directory (same path that you would use in Quixel Bridge):

```
q2wc /path/to/Quixel/Library
```

Alternative for Windows:
```
python3 q2wc /path/to/Quixel/Library
```

Whenever you download new textures, run the script again to generate new XML files.

## Add to World Creator Global Library

You can either add individual textures to your WC Project library, or you can add your entire Quixel library to your WC global library.

To keep things neat and organized, you can maintain the Quixel and WC libraries in their own locations. To add the Quixel textures to the WC library, simply create a symlink. The paths below are only examples! Be sure to adjust as necessary.

On Linux:
```
ln -s /path/to/quixel/Downloaded/surface /path/to/worldcreator/Library/Textures/Quixel
```

On Windows:
```
mklink /D C:\Users\MyUser\Documents\Library\Textures\Quixel C:\Quixel\Downloaded\surface
```
