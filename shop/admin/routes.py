from shop.admin.forms import RegistrationForm

from flask import render_template,session,request,redirect,url_for,flash

from shop import app, db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import User
from shop.products.models import Addproduct,Brand,Category
from shop.customers.model import CustomerOrder,Register
from shop.products.routes import brands,categories
import os


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'请先登陆','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html',title='admin page',products=products)

@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'请先登陆','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html',title="brand page",brands=brands)

@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'请先登陆','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html',title="category page",categories=categories)

@app.route('/order')
def order():
    if 'email' not in session:
        flash(f'请先登陆','danger')
        return redirect(url_for('login'))
    orders = CustomerOrder.query.order_by(CustomerOrder.id.desc()).all()
    return render_template('admin/order.html',title="order page",orders=orders)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data,email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'欢迎 {form.name.data}, 感谢您的注册','success')
        return redirect(url_for('home'))
    return render_template('admin/register.html',form=form,title="Registeration page")

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            session['email'] = form.email.data
            flash(f'欢迎 {form.email.data} ，您已经登陆。','success')
            #or 后面本来应该是url_for('admin'),但是会报错，故修改之
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('密码错误，请重新尝试。','danger')
    return render_template('admin/login.html',form=form,title="login page")
