#!/bin/bash
echo 'Este archivo imita al batch para probar en linux'
echo 'Se inician pruebas'
cd /home/jorge/workspace/Asistente-LADM_COL
git pull origin master
nose2-3
