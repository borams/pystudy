from flask import Flask, render_template, request, escape, session
from vsearch import search4letters
from datetime import datetime
from DBcm import UseDatabase
from checker import check_logged_in
import mysql.connector

app = Flask(__name__)
app.config['dbconfig'] = {'host': 'db',
                          'user': 'vsearch',
                          'password': 'vsearch',
                          'database': 'vsearchlogDB'}
app.secret_key = 'ThisIsVsearch4webSecretKey!#%##$!'

def log_request(req: 'flask_request', res: str) -> None:
    # with open('vsearch.log', 'a') as log:
    #     print(datetime.now(), req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """INSERT INTO log (phrase, letters, ip, browser_string, results)
                  VALUES(%s, %s, %s, %s, %s)"""

        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res,))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    try:
        log_request(request, results)
    except Exception as err:
        print('***** Logging failed with this error:', str(err))
    return render_template('results.html', the_title='Here are your resluts', the_phrase=phrase, the_letters=letters, the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4results!')


@app.route('/viewlog')
@check_logged_in
def view_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """SELECT ts, phrase, letters, ip, browser_string, results
                      FROM log;"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('Created Time', 'Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title = 'View Log',
                               the_row_titles = titles,
                               the_data = contents,)
    except mysql.connector.errors.InterfaceError as err:
        print('Error: ', str(err))
        # print('Error:', type(err))
    except Exception as err:
        print('Error2: ', str(err))

@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are logged in!'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are logged out!'


@app.route('/status')
def check_status() -> str:
    if 'logged_in' in session:
        return 'You are currenlty logged in!'
    return 'You are NOT logged in!'


app.run(host='0.0.0.0', debug=True, port=80)
