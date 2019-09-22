from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, \
    login_required, current_user

from project.models import User, Groups, Wallet
# from project.email import send_email
from project import db, bcrypt, robohash
from .forms import LoginForm, RegisterForm, ChangePasswordForm, GroupsForm, GroupidFrom, WalletForm
from project import app


################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################
@user_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = User.query.filter_by(login=current_user.login).first()
    if user:
        img = user.robohash_img
    else:
        img = ""

    form_id = GroupidFrom(request.form)
    try:
        if request.form['submit_button'] == 'Stop':
            id = form_id.ids.data
            group_ids = Groups.query.filter_by(id=id).first()
            group_ids.status = "Stopped"
            db.session.commit()
        if request.form['submit_button'] == 'Active':
            id = form_id.ids.data
            group_ids = Groups.query.filter_by(id=id).first()
            group_ids.status = "Active"
            db.session.commit()
        if request.form['submit_button'] == 'Delete':
            id = form_id.ids.data
            groups_id = Groups.query.filter_by(id=id).first()
            db.session.delete(groups_id)
            db.session.commit()
    except:
        pass

    form = GroupsForm(request.form)
    if form.validate_on_submit():
        proxy = request.form.getlist('hello')
        if len(proxy) > 0 and proxy[0] == "on":
            print(form.password_proxy)

            group = Groups(
                cookie=form.cookie.data,
                Group_id=form.Group_id.data,
                amount=form.amount.data,
                status="Active",
                user_id=current_user.id,
                login_proxy=form.login_proxy.data,
                password_proxy=form.password_proxy.data,
                ip_proxy=form.ip_proxy.data,
                port=form.port.data
            )
            db.session.add(group)
            db.session.commit()

            flash('Group added', 'success')
        else:

            group = Groups(
                cookie=form.cookie.data,
                Group_id=form.Group_id.data,
                amount=form.amount.data,
                status="Active",
                user_id=current_user.id,
                login_proxy=0,
                password_proxy="empty",
                ip_proxy=0,
                port=0
            )

            db.session.add(group)
            db.session.commit()

            flash('Group added', 'success')
        return redirect('/dashboard')
    else:
        print("shit with group")

    groups_ac = Groups.query.filter_by(user_id=current_user.id, status="Active").all()
    groups_st = Groups.query.filter_by(user_id=current_user.id, status="Stopped").all()
    groups_so = Groups.query.filter_by(user_id=current_user.id, status="Sold").all()
    if groups_ac:
        gros_ac = groups_ac
        len_gros = len(groups_ac)
    else:
        gros_ac = []
        len_gros = 0
    if groups_st:
        gros_st = groups_st
        len_gros_st = len(groups_st)
    else:
        gros_st = []
        len_gros_st = 0
    if groups_so:
        gros_so = groups_so
        len_gros_so = len(groups_so)
    else:
        gros_so = []
        len_gros_so = 0


    return render_template('dashboard.html', img=img, form3=form, gros=gros_ac, len_gros=len_gros,
                           gros_st=gros_st, len_gros_st=len_gros_st,
                           gros_so=gros_so, len_gros_so=len_gros_so, form_id=form_id)


@user_blueprint.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    user = User.query.filter_by(login=current_user.login).first()
    if user:
        img = user.robohash_img
    else:
        img = ""
    form = WalletForm(request.form)
    if form.validate_on_submit():

        wallet = Wallet(
            wallet=form.wallet.data,
            sum=form.sum.data,
            user_id=current_user.id,
            status="Pending"
        )

        db.session.add(wallet)
        db.session.commit()

        flash('Group added', 'success')
        return redirect('/withdraw')
    else:
        print("shit with wallet")
    groups_ac = Wallet.query.filter_by(user_id=current_user.id).all()

    if groups_ac:
        gros_ac = groups_ac
        lens =len(groups_ac)
    else:
        gros_ac = []
        lens = 0

    return render_template('withdraw.html', img=img, form=form, wall = groups_ac, lens=lens)


@user_blueprint.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            login=form.login.data,
            email=form.email.data,
            password=form.password.data
        )
        print(user)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('You registered and are now logged in. Welcome!', 'success')
        return redirect('/dashboard')
    else:
        print("shit")
    form2 = LoginForm(request.form)
    print("login")
    if form2.validate_on_submit():
        print("good")
        user = User.query.filter_by(login=form2.login.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('index.html', form2=form2, form=form)

    return render_template('index.html', form=form, form2=form2)




@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect('/')




@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.profile'))
    return render_template('dashboard.html', form=form)