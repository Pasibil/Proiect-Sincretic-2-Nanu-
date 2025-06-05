from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

current_temp = "N/A"
led_state = False
messages = []
flood_events = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global led_state

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'ON':
            led_state = True
        elif action == 'OFF':
            led_state = False

    return render_template('index.html',
                           temperature=current_temp,
                           led_state=led_state,
                           messages=messages,
                           flood_events=flood_events)

@app.route('/update', methods=['POST'])
def update_temp():
    global current_temp
    data = request.get_json()
    if 'temperature' in data:
        current_temp = data['temperature']
    return jsonify({'status': 'ok'})

@app.route('/led_command')
def get_led_command():
    return jsonify({'led': 'ON' if led_state else 'OFF'})

@app.route('/send_message', methods=['POST'])
def send_message():
    global messages
    data = request.get_json()
    msg = data.get('message', '').strip()

    if msg:
        messages.append(msg)
        if len(messages) > 10:
            messages[:] = messages[-10:]

    return jsonify({'status': 'ok'})

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})

@app.route('/flood_event', methods=['POST'])
def flood_event():
    global flood_events
    data = request.get_json()
    if data is None or data.get('flood', True):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flood_events.append(f"Inundație detectată la {now}")
        if len(flood_events) > 10:
            flood_events[:] = flood_events[-10:]

    return jsonify({'status': 'ok'})

@app.route('/get_flood_events')
def get_flood_events():
    return jsonify({'flood_events': flood_events})

@app.route('/delete_flood/<int:index>', methods=['POST'])
def delete_flood(index):
    global flood_events
    if 0 <= index < len(flood_events):
        flood_events.pop(index)
        return jsonify({'status': 'deleted'})
    return jsonify({'status': 'error'})

@app.route('/sync_flood_events', methods=['POST'])
def sync_flood_events():
    global flood_events
    data = request.get_json()
    if data and 'flood_events' in data:
        flood_events = data['flood_events'][-10:]
    return jsonify({'status': 'ok'})

@app.route('/refresh_lists', methods=['POST'])
def refresh_lists():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
