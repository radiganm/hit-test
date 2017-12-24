#!/bin/bash
## plot-input.sh
## Copyright 2012 Mac Radigan
## All Rights Reserved

f=${0##*/}
d=${0%/*}

usage()
{
cat << EOF
usage: $0 [-h] [-v] -f file

Plots a shape input file.

OPTIONS:
   -f file  plot file
   -g       display results in X11 window (graphical)
   -h       show this message
   -v       verbose
EOF
}

filename=
verbose=
while getopts “f:hgv” opt
do
     case $opt in
         h)
             usage
             exit 1
             ;;
         f)
             filename=$OPTARG
             ;;
         g)
             persist=-persist
             ;;
         v)
             verbose=1
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [[ -z $filename ]]
then
     usage
     exit 1
fi

base=$(basename $filename)
title=${base%.*}

# get x/y min/max for axis
declare -a axis=($(awk '
BEGIN {
 xmin=2147483647
 ymin=2147483647
 xmax=-2147483648
 ymax=-2147483648
}
$1~/box/{
  for( i=1; i<=NF; i++)
  {
    xmin=(xmin > $2 ? $2 : xmin)
    ymin=(ymin > $3 ? $3 : ymin)
    xmax=(xmax < $4 ? $4 : xmax)
    ymax=(ymax < $5 ? $5 : ymax)
  }
}
END { print" "xmin-5" "ymin-5" "xmax+5" "ymax+5 }
' $filename))
xmin=${axis[0]}
ymin=${axis[1]}
xmax=${axis[2]}
ymax=${axis[3]}

{
  if [[ -z $persist ]]
  then
    echo "set term dumb"
  fi
  echo "set multiplot"
  echo "set title '$title'"
  echo "set datafile commentschars '#%/'"
  echo "set datafile separator ','"
  echo "set xrange [${xmin}:${xmax}]"
  echo "set yrange [${ymax}:${ymin}]"
  grep -qE "^box" $filename
  if [[ $? -eq 0 ]]; then
    awk '$1~/box/{print"set object "$NR" rect from "$2","$3" to "$4","$5" "}' $filename
    echo "plot '-' using 1:2 pt 2"
    awk '$1~/box/{print$2","$5}' $filename
    echo "e"
  fi
  grep -qE "^point" $filename
  if [[ $? -eq 0 ]]; then
    echo "plot '-' using 1:2 pt 0"
    awk '$1~/point/{print$2","$3}' $filename
    echo "e"
  fi
} | gnuplot ${persist}

## *EOF*
