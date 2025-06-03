from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

current_temp = "N/A"
led_state = False

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
                           led_state=led_state)

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

if __name__ == '__main__':
    app.run(debug=True)
