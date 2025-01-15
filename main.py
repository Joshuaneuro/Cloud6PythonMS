from flask import Flask
from Controllers.GamesController import routes

#init app
app = Flask(__name__)

# Initialize and register the controller
games_controller = GamesController()
app.register_blueprint(games_controller.routes)

#run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
