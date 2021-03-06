:: Es un script en batch
ECHO OFF
pushd %~dp0
set initialpath=%cd%
popd

ECHO Actualizando repositorio
cd C:\Users\aimplementacion\Asistente-LADM_COL
git fetch --all
git reset --hard origin/master
git pull origin master

ECHO Se actualiza projectgenerator antes de configurar python qgis
cd %initialpath%
python update_project_generator.py C:\Users\aimplementacion\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\projectgenerator C:\Users\aimplementacion\Asistente-LADM_COL\asistente_ladm_col

ECHO Configurando entorno de python qgis
rem https://qgis.org/downloads/weekly/QGIS-OSGeo4W-2.99.0-51-Setup-x86_64.exe # old
rem https://qgis.org/downloads/QGIS-OSGeo4W-3.0.0-3-Setup-x86_64.exe # new
rem C:\Users\aimplementacion\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
rem https://answers.microsoft.com/es-es/windows/forum/windows_10-other_settings-winpc/windows-10-programar-una-tarea-cómo-programar/dd0be19b-0365-4407-90f2-426c014d4da1
@echo off
set QGIS_INSTALLATION_PATH=C:\Program Files\QGIS 3.3
cd %QGIS_INSTALLATION_PATH%\bin
call o4w_env.bat
call qt5_env.bat
call py3_env.bat
@echo off
echo %QGIS_INSTALLATION_PATH% is equals to %OSGEO4W_ROOT% ?
path %OSGEO4W_ROOT%\apps\qgis-dev\bin;C:\Program Files\Git\cmd;C:\Users\aimplementacion\AppData\Local\Programs\Python\Python36\Scripts;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-dev
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-dev\qtplugins;%OSGEO4W_ROOT%\apps\Qt5\plugins
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-dev\python;%OSGEO4W_ROOT%\apps\qgis-dev\python\plugins;C:\Users\aimplementacion\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins;C:\Users\aimplementacion\AppData\Local\Programs\Python\Python36\Lib\site-packages;%PYTHONPATH%

ECHO Se termina configuracion de ambiente de pruebas
REM xvfb-run xbnose2-3

cd C:\Users\aimplementacion\Asistente-LADM_COL
rem "%PYTHONHOME%\python" main.py
ECHO Se compilan recursos
cd C:\Users\aimplementacion\Asistente-LADM_COL\asistente_ladm_col
ECHO Inicia pyrcc5
REM pyrcc5 -version
REM pyrcc5 -o resources_rc.py resources.qrc
python -m PyQt5.pyrcc_main -o resources_rc.py resources.qrc
cd C:\Users\aimplementacion\Asistente-LADM_COL
ECHO Se inician pruebas NOSE2
nose2
