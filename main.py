#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, flash, redirect, render_template, \
    request, url_for

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/')
def index():
    return render_template('index.html')


def call_software():
    from subprocess import call
    #call(["ls", "-l"])
    call(["cmd", "scripts/test_Asistente-LADM_COL.bat"])


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            call_software()
            return 'Se ejecutó exitosamente :D'
            #return redirect(url_for('index'))
    return render_template('login.html', error=error)
