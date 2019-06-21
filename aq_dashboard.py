"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from openaq import OpenAQ
import results


APP = Flask(__name__)

api = OpenAQ()

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    over10 = Record.query.filter(Record.value >= 10).all()
    

    """Base view."""
    return(str([over10]))

def get_dv():
    res = api.measurements(city='Los Angeles', parameter='pm25')[1]['results']

    date_val = []
    i = 0
    for r in res:
        date_val.append((r['date']['utc'], r['value']))
        i += 1
    return(date_val)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< "Date: {}, Measurement: {} ppM" >'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    
    dt_val = get_dv()
    for dv in dt_val:
        db_dt = Record(datetime=dv[0], value=dv[1])
        DB.session.add(db_dt)
    DB.session.commit()
    return 'Data refreshed!'



