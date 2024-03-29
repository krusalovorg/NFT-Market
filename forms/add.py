from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):

    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    #category = StringField('Категория', validators=[DataRequired()])
    category = SelectField(choices=[('Выберети категорию', '')])
    cost = IntegerField('Цена (без пробелов)', validators=[DataRequired()])
    new_category = StringField('Новая Категория')
    #image = FileField('Картинка', validators=[DataRequired()])
    createAsMarket = BooleanField('Создать от имени NFTMarket', default=False)

    submit = SubmitField('Добавить')

    # <p>
    #     {{form3.image.label }}<br>
    #     {{form3.image(class="form-control") }}<br>
    #     {% for error in form3.image.errors %}
    # <p content="alert alert-danger" role="alert">
    #     {{ error }}
    # </p>
    # {% endfor %}
