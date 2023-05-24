from flask import Flask
app = Flask(__name__)
DATABASE = "fortunes_and_users"
app.secret_key = "shhhhhh"