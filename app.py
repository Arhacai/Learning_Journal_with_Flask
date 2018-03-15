from flask import (Flask, g, render_template, flash, redirect, url_for, abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import utils
import models
import forms

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'aksdhk2je3hr4%$wsefjkasdR"r4kljsfdf$'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each requests."""
    g.db.close()
    return response


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('show_entries'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('show_entries'))


@app.route('/entry', methods=('GET', 'POST'))
@login_required
def add_entry():
    form = forms.AddEntry()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data.strip(),
            date=form.date.data,
            time=form.time.data,
            learned=form.learned.data.strip(),
            resources=form.resources.data.strip(),
            tags=form.tags.data.strip()
        )
        flash("Journal entry saved!", "success")
        return redirect(url_for('show_entries'))
    return render_template('new.html', form=form)


@app.route('/')
@app.route('/entries')
@app.route('/entries/<tag>')
def show_entries(tag=None):
    if tag:
        entries = models.Entry.select().where(
            models.Entry.tags.contains(tag)
        )
        if entries.count() == 0:
            abort(404)
    else:
        entries = models.Entry.select().order_by(
                models.Entry.date.desc()
            )
    return render_template('index.html', entries=entries)


@app.route('/details/<slug>')
@login_required
def show_details(slug):
    try:
        entry = models.Entry.get(
            models.Entry.slug == slug
        )
    except models.DoesNotExist:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route('/entries/edit/<slug>', methods=('GET', 'POST'))
@login_required
def edit_entry(slug):
    try:
        entry = models.Entry.get(
            models.Entry.slug == slug
        )
    except models.DoesNotExist:
        abort(404)
    else:
        form = forms.EditEntry()
        if form.validate_on_submit():
            edited_entry = models.Entry.update(
                title=form.title.data.strip(),
                date=form.date.data,
                time=form.time.data,
                learned=form.learned.data.strip(),
                resources=form.resources.data.strip(),
                tags=form.tags.data.strip()
            ).where(models.Entry.slug == slug)
            edited_entry.execute()
            new_entry = models.Entry.get(
                models.Entry.slug == slug
            )
            new_entry.slug = utils.slugify(entry.title)
            new_entry.save()
            flash("Entry edited successfully", "success")
            return redirect(url_for('show_entries'))
        return render_template('edit.html', form=form)


@app.route('/entries/delete/<slug>')
@login_required
def delete_entry(slug):
    try:
        entry = models.Entry.get(models.Entry.slug == slug)
    except models.DoesNotExist:
        abort(404)
    else:
        entry.delete_instance()
        flash("Entry deleted successfully!", "success")
        return redirect(url_for('show_entries'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email='testuser@example.com',
            password='password'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
