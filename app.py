from flask import Flask, render_template, request, jsonify
# test

app = Flask(__name__)

current_temp = "N/A"
led_state = False
messages = []  # va fi o listă cu maxim 10 mesaje

@app.route('/', methods=['GET', 'POST'])
def index():
    global led_state

    if request.method == 'POST':
        action = request.form.get('action')
        # Aici doar salvăm comanda – clientul local va trebui să o preia
        if action == 'ON':
            led_state = True
        elif action == 'OFF':
            led_state = False

    return render_template('index.html',
                           temperature=current_temp,
                           led_state=led_state,
			   messages=messages)

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
            messages = messages[-10:]  # păstrează doar ultimele 10

    return jsonify({'status': 'ok'})

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})


if __name__ == '__main__':
    app.run(debug=True)
