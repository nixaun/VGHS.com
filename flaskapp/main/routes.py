from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flaskapp.models import Course, Teacher, Contact
from flaskapp.main.forms import ContactForm
from flaskapp import db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/offer")
def offer():
    page = request.args.get('page', 1, type=int)
    courses = Course.query.paginate(page=page, per_page=5)
    return render_template('offer.html', title='Our offer', courses=courses)

@main.route("/who")
def who():
    page = request.args.get('page', 1, type=int)
    teachers = Teacher.query.paginate(page=page, per_page=5)
    return render_template('who.html', title='Who\'s who?', teachers=teachers)

@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, subject=form.subject.data, email=form.email.data, content=form.content.data)
        db.session.add(contact)
        db.session.commit()
        flash('Your request has been sent to us. We will awnser as swiftly as possible.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', title='Contact', form=form)
