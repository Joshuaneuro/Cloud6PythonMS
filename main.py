from flask import Flask, jsonify, request
from routes import routes

#init app
app = Flask(__name__)

#register routes
app.register_blueprint(routes)

#run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
