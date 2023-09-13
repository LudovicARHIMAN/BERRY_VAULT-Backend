'''
Ce fichier ce charge de gérer les intéractions client-server
'''
from flask import Flask, request
from flask_socketio import SocketIO
import user_manager
import retriver 
import vault_manager
import password as passwd


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('login')
def handle_login(data):
    login = data['login']
    password = data['password']

    

    if passwd.login_check(login,password):
        socketio.emit('login_response', {'success': True})
    else:
        socketio.emit('login_response', {'success': False})



if __name__ == '__main__':
    socketio.run(app, debug=True)
