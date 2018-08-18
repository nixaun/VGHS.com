from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Course, Teacher, Clas
from flaskapp.intra.forms import CourseForm, TeacherForm, ClassForm, UpdateCourseForm, UpdateTeacherForm, UpdateClassForm
from flaskapp.users.utils import save_picture

intra = Blueprint('intra', __name__)

#__________________intranet routes___________________________________

@intra.route("/intranet")
def intranet():
    return render_template('intra/intranet.html', title='Intranet')

@intra.route("/intranet/courses")
def intranet_courses():
    page = request.args.get('page', 1, type=int)
    courses = Course.query.paginate(page=page, per_page=5)
    return render_template('intra/intranet_courses.html', title='Courses', courses=courses)

@intra.route("/intranet/teachers")
def intranet_teachers():
    page = request.args.get('page', 1, type=int)
    teachers = Teacher.query.paginate(page=page, per_page=5)
    return render_template('intra/intranet_teachers.html', title='Teachers', teachers=teachers)

@intra.route("/intranet/classes")
def intranet_classes():
    page = request.args.get('page', 1, type=int)
    classes = Clas.query.paginate(page=page, per_page=5)
    return render_template('intra/intranet_classes.html', title='Classes', classes=classes)

#______________________courses routes_____________________________________

@intra.route("/course/new", methods=['GET', 'POST'])
@login_required
def new_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data, author=current_user)
        db.session.add(course)
        db.session.commit()
        flash('Your course has been added!', 'success')
        return redirect(url_for('intra.intranet_courses'))
    return render_template('intra/create_course.html', title='New course', form=form, legend='New course')

@intra.route("/course/<int:course_id>")
def course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('intra/intranet_course.html', course=course)

@intra.route("/course/<int:course_id>/update", methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = UpdateCourseForm()
    if form.validate_on_submit():
        course.name = form.name.data
        course.description = form.description.data
        db.session.commit()
        flash('The course has been updated!', 'success')
        return redirect(url_for('intra.course', course_id=course.id))
    elif request.method == 'GET':
        form.name.data = course.name
        form.description.data = course.description
    return render_template('intra/create_course.html', title='Update course', form=form, legend='Update course')

@intra.route("/course/<int:course_id>/delete", methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('The course has been deleted!', 'success')
    return redirect(url_for('intra.intranet_courses'))



#__________________________teachers_________________________________________

@intra.route("/teacher/new", methods=['GET', 'POST'])
@login_required
def new_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        teacher = Teacher(name=form.name.data, first_name=form.first_name.data, email=form.email.data, author=current_user)
        db.session.add(teacher)
        db.session.commit()
        flash('Your teacher has been added!', 'success')
        return redirect(url_for('intra.intranet_teachers'))
    return render_template('intra/create_teacher.html', title='New teacher', form=form, legend='New teacher')

@intra.route("/teacher/<int:teacher_id>")
def teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    return render_template('intra/intranet_teacher.html', teacher=teacher)

@intra.route("/teacher/<int:teacher_id>/update", methods=['GET', 'POST'])
@login_required
def update_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    form = UpdateTeacherForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            teacher.image_file = picture_file
        teacher.name = form.name.data
        teacher.first_name = form.first_name.data
        teacher.email = form.email.data
        db.session.commit()
        flash('This teacher has been updated!', 'success')
        return redirect(url_for('intra.teacher', teacher_id=teacher.id))
    elif request.method == 'GET':
        form.name.data = teacher.name
        form.first_name.data = teacher.first_name
        form.email.data = teacher.email
    image_file = url_for('static', filename='profile_pics/' + teacher.image_file)
    return render_template('intra/update_teacher.html', title='Update teacher', image_file=image_file, form=form, legend='Update teacher')

@intra.route("/teacher/<int:teacher_id>/delete", methods=['POST'])
@login_required
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    flash('The teacher has been deleted!', 'success')
    return redirect(url_for('intra.intranet_teachers'))

#__________________________classes_________________________________________

@intra.route("/class/new", methods=['GET', 'POST'])
@login_required
def new_class():
    form = ClassForm()
    if form.validate_on_submit():
        clas = Clas(name=form.name.data, class_code=form.class_code.data, course=form.course.data, teacher=form.teacher.data, author=current_user)
        db.session.add(clas)
        db.session.commit()
        flash('Your class has been added!', 'success')
        return redirect(url_for('intra.intranet_classes'))
    return render_template('intra/create_class.html', title='New class', form=form, legend='New class')

@intra.route("/class/<int:clas_id>")
def clas(clas_id):
    clas = Clas.query.get_or_404(clas_id)
    return render_template('intra/intranet_class.html', clas=clas)

@intra.route("/class/<int:clas_id>/update", methods=['GET', 'POST'])
@login_required
def update_class(clas_id):
    clas = Clas.query.get_or_404(clas_id)
    form = UpdateClassForm()
    if form.validate_on_submit():
        clas.name = form.name.data
        clas.class_code = form.class_code.data
        clas.course = form.course.data
        clas.teacher = form.teacher.data
        db.session.commit()
        flash('The clas has been updated!', 'success')
        return redirect(url_for('intra.clas', clas_id=clas.id))
    elif request.method == 'GET':
        form.name.data = clas.name
        form.class_code.data = clas.class_code
        form.course.data = clas.course
        form.teacher.data = clas.teacher
    return render_template('intra/create_class.html', title='Update class', form=form, legend='Update class')

@intra.route("/class/<int:clas_id>/delete", methods=['POST'])
@login_required
def delete_class(clas_id):
    clas = Clas.query.get_or_404(clas_id)
    db.session.delete(clas)
    db.session.commit()
    flash('The class has been deleted!', 'success')
    return redirect(url_for('intra.intranet_classes'))
