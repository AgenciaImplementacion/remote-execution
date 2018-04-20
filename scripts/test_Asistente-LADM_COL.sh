#!/bin/bash
echo 'Este archivo imita al batch para probar en linux'
echo 'Se inician pruebas'
cd /home/jorge/workspace/Asistente-LADM_COL
git fetch --all
git reset --hard origin/master
git pull origin master
cd asistente_ladm_col
make
cd ..
nose2-3
