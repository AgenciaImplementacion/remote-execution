ECHO OFF
ECHO Se inician pruebas
cd C:\Users\aimplementacion\Asistente-LADM_COL
git pull origin master
xvfb-run nose2-3
