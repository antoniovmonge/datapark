from datetime import datetime
from flask import render_template, url_for, request, current_app, flash, redirect
from flask_login import current_user, login_required
from app.users.forms import EditProfileForm, EmptyForm
from app.models import Post, User
from app.users import bp
from app import db

@bp.route('/user/<username>')
# @login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('users.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('users.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('users/user.html', user=user, posts=posts,
                            next_url=next_url, prev_url=prev_url, form=form)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('users.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html',
                        title='Edit Profile', form=form)

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.home'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('users.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {username}!')
        return redirect(url_for('users.user', username=username))
    else:
        return redirect(url_for('main.home'))

@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.home'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('users.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username} anymore.')
        return redirect(url_for('users.user', username=username))
    else:
        return redirect(url_for('main.home'))

