from expense import app
from expense.routes import init_routes
from flask import request, jsonify

init_routes()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
