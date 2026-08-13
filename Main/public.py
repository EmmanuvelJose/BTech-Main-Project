from flask import *
from database import *
public=Blueprint('public',__name__)

@public.route('/',methods=['get','post'])
def home():
	session.clear()
	
	return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
	session.clear()
	if 'submit' in request.form:
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'"%(uname,password)
		res=select(q)
		if res:
			session['lid']=res[0]['login_id']

			if res[0]['usertype']=='admin':
				return redirect(url_for('admin.adminhome'))
			
			elif res[0]['usertype']=='radio':
				return redirect(url_for('radio.radiohome'))

			elif res[0]['usertype']=='doctors':
				q="select * from doctors where login_id='%s'"%(session['lid'])
				val=select(q)
				if val:
					session['did']=val[0]['doctor_id']
					return redirect(url_for('doctors.doctors_home'))
		
			# if res[0]['usertype']=='delivery':
			# 	q="select * from deliveryboy where login_id='%s'"%(session['lid'])
			# 	res=select(q)
			# 	print(res)
			# 	session['did']=res[0]['boy_id']
			# 	session['dname']=res[0]['firstname']+" "+res[0]['lastname']
			# 	return redirect(url_for('dboy.dboyhome'))
			
			if res[0]['usertype']=='mshop':
				q="select * from medicalshop where login_id='%s'"%(session['lid'])
				res=select(q)
				print(res)
				session['sid']=res[0]['medicalshop_id']
				session['sname']=res[0]['shopname']
				return redirect(url_for('shop.shophome'))
		else:
			flash("LOGIN FAILED")
	return render_template('login.html')

@public.route('/dboyreg',methods=['get','post'])
def dboyreg():
	data={}
	if 'submit' in request.form:
		print("^^^^^^^^^^^^^^^^^^^^^^^^")
		fname=request.form['fname']
		lname=request.form['lname']
		
		ph=request.form['phone']
		email=request.form['email']
		uname=request.form['uname']
		password=request.form['password']
		q="select * from login where username='%s'"%(uname)
		res=select(q)
		if res:
			flash('THIS USER NAME ALREADY TAKEN BY ANOTHER USER')
			return redirect(url_for('public.dboyreg'))
		else:
			q="insert into login values(NULL,'%s','%s','dboy')"%(uname,password)
			lid=insert(q)
			q="insert into deliveryboy values(NULL,'%s','%s','%s','%s','%s')"%(lid,fname,lname,ph,email)
			insert(q)
			return redirect(url_for('public.dboyreg'))
	return render_template('dboyreg.html',data=data)


@public.route('/doctors_register',methods=['post','get'])
def doctors_register():
	if 'ds' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		pla=request.form['pla']
		phn=request.form['phn']
		mail=request.form['mail']
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="insert into login values(null,'%s','%s','reject')"%(uname,pwd)
		res=insert(q)
		q="insert into doctors values(null,'%s','%s','%s','%s','%s','%s')"%(res,fname,lname,pla,phn,mail)
		insert(q)
	return render_template('doctors_register.html')
