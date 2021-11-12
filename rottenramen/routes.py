from flask import render_template, redirect, url_for, request, flash
from rottenramen import app, database, bcrypt
from rottenramen.forms import FormLogin, FormCreatAccount, FormEditProfile, FormCreatPost
from rottenramen.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'button_submit_login' in request.form:
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_data.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login. E-mail ou Senha Incorretos', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route('/cadastro', methods=['GET', 'POST'])
def register():
    form_creataccount = FormCreatAccount()
    if form_creataccount.validate_on_submit() and 'button_submit_creataccount' in request.form:
        password_crypt = bcrypt.generate_password_hash(form_creataccount.password.data)
        user = User(username=form_creataccount.username.data, email=form_creataccount.email.data, password=password_crypt)
        database.session.add(user)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_creataccount.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('register.html', form_creataccount=form_creataccount)


@app.route('/sair')
@login_required
def logout():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def creat_post():
    form = FormCreatPost()
    posts = Post.query.order_by(Post.id.desc())
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Comentário Feito com Sucesso', 'alert-success')
    return render_template('post.html', form=form, posts=posts)


def save_image(image):
    code = secrets.token_hex(8)
    name, extension = os.path.splitext(image.filename)
    file_name = name + code + extension
    full_path = os.path.join(app.root_path, 'static/profile_photos', file_name)
    size = (400, 400)
    reduced_image = Image.open(image)
    reduced_image.thumbnail(size)
    reduced_image.save(full_path)
    return file_name


@app.route('/perfil')
@login_required
def profile():
    profile_photo = url_for('static', filename=f'profile_photos/{current_user.profile_photo}')
    return render_template('profile.html', profile_photo=profile_photo)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = FormEditProfile()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.profile_photo.data:
            image_name = save_image(form.profile_photo.data)
            current_user.profile_photo = image_name
        database.session.commit()
        flash('Perfil atualizado com Sucesso.', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_photo = url_for('static', filename=f'profile_photos/{current_user.profile_photo}')
    return render_template('editprofile.html', profile_photo=profile_photo, form=form)

