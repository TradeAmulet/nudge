# services/web/server/api/views.py


import redis
from rq import Queue, push_connection, pop_connection
from flask import current_app, render_template, Blueprint, jsonify, request

from server.tasks.tasks import create_task
from server.sockets.exchanges.poloniex_socket import PoloniexSocket

main_blueprint = Blueprint('tasks', __name__,)

@main_blueprint.route('/', methods=['GET'])
def home():
    return render_template('main/home.html')


@main_blueprint.route('/tasks', methods=['POST'])
def run_task():
    words = request.form['words']
    q = Queue()
    task = q.enqueue(create_task, words)
    response_object = {
        'status': 'success',
        'data': {
            'task_id': task.get_id()
        }
    }
    return jsonify(response_object), 202


@main_blueprint.route('/tasks/<task_id>', methods=['GET'])
def get_status(task_id):
    q = Queue()
    task = q.fetch_job(task_id)
    if task:
        response_object = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
                'task_result': task.result,
            }
        }
    else:
        response_object = {'status': 'error'}
    return jsonify(response_object)


@main_blueprint.before_request
def push_rq_connection():
    push_connection(redis.from_url(current_app.config['REDIS_URL']))


@main_blueprint.teardown_request
def pop_rq_connection(exception=None):
    pop_connection()


@main_blueprint.route('/websockets/start/<market_id>', methods=['GET'])
def start_websocket(market_id):
    print("Recognizing route")
    socket_manager = PoloniexSocket()
    socket_manager.start_ws()
