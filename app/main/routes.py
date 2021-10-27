from flask import render_template, url_for, request, current_app, flash, redirect
from flask_login import current_user, login_required
from app.main import bp
from app.models import Post


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.home', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.home', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('home.html', posts=posts, title='Home Page',
                            next_url=next_url, prev_url=prev_url)

@bp.route('/feed')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("home.html", title='Feed', posts=posts,
                            next_url=next_url, prev_url=prev_url)

@bp.route('/coming_soon')
def coming_soon():
    return render_template('coming_soon.html', title='Coming soon')