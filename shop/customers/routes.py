from flask import redirect,render_template,url_for,flash,request,session,current_app
from flask_login import login_required,current_user,logout_user,login_user
from shop import db,app,photos,search,bcrypt,login_manager
from .forms import CustomerRegisterForm,CustomerLoginForm
from .model import Register,CustomerOrder
from shop.products.routes import brands,categories
import secrets,os

@app.route('/customer/register',methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data,username=form.username.data,email=form.email.data,
        password=hash_password,country=form.country.data,state=form.state.data,city=form.city.data,
        address=form.address.data,zipcode=form.zipcode.data,contact=form.contact.data)
        db.session.add(register)
        flash(f'欢迎 {form.name.data} , 感谢您的注册。','success')
        db.session.commit()
        return redirect(url_for('customer/login'))
    return render_template('customer/register.html',form=form,brands=brands(),categories=categories())

@app.route('/customer/login',methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('You are login now!','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('电子邮件地址或密码错误，请重试。','danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html',form=form,brands=brands(),categories=categories())

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('您的订单已经成功发送给商家。','success')
            return redirect(url_for('orders',invoice=invoice))

        except Exception as e:
            print(e)
            flash('提交订单时发生错误，未成功提交订单。','danger')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key,product in orders.orders.items():
            discount = (product['discount']/100)*float(product['price'])
            subTotal += float(product['price'])*int(product['quantity'])
            subTotal -= discount
            grandTotal = float("%.2f"%(1.0*subTotal))
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html',invoice=invoice,subTotal=subTotal,grandTotal=grandTotal,
    customer=customer,orders=orders,brands=brands(),categories=categories())
