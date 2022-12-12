from flask import redirect,render_template,url_for,flash,request,session,current_app
from shop import db,app,photos,search
from .models import Addproduct, Brand,Category
from .forms import Addproducts
from shop.products.models import Addproduct
import secrets,os

def brands():
    #这样处理是为了不显示没有商品的品牌
    brands = Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    return brands

def categories():
    #这样处理是为了不显示没有商品的品类
    categories = Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return categories

@app.route('/')
def home():
    page = request.args.get('page',1,type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0 ).order_by(Addproduct.id.desc()).paginate(page=page,per_page=12)
    return render_template("products/index.html",products=products,brands=brands(),categories=categories())

@app.route('/result')
def result():
    searchword = request.args.get('q')
    #limit表示搜索出来的最多记录条数
    products = Addproduct.query.msearch(searchword,fields=['name','desc'],limit=36)
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product=Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product,brands=brands(),categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    get_b = Brand.query.filter_by(id=id).first_or_404()
    page = request.args.get('page',1,type=int)
    brand = Addproduct.query.filter_by(brand=get_b).paginate(page=page,per_page=12)
    return render_template("products/index.html",brand=brand,brands=brands(),categories=categories(),get_b=get_b)

@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1,type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page,per_page=12)
    return render_template("products/index.html",get_cat_prod=get_cat_prod,categories=categories(),brands=brands(),get_cat=get_cat)

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'请先登陆','danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'品牌 {getbrand} 已经添加到了您的数据库中。','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'请先登陆。','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method=="POST":
        updatebrand.name = brand
        flash(f'品牌信息已经更新。','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html',title='Update brand page',updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>',methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'品牌 {brand.name} 已经从您的数据库中删除。','success')
        return redirect(url_for('admin'))
    flash(f'品牌 {brand.name} 不能被删除。','warning')
    return redirect(url_for('admin'))

@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'请先登陆。','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method=="POST":
        updatecat.name = category
        flash(f'品类信息已经更新。','success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html',title='Update brand page',updatecat=updatecat)


@app.route('/deletecategory/<int:id>',methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'品类 {category.name} 已经从您的数据库中删除。','success')
        return redirect(url_for('admin'))
    flash(f'品类 {category.name} 不能被删除。','warning')
    return redirect(url_for('admin'))

@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'请先登陆','danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getcat = request.form.get('category')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'类别 {getcat} 已经添加到了您的数据库中。','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')

@app.route('/addproduct',methods=['POST','GET'])
def addproduct():
    if 'email' not in session:
        flash(f'请先登陆','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)

    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
        addpro = Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,brand_id=brand,
        category_id=category,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        flash(f'成功添加商品 {name} 到数据库。','success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html',title="add product page",
    form=form,brands=brands,categories=categories)

@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id=brand
        product.colors = form.colors.data
        product.desc = form.discription.data
        if request.files.get('image_1'):
            try:
                #删除掉原先的图片
                print(os.path.join(current_app.root_path,"static/images/"+product.image_1))
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_1))
                #保存新的图片
                product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
            except:
                #如果原先没有图片，直接保存新图片
                product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
        if request.files.get('image_2'):
            try:
                #删除掉原先的图片
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_2))
                #保存新的图片
                product.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
            except:
                #如果原先没有图片，直接保存新图片
                product.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        if request.files.get('image_3'):
            try:
                #删除掉原先的图片
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_3))
                #保存新的图片
                product.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
            except:
                #如果原先没有图片，直接保存新图片
                product.image_3= photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
        db.session.commit()
        flash('你的产品信息已经更新。','success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.discription.data = product.desc
    return render_template('products/updateproduct.html',form=form,brands=brands,categories=categories,product=product)

@app.route('/deleteproduct/<int:id>',methods=["POST"])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_1))
            os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_2))
            os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'商品 {product.name} 已从您的数据库中删除。','success')
        return redirect(url_for('admin'))
    flash(f'未能删除商品。','danger')
    return redirect(url_for('admin'))