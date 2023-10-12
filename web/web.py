from config import *
from flask import Flask, render_template, request
from text import *

app = Flask(__name__,
            template_folder='../web/templates',
            static_folder='../web/static')

@app.route('/')
def get_form():
    return render_template('input.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        pid = result['input_1']
        text = IllustText(raw=crawler.illusts_text(pid=pid)).get_info()

        body = IllustPageText(raw=crawler.illust_pages_text(pid=pid)).get_body()
        url = body[0]["urls"]["original"]
        pic = crawler.img_original_content(url)
        file_name = STATIC_PATH + pid + ".png"
        file = open(file_name, "wb")
        file.write(pic)
        file.close()

        return render_template("output.html", text=text, pid=pid)


if __name__ == '__main__':
    app.run()

