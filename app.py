import asyncio

from flask import Flask, request, render_template, jsonify

from working import send_to_specific_devices

# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)  # Enable CORS to allow frontend requests

@app.route('/')
def index():
    return render_template('index.html')  # Serves the frontend UI

@app.route('/save_password', methods=['POST'])
def save_password():
    data = request.get_json()
    password = data.get('password')

    if password:
        asyncio.run(send_to_specific_devices())
        # with open("passwords.txt", "a") as file:
        #     file.write(password + "\n")
        # return jsonify({"message": "Password saved successfully!"}), 200
    else:
        return jsonify({"message": "No password provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)
