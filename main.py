from flask import Flask
from flask import request, redirect, url_for
from flask import render_template
import re
from urllib.parse import quote

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        width = request.form.get('width')
        height = request.form.get('height')
        return redirect(url_for('handle_link', link=input_text, width=width, height=height))

    return render_template('home.html')


@app.route('/error')
def error():
    return '''
            There appears to be an issue with the provided link, width, or height parameters. <br>
            Please double-check them for accuracy. <br>
            The video link should follow the format "/dQw4w9WgXcQ". <br>
            The width and height parameters should be positive integer values. <br>            
            '''


def valid_int_parameter(param):
    if not isinstance(param, int):
        return False
    if param < 0:
        return False
    return True


def valid_link(param):
    is_valid = re.match(r'^(http(s)??\:\/\/)?(www\.)?((youtube\.com\/embed\/)|(youtu.be\/))([a-zA-Z0-9\-_])+$', param)
    if is_valid is None:
        return False
    return True


@app.route('/<link>')
def handle_link(link):

    url = "https://www.youtube.com/embed/" + quote(link, safe='')
    if not valid_link(url):
        return redirect(url_for('error'))

    width = int(request.args.get('width', default=900, type=int))
    height = int(request.args.get('height', default=600, type=int))

    if not valid_int_parameter(width):
        return redirect(url_for('error'))

    if not valid_int_parameter(height):
        return redirect(url_for('error'))

    return render_template('video.html', width=width, height=height, url=url)


if __name__ == '__main__':
    app.run()
