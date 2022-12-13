from flask import redirect,render_template,url_for,flash,request,session,current_app
from sqlalchemy import false
from shop import db,app
from shop.products.models import Addproduct
from shop.products.routes import brands,categories
import json

#合并字典
def MagerDicts(dict1,dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1+dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items())+list(dict2.items()))
    return False

@app.route('/addcart',methods=['POST'])
def AddCart():
    try:
        #从request中获取商品信息
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method == "POST":
            #把商品信息存放到字典中
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':float(product.discount),
            'color':colors,'quantity':quantity,'image':product.image_1,'colors':product.colors}}
            #将字典存放到会话控制中
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    session.modified = True
                    for key,item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            
                            item['quantity'] = item['quantity']+1
                    print(session['Shoppingcart'])
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'],DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price'])*int(product['quantity'])
        subtotal-=discount
        grandtotal=float("%.2f"%(subtotal))
    return render_template('products/carts.html',grandtotal=grandtotal,brands=brands(),categories=categories())


@app.route('/updatecart/<int:code>',methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key,item in session['Shoppingcart'].items():
                if int(key)==code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('购物车中的信息已经更新！','success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key,item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key,None)
        return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart',None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)