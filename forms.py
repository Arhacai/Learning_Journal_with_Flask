from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField,
                     DateField, IntegerField)
from wtforms.validators import (DataRequired, ValidationError, Email)
from models import Entry


def title_exists(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError("Entry with that title already exists.")


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class AddEntry(Form):
    title = StringField(
        'Title',
        validators=[DataRequired(), title_exists]
    )
    date = DateField(
        'Date(YYYY-MM-DD)',
        validators=[DataRequired()]
    )
    time = IntegerField(
        'Time Spent (minutes)',
        validators=[DataRequired()]
    )
    learned = TextAreaField(
        "What You've Learned",
        validators=[DataRequired()]
    )
    resources = TextAreaField(
        'Resources to Remember',
        validators=[DataRequired()]
    )
    tags = StringField('Tags (separated by a space)')


class EditEntry(Form):
    title = StringField(
        'Title',
        validators=[DataRequired(), title_exists]
    )
    date = DateField(
        'Date(YYYY-MM-DD)',
        validators=[DataRequired()]
    )
    time = IntegerField(
        'Time Spent (minutes)',
        validators=[DataRequired()]
    )
    learned = TextAreaField(
        "What You've Learned",
        validators=[DataRequired()]
    )
    resources = TextAreaField(
        'Resources to Remember',
        validators=[DataRequired()]
    )
    tags = StringField('Tags (separated by a space)')
