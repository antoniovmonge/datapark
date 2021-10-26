from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = PageDownField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
