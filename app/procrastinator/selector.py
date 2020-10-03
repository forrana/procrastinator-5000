from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from procrastinator.auth import login_required
from procrastinator.db import get_db

import datetime

bp = Blueprint('selector', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    categories = db.execute(
        ' SELECT id, title, description, is_positive, icon, user_id'
        ' FROM category'
    ).fetchall()
    category_activities = {}
    for category in categories:
        activities = db.execute(
            ' SELECT id, title, description, score, icon, category_id'
            ' FROM activity WHERE category_id = {}'
            ' ORDER BY score LIMIT 1'.format(category['id'])
        ).fetchall()
        category_activities[category['id']] = activities
    return render_template('selector/index.html', activities=category_activities, categories=categories)


@bp.route('/create/<int:category_id>', methods=('GET', 'POST'))
@login_required
def create(category_id):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO activity (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('selector.index'))

    return render_template('selector/create.html', category_id=category_id)

def get_category(id, check_user=True):
    category = get_db().execute(
        'SELECT id, is_positive, description, icon, user_id'
        'FROM category'
        'WHERE id = ?',
        (id,)
    ).fetchone()

    if category is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_user and category['author_id'] != g.user['id']:
        abort(403)

    return category

def get_post(id, check_user=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_user and post['author_id'] != g.user['id']:
        abort(403)

    return post

def get_record(id, check_user=True):
    record = get_db().execute(
        ' SELECT r.id, started_at, r.title, r.description, activity_id, r.user_id, a.title, is_active'
        ' FROM record r JOIN activity a ON r.activity_id = a.id'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()

    if record is None:
        abort(404, "Record id {0} doesn't exist.".format(id))

    if check_user and record['user_id'] != g.user['id']:
        abort(403)

    return record

def get_activity(id, check_user=True):
    activity = get_db().execute(
        ' SELECT r.id, title, description, score, icon, category_id, user_id, c.title'
        ' FROM activity a JOIN category c ON a.category_id = c.id'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()

    if activity is None:
        abort(404, "Activity id {0} doesn't exist.".format(id))

    if check_user and activity['user_id'] != g.user['id']:
        abort(403)

    return activity

@bp.route('/start/<int:activity_id>', methods=('GET',))
@login_required
def start(activity_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO record (is_active, user_id, activity_id)'
        ' VALUES (?, ?, ?)',
        (True, g.user['id'], activity_id)
    )
    db.commit()
    cratedRecordId = cursor.lastrowid
    return redirect(url_for('selector.record', id=cratedRecordId))

@bp.route('/record/<int:id>', methods=('GET', 'POST', 'DELETE'))
def record(id):
    record = get_record(id)

    if request.method == 'POST':
        db = get_db()
        finished_at = datetime.datetime.now()
        db.execute(
            'UPDATE record SET finished_at = ?, is_active = ?'
            ' WHERE id = ?,',
            (finished_at, False, id)
        )
        db.commit()
        return redirect(url_for('selector.index'))

    if request.method == 'DELETE':
        db = get_db()
        db.execute('DELETE FROM record WHERE id = ?', (id,))
        db.commit()

    if record['is_active']:
        return render_template('selector/active_record.html', record=record)
    return render_template('selector/inactive_record.html', record=record)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('selector.index'))

    return render_template('selector/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('selector.index'))
