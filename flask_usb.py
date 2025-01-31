from flask import Flask, request, jsonify
import serial

# Initialize Flask app
app = Flask(__name__)

# Configure the serial port (COM1 for writing)
SERIAL_PORT = 'COM1'  # Replace with the correct port if needed
BAUD_RATE = 9600      # Adjust to match Docklight configuration

def send_to_serial(message):
    """Sends a message to the serial port."""
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            ser.write(message.encode('utf-8'))  # Send the message
            return True
    except serial.SerialException as e:
        print(f"Serial port error: {e}")
        return False
    except Exception as e:
        print(f"General error: {e}")
        return False


@app.route('/', methods=['GET'])
def home():
    """Home route with a form to submit a message."""
    return '''
        <html>
            <head>
                <title>Flask USB Communication</title>
            </head>
            <body>
                <h1>Send a Message via USB</h1>
                <form action="/message" method="POST">
                    <label for="message">Message:</label><br>
                    <input type="text" id="message" name="message" required><br><br>
                    <input type="submit" value="Send">
                </form>
            </body>
        </html>
    '''

@app.route('/message', methods=['POST'])
def handle_message():
    """Handles message submission and sends it to the serial port."""
    message = request.form.get('message', 'No message provided')

    if send_to_serial(message):
        response = {"status": "success", "message": f"Message '{message}' sent to serial port!"}
    else:
        response = {"status": "error", "message": "Failed to send message to serial port."}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
