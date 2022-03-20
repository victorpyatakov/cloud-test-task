from flask import Flask

from apis import blueprint as api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)






