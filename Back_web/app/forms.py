from flask_wtf import FlaskForm
from wtforms import PasswordField,validators,StringField,IntegerField,FloatField
from wtforms.validators import DataRequired,Required

class LoginForm(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    password=PasswordField('password',[validators.DataRequired()])

class SearchForm(FlaskForm):
    bookinfo=StringField('bookname',validators=[DataRequired()])

class Book_add(FlaskForm):
    id=StringField('id',validators=[DataRequired()])
    name = StringField('name')
    style_num = StringField('style_num',validators=[DataRequired()])
    author = StringField('author',validators=[DataRequired()])
    count = StringField('count',validators=[DataRequired()])
    available_count = StringField('available_count',validators=[DataRequired()])
    price = StringField('price')
    press = StringField('press', validators=[DataRequired()])
    # publish_date = StringField('publish_date', validators=[DataRequired()])
    summary=StringField('summary', validators=[DataRequired()])
    temperture = StringField('temperture', validators=[DataRequired()])
    humidity = StringField('humidity', validators=[DataRequired()])
    url=StringField('url',validators=[DataRequired()])


class Book_delete(FlaskForm):
    id = StringField('id', validators=[DataRequired()])

class Book_alter_select(FlaskForm):
    id=StringField('id',validators=[DataRequired()])

class Book_alter(FlaskForm):
    id=StringField('id')
    name = StringField('name',validators=[DataRequired()])
    style_num = StringField('style_num',validators=[DataRequired()])
    author = StringField('author',validators=[DataRequired()])
    count = StringField('count',validators=[DataRequired()])
    available_count = StringField('available_count',validators=[DataRequired()])
    price = StringField('price',validators=[DataRequired()])
    press=StringField('press',validators=[DataRequired()])
    summary = StringField('summary', validators=[DataRequired()])
    temperture= StringField('summary', validators=[DataRequired()])
    humidity = StringField('summary', validators=[DataRequired()])
    url = StringField('url', validators=[DataRequired()])
class Reader_add(FlaskForm):
    no=StringField('no',validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    gender = StringField('gender', validators=[DataRequired()])
    kind = StringField('kind', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    grade=StringField('grade', validators=[DataRequired()])
    department=StringField('department', validators=[DataRequired()])
    longtitude=StringField('longtitude',validators=[DataRequired()])
    latitude = StringField('latitude', validators=[DataRequired()])
    IDcard=StringField('IDcard',validators=[DataRequired()])

class Reader_delete(FlaskForm):
    no = StringField('no', validators=[DataRequired()])

class Reader_alter_select(FlaskForm):
    no=StringField('readerno',validators=[DataRequired()])

class Reader_select(FlaskForm):
    no=StringField('readerno',validators=[DataRequired()])

class Group_add(FlaskForm):
    id=StringField('id',validators=[DataRequired()])
    room = StringField('room',validators=[DataRequired()])
    id1 = StringField('id1', validators=[DataRequired()])
    id2 = StringField('id2', validators=[DataRequired()])
    id3 = StringField('id3', validators=[DataRequired()])
    id4 = StringField('id4', validators=[DataRequired()])
    id5 = StringField('id5', validators=[DataRequired()])
    id6 = StringField('id6', validators=[DataRequired()])