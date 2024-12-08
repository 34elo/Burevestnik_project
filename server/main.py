from flask import Flask
from flask_server.get_routes import get_data_users, get_data_repair_hardware, get_data_hardware, send_message
from flask_server.post_routes import hash_password, add_data_users, add_data_repair_hardware, add_data_hardware
from flask_server.put_routes import update_data_users, update_data_repair_hardware, update_data_hardware

app = Flask(__name__)

app.add_url_rule('/password', view_func=hash_password, methods=['POST'])

app.add_url_rule('/data/users', view_func=get_data_users, methods=['GET'])
app.add_url_rule('/data/repair_hardware', view_func=get_data_repair_hardware, methods=['GET'])
app.add_url_rule('/data/hardware', view_func=get_data_hardware, methods=['GET'])
app.add_url_rule('/send_message', view_func=send_message, methods=['GET'])

app.add_url_rule('/data/users', view_func=add_data_users, methods=['POST'])
app.add_url_rule('/data/hardware', view_func=add_data_hardware, methods=['POST'])
app.add_url_rule('/data/repair_hardware', view_func=add_data_repair_hardware, methods=['POST'])

app.add_url_rule('/data/users/<string:data_nickname>', view_func=update_data_users, methods=['PUT'])
app.add_url_rule('/data/repair_hardware/<int:data_id>', view_func=update_data_repair_hardware, methods=['PUT'])
app.add_url_rule('/data/hardware/<int:data_id>', view_func=update_data_hardware, methods=['PUT'])


def run_flask():
    app.run(port=5000, debug=False, host='0.0.0.0')


if __name__ == "__main__":
    run_flask()
