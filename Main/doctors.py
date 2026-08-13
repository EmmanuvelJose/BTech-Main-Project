from flask import *
from database import *
import uuid
from newcnn import *
# preprocess_image

doctors=Blueprint('doctors',__name__)


@doctors.route('/doctors_home')
def doctors_home():
	return render_template('doctors_home.html')


@doctors.route('/doctors_view_appointment')
def doctors_view_appointment():
	data={}
	did=session['did']
	# q="select * from appoinments inner join  doctors using(doctor_id) inner join users using(user_id) where doctor_id='%s'" %(did)
	q="SELECT * FROM appoinments INNER JOIN `schedule` USING(`schedule_id`) INNER JOIN   doctors USING(doctor_id) INNER JOIN users USING(user_id)where doctor_id='%s'" %(did)
	data['view']=select(q)
	return render_template('doctors_view_appointment.html',data=data)


@doctors.route('/doctors_view_customers')
def doctors_view_customers():
	data={}
	uid=request.args['uid']
 
	q="select * from users where user_id='%s'"%(uid)
	data['view']=select(q)
	return render_template('doctors_view_customers.html',data=data)


@doctors.route('/doctors_upload_prescription',methods=['post','get'])
def doctors_upload_prescription():
	data={}
	appoinment_id=request.args['appoinment_id']
	if 'submit' in request.form:
		upload=request.files['upload']
		path="static/images/"+str(uuid.uuid4())+upload.filename
		upload.save(path)
		# amt=request.form['amt']
		# da=request.form['da']
		uid=request.args['uid']
		# med=request.form['med']
		q="insert into prescription values(null,'%s','%s',curdate(),'pending')"%(appoinment_id,path)
		insert(q)
	q="select * from prescription inner join appoinments using(appoinment_id) where appoinment_id='%s'"%(appoinment_id)
	res=select(q)

	# q="select * from uploadprescription inner join medicalshop using(medicalshop_id)"
	# data['view']=select(q)
 

	q="select * from medicalshop"
	data['v']=select(q)

	if 'action' in request.args:
		action=request.args['action']
		uid=request.args['uid']
	else:
		action=None

	if action=='update':
		q="select * from prescription where pres_id='%s'"%(uid)
		data['up']=select(q)
		# q="select * from prescription where user_id='%s'"%(uid)
		# data['up']=select(q)
  

	if 'update' in request.form:
		# med=request.form['med']
		upload=request.files['upload']
		path="static/images/"+str(uuid.uuid4())+upload.filename
		upload.save(path)
		# amt=request.form['amt']
		da=request.form['da']
		q="update uploadprescription set uploadfile='%s',total_amount='%s',date='%s' where user_id='%s'"%(path,da,uid)
		update(q)
		return redirect(url_for('doctors.doctors_home'))

	if action=='delete':
		q="delete from uploadprescription where user_id='%s'"%(uid)
		delete(q)
		return redirect(url_for('doctors.doctors_home'))
	return render_template('doctors_upload_prescription.html',data=data)




@doctors.route('/doctor_upload_prediction',methods=['post','get'])
def doctor_upload_prediction():
	data={}
	appoinment_id=request.args['appoinment_id']
	uid=request.args['uid']
	if 'submit' in request.form:
		upload=request.files['upload']
		path="static/images/"+str(uuid.uuid4())+upload.filename
		upload.save(path)
		# med=request.form['med']
		q="insert into upload_prediction_image values(null,'%s','%s','%s','pending','%s')"%(appoinment_id,session['did'],path,uid)
		insert(q)

	q="select * from upload_prediction_image where appoinment_id='%s'"%(appoinment_id)
	data['view']=select(q)

	# if 'action' in request.args:
	# 	action=request.args['action']
	# 	uid=request.args['uid']
	# else:
	# 	action=None

	# if action=='update':
	# 	q="select * from uploadprescription where user_id='%s'"%(uid)
	# 	data['up']=select(q)

	# if 'update' in request.form:
	# 	# med=request.form['med']
	# 	upload=request.files['upload']
	# 	path="static/images/"+str(uuid.uuid4())+upload.filename
	# 	upload.save(path)
	# 	amt=request.form['amt']
	# 	da=request.form['da']
	# 	q="update uploadprescription set uploadfile='%s',total_amount='%s',date='%s' where user_id='%s'"%(path,amt,da,uid)
	# 	update(q)
	# 	return redirect(url_for('doctors.doctors_home'))

	# if action=='delete':
	# 	q="delete from uploadprescription where user_id='%s'"%(uid)
	# 	delete(q)
	# 	return redirect(url_for('doctors.doctors_home'))
	return render_template('doctor_upload_prediction.html',data=data)


@doctors.route('/doctor_view_predict_output')
def doctor_view_predict_output():
	data={}
	pre_img_id=request.args['pre_img_id']
	# q="select * from appoinments inner join  doctors using(doctor_id) inner join users using(user_id) where doctor_id='%s'" %(did)
	q="select * from images  where pre_img_id='%s'"%(pre_img_id)
	data['view']=select(q)
	return render_template('doctor_view_predict_output.html',data=data)

@doctors.route('/doc_predict_output',methods=['get','post'])
def doc_predict_output():
	data={}
	if not session.get('did') is None:
		q="SELECT * FROM `appoinments` INNER JOIN `upload_prediction_image` USING(`appoinment_id`) INNER JOIN `users` ON `users`.`user_id`=`upload_prediction_image`.`user_id` ORDER BY `pre_img_id` DESC"
		# q="SELECT * FROM `appoinments` INNER JOIN `upload_prediction_image` USING(`appoinment_id`) INNER JOIN `doctors` USING(`doctor_id`) INNER JOIN `users` ON `users`.`user_id`=`upload_prediction_image`.`user_id` ORDER BY `pre_img_id` DESC"
		res=select(q)
		print(res)
		data['view']=res
		return render_template("doc_predict_output.html",data=data)
	else:
		return redirect(url_for('public.login'))
	

		return render_template("doc_predict_output.html",data=data)


from keras import backend as K
@doctors.route('/doc_predict_user_prediction',methods=['post','get'])
def doc_predict_user_prediction():
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
	return render_template('doc_predict_user_prediction.html',data=data)

@doctors.route('/predictiontable')
def predictiontable():
	data={}
	uid=request.args['uid']
	aid=request.args['appoinment_id']
 
	q="select * from images where user_id='%s'"%(uid)
	data['view']=select(q)
	return render_template('predictiontable.html',data=data)