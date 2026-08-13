from flask import *
from database import *
import uuid
from newcnn import *
# preprocess_image
admin=Blueprint('admin',__name__)
 

@admin.route('/adminhome',methods=['get','post'])
def adminhome():
	if not session.get('lid') is None:
		return render_template('adminhome.html')

	else:
		return redirect(url_for('public.login'))




@admin.route('/shopreg',methods=['get','post'])
def shopreg():
	if not session.get('lid') is None:
		data={}
		if 'submit' in request.form:
			print("^^^^^^^^^^^^^^^^^^^^^^^^")
			shopname=request.form['shopname']

			place=request.form['place']
			city=request.form['city']
			
			district=request.form['district']
			ph=request.form['phone']
			email=request.form['email']
			uname=request.form['uname']
			password=request.form['password']
			q="select * from login where username='%s'"%(uname)
			res=select(q)
			if res:
				flash('THIS USER NAME ALREADY TAKEN BY ANOTHER USER')
				return redirect(url_for('admin.shopreg'))
			else:
				q="insert into login values(NULL,'%s','%s','mshop')"%(uname,password)
				lid=insert(q)
				q="insert into medicalshop values(NULL,'%s','%s','%s','%s','%s','%s','%s')"%(lid,shopname,place,city,district,email,ph)
				insert(q)
				flash('REGISTRATION SUCESSFULLY')
				return redirect(url_for('admin.shopreg'))
		q="select * from medicalshop"
		res=select(q)
		if res:
			data['mshop']=res
			print(res)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="delete from medicalshop where medicalshop_id='%s'"%(id)
			delete(q)
			return redirect(url_for('admin.shopreg'))
		if action=='update':
			q="select * from medicalshop where medicalshop_id='%s'"%(id)
			data['updater']=select(q)
		if 'update' in request.form:
			shopname=request.form['shopname']

			place=request.form['place']
			city=request.form['city']
			
			district=request.form['district']
			ph=request.form['phone']
			email=request.form['email']
			q="update medicalshop set shopname='%s',place='%s',city='%s',district='%s',phone='%s',email='%s' where medicalshop_id='%s'"%(shopname,place,city,district,ph,email,id)
			update(q)
			return redirect(url_for('admin.shopreg'))
		return render_template('shopreg.html',data=data)

	else:
		return redirect(url_for('public.login'))


@admin.route('/admin_view_feedback',methods=['get','post'])
def admin_view_feedback():
	data={}
	if not session.get('lid') is None:
		q="SELECT * FROM feedback INNER JOIN users using(user_id)"
		res=select(q)
		data['feedbacks']=res
		print(res)
		
		return render_template('admin_view_feedback.html',data=data)
	else:
		return redirect(url_for('public.login'))



@admin.route('/admin_view_medicines',methods=['get','post'])
def admin_view_medicines():
	data={}
	if not session.get('lid') is None:
		q="select * from medicines inner join type using(type_id)"
		res=select(q)
		data['med']=res
		print(res)
		return render_template('admin_view_medicines.html',data=data)

	else:
		return redirect(url_for('public.login'))


@admin.route('/admin_manage_type',methods=['get','post'])
def admin_manage_type():
	data={}
	if not session.get('lid') is None:
		if 'submit' in request.form:
			typ=request.form['typ']
			q="select * from type where type='%s'"%(typ)
			res=select(q)
			if res:
				flash('THIS TYPE IS ALREADY ADDED')
				return redirect(url_for('admin.admin_manage_type'))
			else:
				q="insert into type values(NULL,'%s')"%(typ)
				lid=insert(q)
				return redirect(url_for('admin.admin_manage_type'))

		q="select * from type"
		res=select(q)
		if res:
			data['type']=res
			print(res)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="delete from type where type_id='%s'"%(id)
			delete(q)
			return redirect(url_for('admin.admin_manage_type'))
		if action=='update':
			q="select * from type where type_id='%s'"%(id)
			data['updater']=select(q)
		if 'update' in request.form:
			typ=request.form['typ']
			q="update type set type='%s' where type_id='%s'"%(typ,id)
			update(q)
			return redirect(url_for('admin.admin_manage_type'))
		return render_template('admin_manage_type.html',data=data)

	else:
		return redirect(url_for('public.login'))


