import flask
import sqlite3
from flask import request, redirect, url_for, jsonify
import os

# Set up the database:
api_database = sqlite3.connect('history.db')

app = flask.Flask(__name__)

uplink_status = {}

# Initialize uplink status
uplink_enabled = False
uplink_authorized = False
uplink_active = False

# API credentials
uplink_code = 'c2fa26d57cd69ed4cf86f1a9cf8f0232cc20b24387e3299aa267224722bd31ef'
authorization_code = '4a2dbd905287e75a5d2b659d2546fbab79abb21689e50f59492612df59bff460'

# Initialize IP's for the other hosts on the network
launch_control_ip = ''
authorization_center_ip = ''

# Redirect to uplink status if no API path is specified
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('status'), code=302)

# ------------------ API VERSION 3 ------------------

# Check sattelite status
@app.route('/api/v3/uplink', methods=['GET'])
def status():
    global uplink_active
    global uplink_enabled
    global uplink_authorized
    global launch_control_ip
    global authorization_center_ip
    try:
        if uplink_active:
            return '[*] Uplink active to {} and {} [*]'.format(launch_control_ip, authorization_center_ip)
        else:
            if uplink_enabled == True and uplink_authorized == True:
                os.system('ufw allow from {}'.format(launch_control_ip))
                os.system('ufw allow from {}'.format(authorization_center_ip))
                uplink_active = True
                return '[*] Activated uplink to {} and {} [*]'.format(launch_control_ip, authorization_center_ip)
            else:
                uplink_status['Uplink Enabled'] = uplink_enabled
                uplink_status['Uplink Authorized'] = uplink_authorized
                return jsonify(uplink_status)
    except Exception as exception_message:
        return '[?] The following exception has occured: {}'.format(exception_message)

# Enable the sattelite uplink
@app.route('/api/v3/enable', methods=['GET'])
def enable():
    global uplink_enabled
    global uplink_code
    global launch_control_ip
    try:
        if 'code' in request.args:
            provided_code = str(request.args['code'])
            if provided_code == uplink_code:
                uplink_enabled = True
                launch_control_ip = str(request.remote_addr)
                return '[+] Success: Uplink Enabled [+]'
            else:
                return '[!] Error: Invalid Uplink Code [!]'
        else:
            return '[!] Error: Please provide an uplink code [!]'
    except Exception as exception_message:
        return '[?] The following exception has occured: {}'.format(exception_message)

# Authorize the sattelite uplink
@app.route('/api/v3/authorize', methods=['GET'])
def authorize():
    global uplink_authorized
    global authorization_code
    global authorization_center_ip
    try:
        if 'code' in request.args:
            provided_code = str(request.args['code'])
            if provided_code == authorization_code:
                uplink_authorized = True
                authorization_center_ip = str(request.remote_addr)
                return '[+] Success: Uplink Authorized [+]'
            else:
                return '[!] Error: Invalid Authorization Code [!]'
        else:
            return '[!] Error: Please provide an authorization code [!]'
    except Exception as exception_message:
        return '[?] The following exception has occured: {}'.format(exception_message)

# ------------------ API VERSION 2 ------------------

@app.route('/api/v2/history', methods=['GET'])
def history():
    try:
        if 'record' in request.args:
            record = str(request.args['record'])
            history_sqlite = sqlite3.connect('history.db')
            history_cursor = history_sqlite.cursor()
            history_cursor.execute('SELECT %s FROM firing_history;' % record)
            return str(history_cursor.fetchall())
        else:
            return '[!] Error: Missing record parameter. Do * to show all records [!]'
    except Exception as exception_message:
        return '[?] The following exception has occured: {}'.format(exception_message)

# ------------------ API VERSION 1 ------------------

# Check sattelite network connection
@app.route('/api/v1/connection', methods=['GET'])
def connection():
    try:
        if 'ip' in request.args:
            target_ip = str(request.args['ip'])
            ping = os.popen('ping -c 2 ' + target_ip)
            connection_status = ping.read()
            return connection_status
        else:
            return '[!] Error: Invalid IP parameter. Please provide the IP address for the launch center [!]'
    except Exception as exception_message:
        return '[?] The following exception has occured: {}'.format(exception_message)

app.run(host='0.0.0.0')