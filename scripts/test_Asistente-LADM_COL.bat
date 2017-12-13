:: Es un script en batch
ECHO OFF
ECHO Se inician pruebas
cd C:\Users\aimplementacion\Asistente-LADM_COL
git pull origin master
REM xvfb-run xbnose2-3
nose2