@admin.route('/admin_view_bookings',methods=['get','post'])
def admin_view_bookings():
	data={}
	if not session.get('lid') is None:

		q="SELECT *,`order_details`.`quantity` AS oquantity FROM `order_details` INNER JOIN order_master USING(omaster_id)INNER JOIN users USING(user_id) INNER JOIN products USING(product_id) WHERE `order_master`.`status`='ordered'"
		res=select(q)
		print(res)
		data['orders']=res
		return render_template("admin_view_bookings.html",data=data)
	else:
		return redirect(url_for('public.login'))

@admin.route('/admin_manage_branches',methods=['get','post'])
def admin_manage_branches():
	data={}
	if not session.get('lid') is None:
		if 'submit' in request.form:
			bname=request.form['bname']
			lat=request.form['lat']
			lon=request.form['lon']
			ph=request.form['phone']
			email=request.form['email']
			uname=request.form['uname']
			password=request.form['password']
			q="select * from login where username='%s' and password='%s'"%(uname,password)
			res=select(q)
			if res:
				flash('THIS USER NAME AND PASSWORD ALREADY TAKEN BY ANOTHER USER')
				return redirect(url_for('admin.admin_manage_branches'))
			else:
				q="insert into login values('%s','%s','branch')"%(uname,password)
				lid=insert(q)
				q="select * from branches order by branch_id desc limit 1"
				res=select(q)
				if res:
					prebid=res[0]['branch_id'].split("__")
					print(prebid)
					bid=int(prebid[1])+1
					bid="B__"+str(bid)
					print(bid)
				else:
					bid="B__1"
				q="insert into branches values('%s','%s','%s','%s','%s','%s','%s')"%(bid,uname,bname,lat,lon,ph,email,)
				insert(q)
				return redirect(url_for('admin.admin_manage_branches'))
		q="select * from branches"
		res=select(q)
		if res:
			data['branch']=res
			print(res)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="delete from branches where branch_id='%s'"%(id)
			delete(q)
			return redirect(url_for('admin.admin_manage_branches'))
		if action=='update':
			q="select * from branches where branch_id='%s'"%(id)
			data['updater']=select(q)
		if 'update' in request.form:
			bname=request.form['bname']
			lat=request.form['lat']
			lon=request.form['lon']
			ph=request.form['phone']
			email=request.form['email']
			q="update branches set branch_name='%s',latitude='%s',longitude='%s',phone='%s',email='%s' where branch_id='%s'"%(bname,lat,lon,ph,email,id)
			update(q)
			return redirect(url_for('admin.admin_manage_branches'))
		return render_template('admin_manage_branches.html',data=data)

	else:
		return redirect(url_for('public.login'))





@admin.route('/admin_review_andrate',methods=['get','post'])
def admin_review_andrate():
	data={}
	if not session.get('lid') is None:
		q="select * from review_rating inner join branches using(branch_id) inner join customers using(customer_id)"
		res=select(q)
		print(res)
		data['rating']=res
		print(res)
		# q="select * from feedback inner join branches using(branch_id) where admin_id='%s'"%(cid)	
		# res=select(q)
		# data['fb']=res
		# print(res)
		return render_template('admin_review_andrate.html',data=data)
	else:
		return redirect(url_for('public.login'))


@admin.route('/admin_view_complaints',methods=['get','post'])
def admin_view_complaints():
	data={}
	if not session.get('lid') is None:
		q="SELECT * FROM user INNER JOIN complaint USING(user_id)"
		res=select(q)
		data['complaints']=res
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
			if action=="update":
				q="select * from complaint inner join user using(user_id) where complaint_id='%s' "%(id)
				res=select(q)
				data['updater']=res
		if 'update' in request.form:
			reply=request.form['reply']
			q="update complaint set reply='%s' where complaint_id='%s'"%(reply,id)
			update(q)
			return redirect(url_for('admin.admin_view_complaints'))
		return render_template('admin_view_complaints.html',data=data)


	else:
		return redirect(url_for('public.login'))


