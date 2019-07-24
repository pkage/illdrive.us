all: run

run:
	FLASK_APP=app.py FLASK_ENV=development flask run

init-db:
	FLASK_APP=app.py FLASK_ENV=development flask init-db
