from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SubmissionForm(FlaskForm):
    album_title = StringField('Album Title', validators=[DataRequired()])
    album_artist = StringField('Album Artist', validators=[DataRequired()])
    user = StringField('Your Name')
    details = TextAreaField('Why did you choose this album?')
    submit = SubmitField('Submit')
