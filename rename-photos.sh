#!/bin/bash
#
# rename-photos.sh
#
# PhotosPath="/media/4GBSD/DCIM/101CANON"
# SortPath="/home/angus/.imagesort"
# LibraryPath="/home/angus/Photos"
# CameraPath="/media/4GBSD"

echo "Usage: rename-photos source-dir dest-dir <prefix> <suffix>"
echo "       prefix and suffix are filenaming options."
echo "If you did not enter source and destination directories,"
echo "type 'control-c' now and try again."

[ $# -ge 2 ] || return $FAILURE

PhotosPath="$1"				# Source path of new photos
SortPath="./.imagesort"			# Default sort path
LibraryPath="$2"			# Destination path of renamed photos
CharFromName=4

if [ $# -ge 3 ]; then
	prefix="$3"
else
	prefix=""
fi

if [ $# -ge 4 ]; then
	suffix="$4"
else
	suffix=""
fi

echo
echo
############
# Test to see if $PhotosPath exists, if not promp for new path / exit.
test -d $PhotosPath || read -p "$PhotosPath does not exist, close to exit or type new path:" PhotosPath
test -d $PhotosPath || "read -p '$PhotosPath is invalid. Press enter to close' && exit"

test -d $SortPath || mkdir $SortPath

############
# Copy files from $PhotosPath to $SortPath
rsync -va $PhotosPath/* $SortPath/

############
# rename all image files in $SortPath
# FolderDateDD-HHMMSS.ext
# jhead  -autorot -ft -nf%y%m%d-%H%M%S $SortPath/*
jhead -ft -n%Y/%m/%d/$prefix%Y-%m-%d-%H:%M:%S%f$suffix *.jpg


###########
# Sort files into folders using $CharFromName letters of the file name
#
#ls $SortPath | while read file; do
 # extract first $CharFromName characters from filename
# FolderDate=${file:0:$CharFromName}
 # create directory if it does not exist
# test -d $LibraryPath/$FolderDate || mkdir $LibraryPath/$FolderDate
 # move the current file to the destination dir
# mv -v $SortPath/$file $LibraryPath/$FolderDate/$file
#done

##########
# move sorted files into photo library
# mv -v $SortPath/* $LibraryPath/

##########
# Umount the card
# umount $CameraPath

##########
# End notification
echo 
echo "Photos  from: $PhotosPath"
echo "End location: $LibraryPath"
echo 
echo "The card has been ejected."
echo 
read -p "Press enter to close this window…"
