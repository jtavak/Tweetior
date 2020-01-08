import MySQLdb
from flask import Flask, request, render_template
import poem_maker

host = ''
user = ''
passwd = ''
dbname = ''


def get_dropdown_values(tweeter):
    one, two, three, four, five = '', '', '', '', ''
    if tweeter == 'realDonaldTrump':
        one = 'selected'
    elif tweeter == 'TheEllenShow':
        two = 'selected'
    elif tweeter == 'ConanOBrien':
        three = 'selected'
    elif tweeter == 'BarackObama':
        four = 'selected'
    elif tweeter == 'jimmyfallon':
        five = 'selected'

    selected = """<option %s>realDonaldTrump</option>
    <option %s>TheEllenShow</option>
    <option %s>ConanOBrien</option>
    <option %s>BarackObama</option>
    <option %s>jimmyfallon</option>""" % (one, two, three, four, five)

    return selected


app = Flask(__name__)


@app.route('/')
def index():
    db = MySQLdb.connect(host, user, passwd, dbname)

    cur = db.cursor()
    poem = poem_maker.create_poem(8, 10, 10, 'realDonaldTrump', cur)
    twitter_poem = poem_maker.get_twitter_poem(poem)
    cur.close()
    db.close()
    choices = '<option selected>realDonaldTrump</option><option>TheEllenShow</option><option>ConanOBrien</option' \
              '><option>BarackObama</option><option>jimmyfallon</option> '

    return render_template('index.html', min_words=8, max_words=10, poem=poem, choices=choices,
                           twitter_poem=twitter_poem)


@app.route('/', methods=['post', 'get'])
def poem_maker_input():
    if request.method == 'POST':
        min_words = int(request.form.get('min_words_per_line'))
        max_words = int(request.form.get('max_words_per_line'))
        lines = request.form.get('lines')
        tweeter = request.form.get('tweeter')

        if not lines:
            lines = 10
        else:
            lines = int(lines)

        if min_words <= max_words:

            db = MySQLdb.connect(host, user, passwd, dbname)

            cur = db.cursor()
            poem = poem_maker.create_poem(min_words, max_words, lines, tweeter, cur)
            twitter_poem = poem_maker.get_twitter_poem(poem)
            cur.close()
            db.close()
        else:
            poem = ['Min words cannot be higher than max words.']

    choices = get_dropdown_values(tweeter)

    return render_template('index.html', min_words=min_words, max_words=max_words, poem=poem, lines=lines,
                           choices=choices, twitter_poem=twitter_poem)
