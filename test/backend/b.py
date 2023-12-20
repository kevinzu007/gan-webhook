from flask import Flask, render_template, request, jsonify, g
from flask_socketio import SocketIO, join_room, leave_room
import subprocess


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('connect')
def on_connect():
    user_id = request.args.get('token')
    if user_id:
        join_room(user_id)
        g.user_id = user_id  # Store the user_id in the global g object
        print(f'WebSocket Client {request.sid} connected with user ID: {user_id}')
        print('ccccccccccccccccc')

@socketio.on('disconnect')
def on_disconnect():
    #user_id = request.args.get('token')
    # 这个修改的代码仍然有一些问题需要解决，例如g对象在多线程环境下可能无法正常工作，你可能需要寻找其他方式来存储用户的身份ID
    user_id = g.get('user_id', None)
    if user_id:
        leave_room(user_id)      # 离开房间
        print('WebSocket Client disconnected')



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_message', methods=['GET'])
def send_message():
    print('ssssssssssssssss')
    user_id = request.args.get('token')      # 获取连接时携带的用户身份ID
    cmd = "ping www.baidu.com -w 5"
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1)
    for info in iter(pipe.stdout.readline, b''):
        info = info.decode("utf-8")
        #print(info)
        print('kkkkkkkkkkkkkkkkkkkkkkk')
        socketio.emit('message', info, room=user_id)
        print('jjjjjjjjjjjjjjjjjjjj')
        socketio.sleep(0.5)
    #return jsonify('pipeppp: OK')
    return jsonify({})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9527, debug=True)


