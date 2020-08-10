# Copyright (c) 2020 Novus Space

###############################
#########  Web Server #########
###############################


from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, send_file, request, jsonify, redirect
from random import random
from time import sleep
from threading import Thread, Event
import serial

__author__ = 'alex'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()


def data_update():
    comData = serial.Serial('COM3', baudrate=115200, timeout=0)
    print("Making random numbers")
    count = 1
    while not thread_stop_event.isSet():
        number = comData.readline().decode('utf8')
        dataFile = open('lib/oldData/oldData.txt', 'a')
        dataFile.write('[VALUE : ' + str(count) + '] >> ' + number)
        dataFile.close()
        print(number)
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(1)
        count += 1


@app.route('/')
def index():
    return render_template('bootstrap.html')


database = {'admin': 'admin'}


@app.route('/data_update', methods=['POST', 'GET'])
def login():
    name1 = request.form['username']
    pwd = request.form['password']
    if name1 not in database:
        return render_template('bootstrap.html', info='Invalid User')
    else:
        if database[name1] != pwd:
            return render_template('bootstrap.html', info='Invalid Password')
        else:
            return render_template('index.html', name=name1)


@app.route('/data_update', methods=['POST', 'GET'])
def portStatus():
    if comData.isOpen():
        return render_template('index.html', status='available')
    else:
        return render_template('index.html', status='unvailable')


@app.route('/oldData', methods=['GET', 'POST'])
def oldData():
    path = "lib/oldData/oldData.txt"
    return send_file(path, as_attachment=True)


@app.route('/cool_form', methods=['GET', 'POST'])
def cool_form():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(data_update)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, '192.168.1.18')
