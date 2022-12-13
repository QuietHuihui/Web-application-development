# 网络应用开发实验公开代码
## 学号：202030442397 姓名：王旭晖

## 代码文件简单说明

-run.py 启动应用
-shop
  |-admin管理模块
       |-forms.py表单
       |-models.py数据库model类
       |-routes.py路由
 |-carts购物车模块
       |-carts.py路由
 |-customers顾客模块
       |-forms.py表单
       |-models.py数据库model类
       |-routes.py路由
 |-products商品模块
       |-forms.py表单
       |-models.py数据库model类
       |-routes.py路由
 |-static静态资源
       |-css
       |-js
       |-images商品图片保存位置
 |-templates模板
       |-admin管理员页面
	|-brand.html品牌和品类管理
	|-index.html商品管理
	|-order.html订单详情页
	|-register.html管理员注册页面
	|-login.html管理员登录页面
       |-customer顾客页面
	|-login.html顾客登录页面
	|-register.html顾客注册页面
	|-order.html顾客查看订单页面
       |-products商品页面
	|-addbrand.html添加品牌或者品类
	|-addproduct.html添加商品
	|-carts.html 购物车页面
	|-result.html 搜索结果页面
	|-single_page.html 商品详情页
	|-updatebrand.html 进行品牌和品类的更新
	|-updateproduct.html 进行商品更新的页面
       |-_formhelpers.html 用于渲染表单
       |-_messages.html 用于处理flash()函数弹出的信息
       |-adminbar.html 管理员页面的导航栏
       |-layout.html 引入bootstrap4提供的css和js
       |-navbar.html 顾客页面下的导航栏


       
