#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import os
import subprocess
import sys

from flask import Flask, flash, redirect, render_template, \
    request, url_for, send_file, send_from_directory, request
	
from shutil import copyfile

"""

"""

app = Flask(__name__)
app.secret_key = 'some_secret'
app.defaultpath = 'logs'


@app.route('/')
def index():
    return render_template('login.html')


def call_software():
	output = b"vacio"
	#output = bytearray()
	is_windows = hasattr(sys, 'getwindowsversion')
	if (is_windows):
		try:
			output = subprocess.check_output(["scripts\\test_Asistente-LADM_COL.bat"], stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as e:
			output = e.output
			print("Error")
			print(e.output)	
	else:
		output = subprocess.check_output(["scripts/test_Asistente-LADM_COL.sh"], stderr=subprocess.STDOUT)

    #os.system("C:/Users/aimplementacion/remote-execution/scripts/test_Asistente-LADM_COL.bat")
    # ouput = os.popen(
    #    "C:/Users/aimplementacion/remote-execution/scripts/test_Asistente-LADM_COL.bat").readlines()
	return output

def get_version():
	p = subprocess.Popen(["git", "rev-parse", "HEAD"], cwd="C:\\Users\\aimplementacion\\Asistente-LADM_COL", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()
	return p.stdout.readline().decode("utf-8").replace('\n', '')

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
            print("stdouttext", stdouttext)
            print("gitv", get_version())
            print("type", type(get_version()))
            handle, filepath = tempfile.mkstemp()
            #fd = os.open( "foo.txt", os.O_RDWR|os.O_CREAT )
            #fd = os.fdopen(handle)
            #nombre_archivo = filepath[filepath.rfind(os.sep) + 1:]
            #carpeta_archivo = filepath[0:filepath.rfind(os.sep) + 1]
            #print(nombre_archivo, carpeta_archivo)
            f = os.fdopen( handle, "w" )
            # f.write( "\n".join(stdouttext) )
            f.write(stdouttext.decode())
            f.close()
            destino = app.defaultpath + os.sep + "log_" + get_version() + ".log"
            copyfile(filepath, destino)
            #uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
            #return send_from_directory(directory=carpeta_archivo, filename=nombre_archivo)
            return send_file(filepath, as_attachment=True, attachment_filename="stdout.log")
            # return 'Se ejecutó exitosamente :D'
            # return redirect(url_for('index'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    # para produccion reemplazar por la IP correspondiente
    app.run(host="0.0.0.0", port=5000)
