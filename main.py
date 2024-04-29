import os

from flask import Flask, render_template, url_for, redirect, request, abort
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from data import db_session
from data.forms import RegistrationForm, LoginForm, JobForm
from data.users import User
from data.jobs import Job

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        jobs = db_sess.query(Job).filter((Job.user == current_user) | (Job.is_public != False))
    else:   
        jobs = db_sess.query(Job).filter(Job.is_public != False)
    return render_template('home.html', title='КосмоРаб', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            type=form.type.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/home")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job',  methods=['GET', 'POST'])
@login_required
def add_job():
    if current_user.type == 'employer':
        form = JobForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            job = Job()
            job.title = form.title.data
            job.salary = form.salary.data
            job.about = form.about.data
            job.is_public = form.is_public.data
            current_user.jobs.append(job)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/home')
        return render_template('edit_job.html', title='Добавление вакансии', 
                            form=form)
    else:
        abort(404)
        

@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Job).filter(Job.id == id,
                                          Job.user == current_user
                                          ).first()
        if job:
            form.title.data = job.title
            form.about.data = job.about
            form.salary.data = job.salary
            form.is_public.data = job.is_public
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Job).filter(Job.id == id,
                                          Job.user == current_user
                                          ).first()
        if job:
            job.title = form.title.data
            job.about = form.about.data
            job.salary = form.salary.data
            job.is_public = form.is_public.data
            db_sess.commit()
            return redirect('/home')
        else:
            abort(404)
    return render_template('edit_job.html',
                           title='Редактирование вакансии',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == id,
                                      Job.user == current_user
                                      ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/home')


def main():
    db_session.global_init("db/data.db")
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
