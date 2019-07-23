import sqlite3
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
    jsonify, make_response
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def index():
    return render_template('/edit.html')

@bp.route('/addevent', methods = ['POST', 'GET'])
def add_event():
	if request.method == "POST":
		try:
			# name of event
			evt_name = request.form('evtname')
			# date/time of event
			evt_time = request.form('evttime')

			with sqlite3.connect(current_app.config['DATABASE'], \
				detect_types=sqlite3.PARSE_DECLTYPES) as con:
				cur = con.cursor()
				cur.execute("INSERT INTO Events (time, name) VALUES (?, ?)", \
					(evt_time, evt_name))
				con.commit()

			# TODO: return 200 and evtID
		except:
			con.revert()
			# return appropriate error code
			print("EVENT AHHHHH")
		finally:
			con.close()

@bp.route('/addcar', methods = ['POST', 'GET'])
def add_car():
	if request.method == "POST":
		try:
			# event foreign key
			evt_fk = request.form('evtfk')
			# number of seats in car
			car_seats = request.form('carseats')
			# whether this is a default car for unassigned people
			car_default = request.form('cardefault')

			# name of driver
			dvr_name = request.form('dvrname')

			with sqlite3.connect(current_app.config['DATABASE'], \
				detect_types=sqlite3.PARSE_DECLTYPES) as con:
				cur = con.cursor()
				cur.execute("INSERT INTO Cars (event_fk, seats, is_default)"
					"VALUES (?, ?, ?)", (evt_fk, car_seats, car_default))
				car_fk = cur.lastrowid
				cur.execute("INSERT INTO People (car_fk, name, driver)"
					"VALUES (?, ?, ?)", (car_fk, dvr_name, True))
				con.commit()

			# TODO: return 200 and car_fk
		except:
			con.revert()
			# return appropriate error code
			print("CAR AHHHHH")
		finally:
			con.close()

@bp.route('/addperson', methods = ['POST', 'GET'])
def add_person():
	if request.method == "POST":
		try:
			# car foreign key (SHOULD BE DEFAULT)
			car_fk = request.form('carfk')
			# person name
			per_name = request.form('pername')

			with sqlite3.connect(current_app.config['DATABASE'], \
				detect_types=sqlite3.PARSE_DECLTYPES) as con:
				curr = con.cursor()
				cur.execute("INSERT INTO People (car_fk, name, driver)"
					"VALUES (?, ?, ?)", (car_fk, per_name, False))
				con.commit()

			# TODO: return 200 and personID
		except:
			con.revert()
			# return appropriate error code
			print("PERSON AHHHHH")
		finally:
			con.close()



