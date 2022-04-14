from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RedactForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()], default='nick')
    description = StringField('Описание', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()], default='name')
    surname = StringField('Фамилия', validators=[DataRequired()], default='sur')
    submit = SubmitField('Применить')



