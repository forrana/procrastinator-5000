from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from procrastinator.auth import login_required
from procrastinator.db import get_db

bp = Blueprint('settings', __name__)


@bp.route('/settings')
@login_required
def settings():
    db = get_db()
    categories = db.execute(
        ' SELECT id, title, description, is_positive, icon, user_id'
        ' FROM category'
    ).fetchall()
    category_activities = {}
    for category in categories:
        activities = db.execute(
            ' SELECT id, title, description, score, icon, category_id'
            ' FROM activity WHERE category_id = {}'.format(category['id'])
        ).fetchall()
        category_activities[category['id']] = activities
    return render_template('settings/settings.html', activities=category_activities, categories=categories)


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

@bp.route('/<int:id>/activity', methods=('GET', 'POST', 'DELETE'))
def activity():
    activity = get_activity(id)

    if request.method == 'POST':
        db = get_db()
        db.execute(
            'UPDATE record SET finished_at = ?, is_active = ?'
            ' WHERE id = ?,',
            (True, False, id)
        )
        db.commit()
        return redirect(url_for('settings.index'))

    if request.method == 'DELETE':
        db = get_db()
        db.execute('DELETE FROM record WHERE id = ?', (id,))
        db.commit()
        return redirect(url_for('settings.index'))

    return render_template('settings/activity.html', record=record)

@bp.route('/activity/create', methods=('GET','POST'))
def activity_create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        score = request.form['score']
        category_id = request.form['category_id']
        error = None

        if not title:
            error = 'title is required.'

        if not score:
            error = 'score is required.'

        if not category_id:
            error = 'category is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO activity (title, description, score, category_id, user_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, description, score, category_id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('settings.index'))

    return render_template('settings/category_create.html')

@bp.route('/<int:id>/category', methods=('GET', 'POST', 'DELETE'))
def category():
    category = get_category(id)

    if request.method == 'POST':
        db = get_db()
        db.execute(
            'UPDATE record SET finished_at = ?, is_active = ?'
            ' WHERE id = ?,',
            (False, False, id)
        )
        db.commit()
        return redirect(url_for('settings.index'))

    if request.method == 'DELETE':
        db = get_db()
        db.execute('DELETE FROM record WHERE id = ?', (id,))
        db.commit()

    return render_template('settings/category.html', category=category)


@bp.route('/category/create', methods=('GET','POST'))
def category_create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        is_positive = request.form['is_positive']
        error = None

        if not title:
            error = 'title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO category (title, description, is_positive, user_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, description, is_positive, g.user['id'])
            )
            db.commit()
            return redirect(url_for('settings.index'))

    return render_template('settings/category_create.html')