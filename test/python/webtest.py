from flask import Flask, render_template

app = Flask(__name__)

@app.route('/workspace')
def index():
    return render_template('test.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')