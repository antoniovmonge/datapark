from datetime import datetime
from flask import render_template, url_for, request, current_app, flash, redirect
from flask_login import current_user, login_required
from app.messages.forms import MessageForm
from app.models import User, Message
from app.messages import bp
from app import db

@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                        body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('users.user', username=recipient))
    return render_template('messages/send_message.html', title='Send Message',
                            form=form, recipient=recipient, legend='Send Message')

@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages/messages.html', messages=messages.items,
                            next_url=next_url, prev_url=prev_url, title='Messages')
