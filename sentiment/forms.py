from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

class AudioForm(FlaskForm):
    audio_file = FileField('Upload Audio File')
    submit=SubmitField('Upload')


