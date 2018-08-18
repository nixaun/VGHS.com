from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError
from flaskapp.models import Course, Teacher, Clas

class CourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_name(self, name):
        name = Course.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That course already exists. Please check the courses section on the intranet for it.')

class UpdateCourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_name(self, name):
        name = Course.query.filter_by(name=name.data).first()
        if name.data != course.name:
            if name:
                raise ValidationError('That course already exists. Please check the courses section on the intranet for it.')


class TeacherForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

    def validate_email(self, email):
        teacher = Teacher.query.filter_by(email=email.data).first()
        if teacher:
            raise ValidationError('That email is already taken. Please check the classes section on the intranet for it.')

class UpdateTeacherForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

    def validate_email(self, email):
        teacher = Teacher.query.filter_by(email=email.data).first()
        if email.data != teacher.email:
            if teacher:
                raise ValidationError('That email is already taken. Please check the classes section on the intranet for it.')

class ClassForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    class_code = StringField('Class code', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    teacher = StringField('Teacher', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_name(self, name):
        clas = Clas.query.filter_by(name=name.data).first()
        if clas:
            raise ValidationError('That class already exists. Please check the classes section on the intranet for it.')

    def validate_class_code(self, class_code):
        clas = Clas.query.filter_by(class_code=class_code.data).first()
        if clas:
            raise ValidationError('That classcode is already taken. Please choose a different one.')

class UpdateClassForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    class_code = StringField('Class code', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    teacher = StringField('Teacher', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_name(self, name):
        clas = Clas.query.filter_by(name=name.data).first()
        if name.data != clas.name:
            if clas:
                raise ValidationError('That class already exists. Please check the classes section on the intranet for it.')

    def validate_class_code(self, class_code):
        clas = Clas.query.filter_by(class_code=class_code.data).first()
        if class_code.data != clas.class_code:
            if clas:
                raise ValidationError('That classcode is already taken. Please choose a different one.')
