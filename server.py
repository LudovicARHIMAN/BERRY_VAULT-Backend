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

# Connexion d'un utilisateur déjà référencé
@socketio.on('login')
def handle_login(data):
    login = data['login']
    password = data['password']
    if passwd.login_check(login,password):
        socketio.emit('login_response', {'success': True})
    else:
        socketio.emit('login_response', {'success': False})


# Ajout d'un nouvel utilisater
@socketio.on('new_user')
def handle_login(data):
    login = data['login']
    password = data['password']
    
    if user_manager.user_exist(login):
        socketio.emit('new_user_res', {'success': False})
    else:
        user_manager.new_user(login,password)
        socketio.emit('new_user_res', {'success': True})


# affiche les login et password
@socketio.on('display_password_login')
def handle_login(data):
    login = data['login']
    pass_name = data['pass_name']
    
    if user_manager.user_exist(login):
        socketio.emit('new_user_res', {'success': False})
    else:
        vault_manager.dis(login,pass_name)
        socketio.emit('new_user_res', {'success': True})




if __name__ == '__main__':
    socketio.run(app, debug=True)
