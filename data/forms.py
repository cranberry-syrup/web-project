from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почтовый адрес email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
    
class RegistrationForm(FlaskForm):
    email = EmailField('Почтовый адрес email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя или название компании', validators=[DataRequired()])
    type = SelectField('Тип учётной записи', choices=[('employee', 'Работник'), ('employer', 'Работодатель')])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class JobForm(FlaskForm):
    title = StringField('Наименование', validators=[DataRequired()])
    salary = IntegerField('Размер заработной платы', validators=[DataRequired()])
    about = TextAreaField("О вакансии")
    is_public = BooleanField("Выложить в открытый доступ")
    submit = SubmitField('Применить')
