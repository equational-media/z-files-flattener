""" ZFF for the Command Line
ZFFCL 0.1.1

SYNOPSIS
'python3 zffcl.py'
default for origdir is . the current directory. 
default for flatdir is 'zff-flat' - will be created in current folder if it does not exist.

Restrictions...
Can only create a new directory local and one level deep to the current working directory.
This is for safety's sake, for now.

Future User Option...
retain or set new metadata on copy.
Currently it retains the metadata from original file. (shutil copy2 vs copyfile)
This is probably best for post audio but slower.

"""

import sys
import os
import shutil
from datetime import datetime

DIR_OUT_BASENAME_DEFAULT = "zff-flat"
INCR_SEP = "-"

#################################################################################
def confirmProceed(dirInFull, dirOutFull):
#################################################################################
   positives = ['y','yes']
   if os.path.isdir(dirOutFull):
      msgToConfirm = "\nCopy into flattened format from\n'" + dirInFull + "' " + \
                     "to\n'" + dirOutFull + "' (y/n)? "
   else:
      msgToConfirm = "\nCreate output directory\n'" + dirOutFull + "'\n" + \
                     "and copy flattened files into it from\n'" + dirInFull + "' (y/n)? "
   return input(msgToConfirm).strip().lower() in positives


#################################################################################
def flattenFiles(dirRunPath, dirInFull, dirOutFull, fnameExtensions):
#################################################################################
   # fnameExtensions should come in as all lowercase. We could check this again here if we want to be sure.
   copiedfiles = []
   dupfiles = []
   errfiles = []
   
   doAllExtensions = (len(fnameExtensions) == 0) 

   thenow = datetime.now()
   strDateTimeFilenameFormat = thenow.strftime("%Y%m%d_%H%M%S")
   strDateTimeFriendlyFormatted = thenow.strftime("%Y %b %d, %I:%M:%S%p")
   strLogFileName = "ZFFreport-" + strDateTimeFilenameFormat + ".txt"
   # strLogFileFullPath = os.path.join(os.getcwd(), strLogFileName)
   strLogFileFullPath = os.path.join(dirRunPath, strLogFileName)

   print("\n")

   for subdir, _, fnames in os.walk(dirInFull):
      if subdir == dirOutFull:
         continue
      for fname in fnames:
         if (doAllExtensions or (os.path.splitext(fname)[1].lower() in fnameExtensions)):
            sourcePath = os.path.join(subdir, fname)
            destPath = os.path.join(dirOutFull, fname)
            friendlySourcePath = os.path.join(subdir[(len(dirInFull)+1):], fname)
            
#            print(friendlySourcePath + " =>\n" + destPath)
            
            if os.path.exists(destPath):
               dupfiles.append(friendlySourcePath)
            else:
               try:
                  shutil.copy(sourcePath, destPath)
                  copiedfiles.append(friendlySourcePath)
                  isPlural = (len(copiedfiles) > 1)
                  strMsgOut = "Copying... copied " + str(len(copiedfiles)) + " file"
                  if (isPlural):
                     strMsgOut += "s"
                  sys.stdout.write("\r%s" % strMsgOut)
               except:
                  errfiles.append(friendlySourcePath)
               
   sys.stdout.flush()

   isLogFile = False
   try:
      fileLogger = open(strLogFileFullPath, 'a')
      isLogFile = True
   except:
      print("\nCould not open or create log file " + strLogFileFullPath + \
         ". Try running ZFF from a different directory with full permissions.\n")
      isLogFile = False

   if isLogFile: fileLogger.write("\nZFF Report for " + strDateTimeFriendlyFormatted + "\n")

   numUncopiedFiles = len(dupfiles) + len(errfiles) 

   if (numUncopiedFiles == 0):
      print("\nNo errors.\n")
      if isLogFile: fileLogger.write("\nNo errors.\n")
   else:
      strErrMsg = "Uncopied files: " + str(numUncopiedFiles) + ". See " + strLogFileName + " for details."
      print("\n" + strErrMsg + "\n")
      if isLogFile: 
         fileLogger.write("\nUncopied files (" + str(numUncopiedFiles) + "):\n")
         if (len(dupfiles) > 0):
            fileLogger.write(">>> Files with duplicates ("+ str(len(dupfiles)) +"):\n")
            i = 0
            for fpath in dupfiles:
               i += 1
               fileLogger.write(" " + str(i) + ") " + fpath + "\n")

         if (len(errfiles) > 0):
            fileLogger.write(">>> Files with errors (" + len(errfiles) + "):\n")
            i = 0
            for fpath in errfiles:
               i += 1
               fileLogger.write(" " + str(i) + ") " + fpath + "\n")

   if (len(copiedfiles) == 0):
      print("No files copied.\n")
      if isLogFile: fileLogger.write("\nNo files copied.\n")
   else:
      if isLogFile:
         fileLogger.write("Copied Files (" + str(len(copiedfiles)) + "):\n")
         i = 0
         for fpath in copiedfiles:
            i += 1
            fileLogger.write(" " + str(i) + ") " + fpath + "\n")

   if isLogFile:
      fileLogger.close()
      print("Wrote to logfile: " + strLogFileFullPath)

   return 0

