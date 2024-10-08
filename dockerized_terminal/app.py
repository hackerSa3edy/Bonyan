from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import docker
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
# import pyte
import socket
import logging
from flask_jwt_extended.exceptions import NoAuthorizationError

app = Flask(__name__)
app.config['SECRET_KEY'] = r'django-insecure-%2dmqnqj9v2e&8yk*t=#b+2-=i!45+153*@-g0*=&%1od16z^m'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key' # fake: jwt-secret-string
app.config['JWT_IDENTITY_CLAIM'] = 'user_id'  # Change this if you want to use a different claim
app.config['JWT_ACCESS_COOKIE_NAME'] = 'jwtAccess'
app.config['JWT_REFRESH_COOKIE_NAME'] = 'jwtRefresh'
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# @jwt.user_identity_loader
# def user_identity_lookup(identity):
#     return identity

# Initialize Docker client
# client = docker.from_env()
client = docker.DockerClient(base_url='tcp://host.docker.internal:2375')

# Dictionary to hold references to terminal emulators
terminals = {}

# Initialize logging
logging.basicConfig(level=logging.INFO)

@app.route('/terminal', strict_slashes=False)
@jwt_required(locations=['headers', 'cookies'])
def index():
    # token = get_jwt()
    # print('token:', token)
    return render_template('index.html')

# Handle socket events
@socketio.on('connect')
@jwt_required(locations=['headers', 'cookies'])
def handle_connect():
    emit('message', {'data': 'Connected'})

@socketio.on('disconnect')
@jwt_required(locations=['headers', 'cookies'])
def handle_disconnect():
    JWTtoken = get_jwt()

    role = JWTtoken['user_role']
    user_id = JWTtoken['user_id']

    try:
        container = client.containers.get(f'{role}-{user_id}')
    except docker.errors.NotFound:
        pass
    else:
        container.stop()
    emit('message', {'data': 'Disconnected'})

@socketio.on('start_terminal')
@jwt_required(locations=['headers', 'cookies'])
def handle_start_terminal(data):
    namespace = request.namespace  # Get the namespace from the request
    logging.info('Starting terminal...')

    JWTtoken = get_jwt()
    role = JWTtoken['user_role']
    user_id = JWTtoken['user_id']
    try:
        try:
            container = client.containers.get(f'{role}-{user_id}')
        except docker.errors.NotFound:
            # print('false')
            container = client.containers.run('holbertonschool/265-0:latest', '/bin/bash', tty=True, stdin_open=True, detach=True, name=f'{role}-{user_id}', hostname=f'{role}-{user_id}')

        container.start()
        stream = container.attach_socket(params={'stdin': 1, 'stdout': 1, 'stderr': 1, 'stream': 1})
    except Exception as e:
        logging.error('Failed to start terminal: %s', e)
        return

    terminals[container.id] = stream
    stream._sock.send(b'\n')

    emit('terminal_started', {})
    read_socket(namespace, container.id, broadcast=False)

@socketio.on('input')
@jwt_required(locations=['headers', 'cookies'])
def handle_input(data):
    JWTtoken = get_jwt()
    role = JWTtoken['user_role']
    user_id = JWTtoken['user_id']

    container = client.containers.get(f'{role}-{user_id}')
    input_data = data['input']
    stream = terminals[container.id]

    stream._sock.send(input_data.encode('utf-8'))

    # read_socket(namespace, container_id, broadcast=False)

def read_socket(namespace, container_id, broadcast=True):
    stream = terminals[container_id]
    with app.app_context():
        # Read all output from the socket
        while True:
            output = b''
            try:
                chunk = stream._sock.recv(1024)
                if len(chunk) == 0:
                    break
                output += chunk
            except socket.timeout:
                break

            emit('output', {'output': output.decode()}, namespace=namespace, broadcast=broadcast)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
