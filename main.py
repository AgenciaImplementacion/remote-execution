#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import os
import subprocess

from flask import Flask, flash, redirect, render_template, \
    request, url_for, send_file, send_from_directory, request

"""
Ingresa al navegador con:
http://mi.ip:5000/reporte/pdf?url_imagen=http://ip_serv/imagen.png
"""

app = Flask(__name__)
app.secret_key = 'some_secret'
app.othervar = 'scripts'


@app.route('/')
def index():
    return render_template('login.html')


def call_software():
    # os.system("C:/Users/aimplementacion/remote-execution/scripts/test_Asistente-LADM_COL.bat")
    # ouput = os.popen(
    #    "C:/Users/aimplementacion/remote-execution/scripts/test_Asistente-LADM_COL.bat").readlines()
    ouput = subprocess.check_output(["scripts/test_Asistente-LADM_COL.sh"], stderr=subprocess.STDOUT)
    return ouput


@app.route('/execute', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            stdouttext = call_software()
            print(stdouttext)
            handle, filepath = tempfile.mkstemp('.log', 'remote-execution-')
            #fd = os.open( "foo.txt", os.O_RDWR|os.O_CREAT )
            #fd = os.fdopen(handle)
            #nombre_archivo = filepath[filepath.rfind(os.sep) + 1:]
            #carpeta_archivo = filepath[0:filepath.rfind(os.sep) + 1]
            #print(nombre_archivo, carpeta_archivo)
            f = os.fdopen( handle, "w" )
            # f.write( "\n".join(stdouttext) )
            f.write(stdouttext.decode())
            f.close()
            #uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
            #return send_from_directory(directory=carpeta_archivo, filename=nombre_archivo)
            return send_file(filepath, as_attachment=True, attachment_filename="stdout.log")
            # return 'Se ejecutó exitosamente :D'
            # return redirect(url_for('index'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    # para produccion reemplazar por la IP correspondiente
    app.run(host="0.0.0.0", port=5000)
