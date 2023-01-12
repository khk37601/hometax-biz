#!/bin/bash

if [ $1 == "s" ] || [ $1 == "status" ]
then
   echo "start async hometax"
   python3 main.py -s
fi