@admin.route('/admin_view_docterp',methods=['get','post'])
def admin_view_docterp():
	data={}
	if not session.get('lid') is None:

		q="SELECT * FROM `users` INNER JOIN `appoinments` ON `users`.`user_id`=`appoinments`.`user_id` INNER JOIN `schedule` ON `schedule`.`schedule_id`=`appoinments`.`schedule_id` INNER JOIN `doctors` ON `doctors`.`doctor_id`=`schedule`.`doctor_id`"
		print(q,"ttttttttttttttttttttttttttttttttt")
		res=select(q)
		print(res)
		data['orders']=res

		return render_template("admin_view_docterp.html",data=data)
	else:
		return redirect(url_for('public.login'))



@admin.route('/admin_view_doctors',methods=['get','post'])
def admin_view_doctors():
	data={}
	if not session.get('lid') is None:

		q="SELECT * FROM `doctors` inner join login using(login_id)"
		res=select(q)
		print(res)
		data['doct']=res

		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None

		if action=="accept":
			q="update login set usertype='doctors' where login_id='%s'"%(id)
			update(q)
			return redirect(url_for('admin.admin_view_doctors'))

		if action=="reject":
			q="update login set usertype='rejected' where login_id='%s'"%(id)
			update(q)
			return redirect(url_for('admin.admin_view_doctors'))
		return render_template("admin_view_doctors.html",data=data)
	else:
		return redirect(url_for('public.login'))


@admin.route('/admin_predict_output',methods=['get','post'])
def admin_predict_output():
	data={}
	if not session.get('lid') is None:

		q="SELECT * FROM `appoinments` INNER JOIN `upload_prediction_image` USING(`appoinment_id`) INNER JOIN `doctors` USING(`doctor_id`) INNER JOIN `users` ON `users`.`user_id`=`upload_prediction_image`.`user_id` ORDER BY `pre_img_id` DESC"
		res=select(q)
		print(res)
		data['view']=res

		# if 'action' in request.args:
		# 	action=request.args['action']
		# 	id=request.args['id']
		# else:
		# 	action=None

		# if action=="accept":
		# 	q="update login set usertype='doctors' where login_id='%s'"%(id)
		# 	update(q)
		# 	return redirect(url_for('admin.admin_view_doctors'))

		# if action=="reject":
		# 	q="update login set usertype='rejected' where login_id='%s'"%(id)
		# 	update(q)
		# 	return redirect(url_for('admin.admin_view_doctors'))
		return render_template("admin_predict_output.html",data=data)
	else:
		return redirect(url_for('public.login'))



from keras import backend as K
@admin.route('/admin_predict_user_prediction',methods=['post','get'])
def admin_predict_user_prediction():
	K.clear_session()
	data={}
	pre_img_id=request.args['pre_img_id']
	uid=request.args['uid']
	if 'submit' in request.form:
		upload=request.files['upload']
		path="static/images/"+str(uuid.uuid4())+ ".jpg"
		upload.save(path)
		values=preprocess_image(path)
		q="INSERT `images` VALUES(NULL,'%s','%s','%s','%s')"%(uid,path,values,pre_img_id)
		print(q)
		res=insert(q)
		
	q="select * from images  where pre_img_id='%s'"%(pre_img_id)
	data['view']=select(q)
	return render_template('admin_predict_user_prediction.html',data=data)




@admin.route('/admin_schedule',methods=['post','get'])
def admin_schedule():
	K.clear_session()
	data={}
	id=request.args['id']
	if 'submit' in request.form:
		stime=request.form['stime']
		etime=request.form['etime']
		da=request.form['da']
		q="INSERT `schedule` VALUES(NULL,'%s','%s','%s','%s','available')"%(id,da,stime,etime)
		print(q,"iiiiiiiiiiiiiiiiiiii")
		print(q)
		insert(q)
		
	q="select * from SCHEDULE  where doctor_id='%s'"%(id)
	data['view']=select(q)
	return render_template('admin_schedule.html',data=data)
