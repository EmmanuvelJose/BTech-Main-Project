from flask import *
from public import public
from admin import admin
from shop import shop
from dboy import dboy
from doctors import doctors
from api import api
from radio import radio



app=Flask(__name__)
app.secret_key="hello"
app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(shop,url_prefix='/shop')
app.register_blueprint(dboy,url_prefix='/dboy')
app.register_blueprint(doctors,url_prefix='/doctors')
app.register_blueprint(api,url_prefix='/api')
app.register_blueprint(radio,url_prefix='/radio')


app.run(debug=True,port=5099,host="0.0.0.0")
# app.run(debug=True,port=5058,host="192.168.1.20")
