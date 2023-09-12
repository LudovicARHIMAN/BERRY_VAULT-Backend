'''
Ce fichier ce charge de gérer les intéractions client-server
'''
# Importation des modules 
import socketio # websocket pour communiquer avec les clients 
import eventlet #  `basic API primitives` module 



# Connexion client-server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print(f'Client {sid} connected')

@sio.event
def disconnect(sid):
    print(f'Client {sid} disconnected')



@sio.on('message')
def handle_message(sid, data):
    print(f'Received message: {data}')
    sio.emit('response', data)  # envoie la réponse aux clients


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 8080)), app)



