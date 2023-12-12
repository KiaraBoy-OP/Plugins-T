from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def start():
    return "KiaraBot Started Successfully"

os.system("python3 -m TelethonKiara")
app.run(port=5000)