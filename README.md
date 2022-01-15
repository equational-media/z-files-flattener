## Z Files Flattener (ZFF)
### v0.1.1
This utility copies files of any chosen extensions from any chosen multilevel directory structure into a single, flat folder. It has been tested on Mac (Linux) and Windows. It can be run as an executable or a python script. To run the python:

```python3 zffcl.py``` or ```python zffcl.py``` 

There is also an included executable, one for each OS, compiled from that script via [pyinstaller](https://www.pyinstaller.org/). It's an executable but not a GUI. It opens up the OS command line, but is helpful because you don't need python to run it, and you can move it to and open it from any folder you choose... so you can reference relative directories without having to copy or type long paths. 

If you do run python globally on your system, you can run it via python as well, from any folder.

Here's a [video tutorial on using ZFF](https://youtu.be/BuyJt5O7QnU).

### What Happens When It Runs:
- You are prompted to give a list of extensions. One extension at a time. Ex. MP3, WAV, txt, png. It will only copy files of your given extensions. When done entering, type "x" (or "X"). The extensions are NOT case-sensitive. If you want to copy ALL the files from a directory structure, just hit "x" without entering any extensions first.
- You are prompted for the input folder. The default is the folder from where the script or executable is running. You can enter a relative directory path to this one or the full qualified path. 
- You are prompted for the output folder. This is where ZFF will copy all the files to. 
- ZFF does a deep copy from the input folder into the output folder. It doesn't overwrite, move, or rename anything. It only copies and avoids files with duplicate names. It writes results to a log file, that takes the format `ZFFreport-yyyymmdd_hhmmss.txt`. It will report the successful files copied, and any that weren't. For instance, if there are two files that share the same name but are in different directories, only the first found will be copied.

### Example.

Let's say you've entered extensions `wav` and `mp3` and specified `CARDDUMP` as the input directory and  `My-Output-Folder` as the output directory.

```
/CARDDUMP/
   /ZOOM0001/
      ZOOM0001_Tr1.WAV
      ZOOM0001_Tr2.WAV
      190403_120005.hprj
   /ZOOM0002/
      ZOOM0002_Tr1.WAV
      ZOOM0002_Tr2.WAV
      190403_120522.hprj
   /ZOOM0003/
      ZOOM0003_Tr1.MP3
      ZOOM0003_Tr2.WAV
      randomotherfilehere.txt
```
### You'll end up with:
```
/My-Output-Folder/
   ZOOM0001_Tr1.WAV
   ZOOM0001_Tr2.WAV
   ZOOM0002_Tr1.WAV
   ZOOM0002_Tr2.WAV
   ZOOM0003_Tr1.MP3
   ZOOM0003_Tr2.WAV
```
More details:
- ZFF will create the output directory if it does not exist. 
- If no output directory is specified, ZFF will create '`zff-flat`', relative to the running folder.
- If you're copying into a folder that already exists, and that already has files, ZFF will skip any that have the same name. So be careful if you don't want files from different input directories or cards mixed into the same output directory. 
- Copied files retain the metadata from the original.


### How To Run In Python:
This is tested in python3 but should work in python2. 

`python3 zffcl.py`

I ran python in my own environment:
```
python3 -m venv [your-env]
source [your-env]/bin/activate (OSX)
.\[your-env]\Scripts\activate.bat  (Windows)
```

### How To Build The Binary:
There's a number of options but [pyinstaller](https://www.pyinstaller.org) worked for me. I used:

 `pyinstaller --console --onefile --clean zffcl.py`

### Current Issues:

- When you exit the ZFF executable, the terminal/command window may not close on its own.
- The ZFF executable may not be able to write the log file if it is run from some special system folders, like the top level C:\ drive.
- If copying large files, for instance raw movies, there is no progress bar for each individual file... so it may seem that ZFF has stopped.
- If you choose to copy all files, ZFF will copy hidden files too. This isn't necessary a bug, but something to be aware of.

### Files included in this distribution:

```
zffcl.py
zffcl-osx
zffcl-win.exe
```

### Contact Info
```
hi AT gazfilm.com
Tw, IG: @gazfilm
```
