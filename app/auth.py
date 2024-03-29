import functools
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user['verified'] == 0:
            return redirect(url_for('auth.unverified'))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Users WHERE id = ?', (user_id,)
        ).fetchone()
        


@bp.route('/unverified')
def unverified():
    return render_template('auth/unverified.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM Users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {0} is already registered.'.format(username)

        if not username.endswith('@comp-soc.com'):
            error = 'Registration is restricted to @comp-soc.com addresses.'

        if error is None:
            # the name is available, store it in the database and go to
            # the login page

            verification = str(uuid.uuid4())

            db.execute(
                'INSERT INTO Users (username, password, verified, verification) VALUES (?, ?, 0, ?)',
                (username, generate_password_hash(password), verification)
            )
            db.commit()
            flash({'text': 'Registered user successfully', 'type': 'success'})
            return redirect(url_for('auth.login'))

        flash({'text': error, 'type': 'danger'})

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM Users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard.show_index'))

        flash({'text': error, 'type': 'danger'})

    return render_template('auth/login.html')

@bp.route('/verify/<token>', methods=('GET',))
def verify_user(token):
    db = get_db()


    db.execute('UPDATE Users SET verified=1, verification=NULL WHERE verification=?', ( token, ))
    db.commit()
    flash({'text': 'Verified user successfully', 'type': 'success'})

    return redirect(url_for('auth.login'))


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))
