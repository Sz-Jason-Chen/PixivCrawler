from flask import Flask  # ⑴

app = Flask(__name__)  # ⑵


@app.route('/')  # ⑶
def index():  # ⑷
    return 'Hello flask ！'  # ⑸


if __name__ == '__main__':
    app.run()  # ⑹