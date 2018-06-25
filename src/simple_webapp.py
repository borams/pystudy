from flask import Flask, session
from checker import check_logged_in

app = Flask(__name__)

app.secret_key = 'ThisIsNotSomethingThatYouCannotGuesss!;ld)#)('

@app.route('/')
def hello() -> str:
    return 'Hello from the simple webapp!'


@app.route('/page1')
@check_logged_in
def page1() -> str:
    return 'Page 1'


@app.route('/page2')
@check_logged_in
def page2() -> str:
    return 'Page 2'


@app.route('/page3')
@check_logged_in
def page3() -> str:
    return 'Page 4'


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are logged in!'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are logged out!'


@app.route('/status')
def status() -> str:
    if 'logged_in' in session:
        return 'You are logged in!'
    return 'You are logged out!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
