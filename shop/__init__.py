from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
import os
from flask_msearch import Search
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
#配置sqlite数据库位置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
#配置应用密钥
app.config['SECRET_KEY'] = "diaspfmpoqw1230j12e0bh21"
#配置图片上传位置
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir,'static/images')
#配置图片上传集
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"请您先登陆。"

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes
