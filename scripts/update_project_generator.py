#!/usr/bin/env python3
import os
import sys
import shutil
import zipfile
import tempfile
import urllib.request

try:
    projectgenerator_path = sys.argv[1]
    asistente_ladm_col_path = sys.argv[2]
    projectgenerator_meta = os.path.join(projectgenerator_path, 'metadata.txt')
    asistente_ladm_col_meta = os.path.join(asistente_ladm_col_path, 'config/general_config.py')
    if not os.path.exists(projectgenerator_meta) or not os.path.exists(projectgenerator_meta):
        print('Alguna de las rutas no existe.')
        exit(1)
except Exception as e:
    print('Ingrese la ruta del plugin projectgenerator y asistente_ladm_col.')

try:
    for line in open(projectgenerator_meta):
        if 'version=' in line:
            key, _, value = line.partition("=")
            print('projectgenerator_meta key, value:', key, value)
            break
    version_installed_pg = value.strip()
    del value
    for line in open(asistente_ladm_col_meta):
        if 'PROJECT_GENERATOR_MIN_REQUIRED_VERSION = ' in line:
            key, _, value = line.partition(" = ")
            print('asistente_ladm_col_meta key, value:', key, value)
            break
    version_required_pg = value.strip().strip('"    ')
except ValueError as e:
    print('Error en el valor de la versión')

print('Versions installed and required:', version_installed_pg, ',', version_required_pg)

if version_installed_pg == version_required_pg:
    print('La versión actual cumple con los requerimientos.')
else:
    tmpFile = tempfile.mktemp()
    tmpDir = tempfile.mktemp()
    url = 'https://github.com/opengisch/projectgenerator/releases/download/v3.2.3/projectgenerator-v{version}.zip'.format(version=version_required_pg)
    print('tmpDir, tmpFile, url', tmpDir, tmpFile, url)
    urllib.request.urlretrieve(url, tmpFile)
    with zipfile.ZipFile(tmpFile, "r") as zip_ref:
        zip_ref.extractall(tmpDir)
        os.remove(tmpFile)
        shutil.rmtree(projectgenerator_path)
        shutil.move(tmpDir + '/projectgenerator', projectgenerator_path)
        shutil.rmtree(tmpDir)
