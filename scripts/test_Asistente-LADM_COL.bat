:: Es un script en batch
ECHO OFF
ECHO Configurando entorno
rem https://qgis.org/downloads/weekly/QGIS-OSGeo4W-2.99.0-51-Setup-x86_64.exe
rem C:\Users\aimplementacion\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
rem https://answers.microsoft.com/es-es/windows/forum/windows_10-other_settings-winpc/windows-10-programar-una-tarea-cómo-programar/dd0be19b-0365-4407-90f2-426c014d4da1
@echo off
cd C:\Program Files\QGIS 2.99\bin
call o4w_env.bat
call qt5_env.bat
call py3_env.bat
@echo off
path %OSGEO4W_ROOT%\apps\qgis-dev\bin;C:\Program Files\Git\cmd;C:\Users\aimplementacion\AppData\Local\Programs\Python\Python36\Scripts;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-dev
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-dev\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-dev\python;C:\Users\aimplementacion\AppData\Local\Programs\Python\Python36\Lib\site-packages;%PYTHONPATH%

ECHO Se inician pruebas
REM xvfb-run xbnose2-3
python update_project_generator.py C:\Users\aimplementacion\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\projectgenerator C:\Users\aimplementacion\Asistente-LADM_COL\asistente_ladm_col
cd C:\Users\aimplementacion\Asistente-LADM_COL
git pull origin master
rem "%PYTHONHOME%\python" main.py
nose2