#################################################################################
def getDirFullPath(dirGiven, currentDirRunning):
#################################################################################
   # handle special case of external volumes with a space in the name; Windows dir's shouldn't start with this, so OK.
   dirGiven = dirGiven.replace("\\ ", " ")
   while dirGiven.startswith('"') and dirGiven.endswith('"'): dirGiven = dirGiven[1:-1]
   while dirGiven.startswith("'") and dirGiven.endswith("'"): dirGiven = dirGiven[1:-1]
   if (os.path.isdir(dirGiven)):
      return dirGiven
   else:
      return os.path.join(currentDirRunning, dirGiven)

#################################################################################
def isValidFileExtension(ext):
#################################################################################
   # checks that extension is between 2 and 16 characters long and alphanumeric.
   # can also start with a dot.
   if (ext.startswith(".")):
      ext = ext[1:]
   return len(ext) >= 2 and len(ext) <= 16 and ext.isalnum()

#################################################################################
def getDesigFileExtensionsLC():
#################################################################################
   # The LC is for Lower Case.
   fExtsLC = []

   print("Enter valid file extensions (not case-sensitve). When done, type 'X'.\n" + 
         "If no valid extensions are entered, all files will be flattened.\n\n")

   newExt = input("First Extension ('X' to flatten all files): ").strip()

   while newExt not in ['x', 'X']:
      if (not newExt.startswith(".")):
         newExt = "." + newExt
      if (newExt.lower() in fExtsLC):
         print(newExt, " is already in.")
      elif (isValidFileExtension(newExt)):
         # print("appending : " + newExt)
         fExtsLC.append(newExt.lower())
      else:
         print(newExt, " is not a valid filename extension.")
      print("\nExtensions so far: " + str(fExtsLC))
      newExt = input("Next Extension ('X' to move on): ").strip()

   return fExtsLC

  
#################################################################################
def runTool():
#################################################################################
   dirOutBasename = DIR_OUT_BASENAME_DEFAULT
   dirCurrentPath = os.getcwd()
   if getattr(sys, 'frozen', False): dirCurrentPath = os.path.dirname(sys.executable)
   
   dirInFullPath = dirCurrentPath
   dirOutFullPath = getDirFullPath(dirOutBasename, dirCurrentPath)

   msgInform = "You are running relative to directory: \n" + dirCurrentPath
   print(msgInform + "\n")

   fileExtensions = getDesigFileExtensionsLC()

   msgIn = "Original directory path (skip to default to this directory, '" + \
      os.path.basename(dirInFullPath) + "'): "
   msgOut = "New flattened directory path (skip to create or use the default directory '" + \
      DIR_OUT_BASENAME_DEFAULT + "'): "

   dirGiven = input(msgIn).strip()
   dirOutGiven = input(msgOut).strip()

   if len(dirGiven) > 0: 
      dirInFullPath = getDirFullPath(dirGiven, dirCurrentPath)
      # dirInFullPath = os.path.abspath(dirGiven)
      if not os.path.isdir(dirInFullPath):
         print("Not a valid input directory: \n'"+dirInFullPath+"'")
         return -1  # means nothing yet

   # Figure out if user entered full path or relative directory basename. Or nothing at all.
   if len(dirOutGiven) > 0: 
      dirOutFullPath = getDirFullPath(dirOutGiven, dirCurrentPath)

   if len(dirOutFullPath) == 0: 
      print("Not a valid output directory: \n'"+dirOutGiven+"'")
      return -1  # means nothing yet

   if confirmProceed(dirInFullPath, dirOutFullPath):
      if not os.path.isdir(dirOutFullPath):
         try:
            os.mkdir(dirOutFullPath)
         except:
            print("\nCould not create directory '" + dirOutFullPath + "'")
            return -1   # means nothing yet

      flattenFiles(dirCurrentPath, dirInFullPath, dirOutFullPath, fileExtensions)
      print("\n")
   else:
      print("\nOperation cancelled by User.\n")
      return 0

#################################################################################
def main():
#################################################################################
   if os.name == 'nt': _= os.system("cls")
   else: _=os.system("clear")

   strIntroMsg = "\n" +\
      "**********************************************************************\n" +\
      "  ************ Welcome to the Z Files Flattener v0.1.1 *************\n" +\
      "**********************************************************************\n" +\
      "This tool copies (not moves) all files of your designated extensions\n" +\
      "from the top level directory you enter,\n" +\
      "no matter its substructure or how many levels deep, \n" +\
      "into a single directory, but in a flat, one level structure.\n" +\
      "This output directory will be created if it does not exist.\n" +\
      "Its default name is '" + DIR_OUT_BASENAME_DEFAULT + "'.\n" +\
      "If it exists already, no files already inside will be overwritten,\n"+\
      "but new files with unique names will still be copied.\n" +\
      "\nCoded and released by @gazfilm Feb 2020.\n" +\
      "**********************************************************************\n"
   print(strIntroMsg)
   ans ="y"
   while ans.lower() in ['y','yes']:
      runTool()
      ans = input('Do Another (y/n)? ').strip()

   print('\nThank you for using the Z Files Flattener. \n')

   # try:
   #    import getch
   #    if (getch.getch()): sys.exit(0)
   # except:
   #    try:
   #       import msvcrt
   #       if (msvcrt.getch()): sys.exit(0)
   #    except:
   #       exit(0)
   # finally:
   #    exit(0)
   
   sys.exit(0)

#################################################################################
main()
#################################################################################
