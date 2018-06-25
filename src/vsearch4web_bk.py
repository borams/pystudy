from flask import Flask, render_template, request, escape
from vsearch import search4letters
from datetime import datetime
import mysql.connector

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    # with open('vsearch.log', 'a') as log:
    #     print(datetime.now(), req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    dbconnect = {'host': 'db',
                 'user': 'vsearch',
                 'password': 'vsearch',
                 'database': 'vsearchlogDB'}

    conn = mysql.connector.connect(**dbconnect)
    cursor = conn.cursor()
    _SQL = """INSERT INTO log (phrase, letters, ip, browser_string, results)
              VALUES(%s, %s, %s, %s, %s)"""

    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res,))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html', the_title='Here are your resluts', the_phrase=phrase, the_letters=letters, the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4results!')


@app.route('/viewlog')
def view_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    row_titles = ['Request Time', 'Form Data', 'Remote_addr', 'User_agent', 'Results']
    return render_template('viewlog.html',
                           the_title='View Logs History',
                           the_row_titles=row_titles,
                           the_data=contents)


app.run(host='0.0.0.0', debug=True, port=80)
