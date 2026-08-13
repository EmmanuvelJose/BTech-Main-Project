from flask import *
from database import *
# import demjson
import uuid
from datetime import datetime,date,timedelta
from newcnn import *



api=Blueprint('api',__name__)

@api.route('/login')
def login():
	data={}
	username=request.args['username']
	password=request.args['password']
	q="select * from login where username='%s' and password='%s'"%(username,password)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)

@api.route('/usermanagefeedback')
def usermanagefeedback():
	data={}
	lid=request.args['lid']
	complaint=request.args['complaint']
	q="insert into feedback values(null,(select user_id from users where login_id='%s'),'%s',curdate())"%(lid,complaint)
	insert(q)
	data['status']="success"
	data['method']="usermanagefeedback"
	return str(data)


@api.route('/userviewfeedback')
def userviewfeedback():
	data={}
	lid=request.args['lid']
	q="select * from feedback where user_id=(select user_id from users where login_id='%s')"%(lid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="userviewfeedback"
	return str(data)


@api.route('/userregister')
def userregister():
	data={}
	fname=request.args['fname']
	lname=request.args['lname']
	place=request.args['place']
	email=request.args['email']
	phone=request.args['phone']
	dob=request.args['dob']
	district=request.args['district']
	username=request.args['username']
	password=request.args['password']
	q="select * from login where username='%s'"%(username)
	res=select(q)
	if res:
		data['status']="duplicate"
	else:
		q="insert into login values(null,'%s','%s','user')"%(username,password)
		id=insert(q)
		q="insert into users values(null,'%s','%s','%s','%s','%s','%s','%s','%s')"%(id,fname,lname,dob,phone,email,place,district)
		insert(q)
		data['status']="success"
	return str(data)



@api.route('/doctorregister')
def doctorregister():
	data={}
	fname=request.args['fname']
	lname=request.args['lname']
	place=request.args['place']
	email=request.args['email']
	phone=request.args['phone']
	username=request.args['username']
	password=request.args['password']
	q="select * from login where username='%s'"%(username)
	res=select(q)
	if res:
		data['status']="duplicate"
	else:
		q="insert into login values(null,'%s','%s','pending')"%(username,password)
		id=insert(q)
		q="insert into doctors values(null,'%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phone,email)
		insert(q)
		data['status']="success"
	return str(data)


@api.route('/deliveryregister')
def deliveryregister():
	data={}
	name=request.args['name']
	lname=request.args['lname']
	email=request.args['email']
	phone=request.args['phone']
	username=request.args['username']
	password=request.args['password']
	q="select * from login where username='%s'"%(username)
	res=select(q)
	if res:
		data['status']="duplicate"
	else:
		q="insert into login values(null,'%s','%s','delivery')"%(username,password)
		id=insert(q)
		q="insert into deliveryboy values(null,'%s','%s','%s','%s','%s')"%(id,name,lname,phone,email)
		insert(q)
		data['status']="success"
	return str(data)






@api.route('/deliveryboyvieworderdispatched')
def deliveryboyvieworderdispatched():
	data={}
	lid=request.args['lid']
	q="select *,`uploadprescription`.`date` AS pdate from delivery inner join uploadprescription using(prescription_id) inner join users using(user_id) where boy_id=(select boy_id from deliveryboy where login_id='%s') and `status`='dispatched'"%(lid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="deliveryboyvieworderdispatched"
	return str(data)

@api.route('/deliveryboyvieworderpickup')
def deliveryboyvieworderpickup():
	data={}
	lid=request.args['lid']
	q="select *,`uploadprescription`.`date` AS pdate from delivery inner join uploadprescription using(prescription_id) inner join users using(user_id) where boy_id=(select boy_id from deliveryboy where login_id='%s') and `status`='pickup'"%(lid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="deliveryboyvieworderpickup"
	return str(data)


@api.route('/deliveryboyupdatestatustopickup')
def deliveryboyupdatestatustopickup():
	data={}
	lid=request.args['lid']
	pid=request.args['pid']
	q="update uploadprescription set status='pickup' where prescription_id='%s'"%(pid)
	update(q)
	q="update delivery set date=NOW() where prescription_id='%s'"%(pid)
	update(q)
	data['status']="success"
	data['method']="deliveryboyupdatestatustopickup"
	return str(data)


@api.route('/deliveryboyupdatestatustodeliverd')
def deliveryboyupdatestatustodeliverd():
	data={}
	lid=request.args['lid']
	pid=request.args['pid']
	q="update uploadprescription set status='delivered' where prescription_id='%s'"%(pid)
	update(q)
	q="update delivery set date=NOW() where prescription_id='%s'"%(pid)
	update(q)
	data['status']="success"
	data['method']="deliveryboyupdatestatustodeliverd"
	return str(data)






@api.route('/userviewmedicalshop')
def userviewmedicalshop():
	data={}
	q="SELECT * FROM `medicalshop`"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)




@api.route('/userview_doctors')
def userview_doctors():
	data={}
	q="SELECT * FROM `doctors`"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)


@api.route('/useruploadprescriptions',methods=['get','post'])
def useruploadprescriptions():
	data={}
	sid=request.form['sid']
	lid=request.form['logid']
	image=request.files['image']
	path="static/"+str(uuid.uuid4())+image.filename
	image.save(path)
	q="insert into uploadprescription values(null,'%s',(select user_id from users where login_id='%s'),'%s','',curdate(),'pending')"%(sid,lid,path)
	insert(q)
	data['status']="success"
	data['method']="useruploadprescriptions"
	return str(data)



@api.route('/userviewuploadedfilesprescription')
def userviewuploadedfilesprescription():
	data={}
	lid=request.args['lid']
	sid=request.args['sid']
	q="select * from uploadprescription where user_id=(select user_id from users where login_id='%s') and medicalshop_id='%s'"%(lid,sid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="userviewuploadedfilesprescription"
	return str(data)



@api.route('/userviewuploadedmedicaldetails')
def userviewuploadedmedicaldetails():
	data={}
	pid=request.args['pid']
	q="SELECT *,`medicinedetails`.`quantity` AS mquantity,`medicinedetails`.`rate` AS mrate,`medicinedetails`.`total` AS mtotal FROM `medicinedetails` INNER JOIN `uploadprescription` USING(prescription_id) INNER JOIN `medicines` USING(medicine_id) INNER JOIN `type` USING(type_id) WHERE prescription_id='%s'"%(pid)
	
	print(q)	
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="userviewuploadedmedicaldetails"
	return str(data)


@api.route('/useracceptmedicine')
def useracceptmedicine():
	data={}
	pid=request.args['pid']
	q="update `uploadprescription` set status='accept' where prescription_id='%s'"%(pid)
	update(q)
	data['status']="success"
	data['method']="useracceptmedicine"
	return str(data)



@api.route('/userrejectmedicine')
def userrejectmedicine():
	data={}
	pid=request.args['pid']
	q="update `uploadprescription` set status='reject' where prescription_id='%s'"%(pid)
	update(q)
	data['status']="success"
	data['method']="userrejectmedicine"
	return str(data)


@api.route('/usermakepayment')
def usermakepayment():
	data={}
	appoint_id=request.args['pid']
	amount=request.args['amount']
	q="insert into payment values(null,'%s','%s',curdate())"%(appoint_id,amount)
	insert(q)
	q="update `appoinments` set status='paid' where appoinment_id='%s'"%(appoint_id)
	update(q)
	data['status']="success"
	return str(data)


@api.route('/usermakeappointments')
def usermakeappointments():
	data={}
	date=request.args['date']
	lid=request.args['lid']
	sh=request.args['sh']
	time=request.args['time']
	# nop=request.args['nop']
	# nops=int(nop)
	# print(nops)
	
	
	q="insert into appoinments values(null,'%s',(select user_id from users where login_id='%s'),'%s','%s','pending','500')"%(sh,lid,date,time)
	insert(q)
	data['status']="success"
	data['method']="usermakeappointments"
	return str(data)

@api.route('/userviewappoinments')
def userviewappoinments():
	data={}
	
	lid=request.args['lid']
	q="SELECT * FROM   doctors INNER JOIN appoinments ON doctors.doctor_id where user_id=(select user_id from users where login_id='%s') "%(lid)
	res=select(q)
	print(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)



@api.route('/doctorviewappoinments')
def doctorviewappoinments():
	data={}
	
	lid=request.args['lid']
	q="SELECT * FROM  `appoinments` INNER JOIN `schedule` USING (schedule_id)  INNER JOIN users USING(user_id) where doctor_id=(select doctor_id from doctors where login_id='%s')"%(lid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)


@api.route('/doctorview_customers')
def doctorview_customers():
	data={}
	
	app_id=request.args['app_id']
	q="select * from users inner join appoinments using(user_id) where appoinment_id='%s'"%(app_id)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)

@api.route('/user_view_doctor_prescription')
def user_view_doctor_prescription():
	data={}
	
	appoi_id=request.args['appoi_id']
	q="select * from prescription inner join appoinments using(appoinment_id) where appoinment_id='%s'"%(appoi_id)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)

@api.route('/doctor_upload_prescription',methods=['get','post'])
def doctor_upload_prescription():
	data={}
	
	app_id=request.form['app_id']
	image=request.files['image']
	path="static/"+str(uuid.uuid4())+image.filename
	image.save(path)
	q="insert into prescription values(null,'%s','%s',curdate(),'pending')"%(app_id,path)
	
	insert(q)
	data['status']="success"
	return str(data)




@api.route('/viewrating')
def viewrating():
	data={}
	lid=request.args['lid']
	bid=request.args['bid']
	q="select * from rating where user_id=(select user_id from users where login_id='%s') and boy_id='%s'" %(lid,bid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res[0]['rated']
	else:
		data['status']="failed"
	data['method']='viewrating'
	return str(data)

@api.route('/userrating')
def userrating():
	data={}
	lid=request.args['lid']
	rate=request.args['rate']
	bid=request.args['bid']
	q="select * from rating where user_id=(select user_id from users where login_id='%s') and boy_id='%s'" %(lid,bid)
	res=select(q)
	if res:
		q="update rating set rated='%s' where user_id=(select user_id from users where login_id='%s') and boy_id='%s'" %(rate,lid,bid)
		update(q)
	else:
		q="insert into rating values(null,(select user_id from users where login_id='%s'),'%s','%s',curdate())" %(lid,bid,rate)
		insert(q)
	data['status']="success"
	data['method']='userrating'
	return str(data)



@api.route('/userviewdeliveryboys')
def userviewdeliveryboys():
	data={}
	pid=request.args['pid']
	q="SELECT * FROM `delivery` INNER JOIN `deliveryboy` USING(boy_id) WHERE prescription_id='%s'"%(pid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)



@api.route('/deliveryviewrating')
def deliveryviewrating():
	data={}
	lid=request.args['lid']
	q="select * from rating where boy_id=(select boy_id from deliveryboy where login_id='%s')" %(lid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res[0]['rated']
	else:
		data['status']="failed"
	return str(data)


# @api.route('/viewmedicalshop')
# def viewmedicalshop():
# 	data={}
# 	q="select * from medicalshop"
# 	res=select(q)
# 	if res:
# 		data['status']="success"
# 		data['data']=res 
# 	else:
# 		data['status']="failed"
# 		data['method']='viewmedicalshop'
# 	return str(data)


@api.route('/user_upload_doctor_prescription_to_medical_shop')
def user_upload_doctor_prescription_to_medical_shop():
	data={}
	img=request.args['file']
	datae=request.args['date']
	statusss=request.args['statusss']
	medicalshop=request.args['medicalshop']
	lid=request.args['lid']
	q="insert into uploadprescription values(null,'%s',(select user_id from users where login_id='%s'),'%s','0',curdate(),'pending')" %(medicalshop,lid,img)
	insert(q)
	data['status']="success"
	data['method']='user_upload_doctor_prescription_to_medical_shop'
	return str(data)


@api.route('/viewmedicalshop')
def viewmedicalshop():
	data={}
	q="select * from medicalshop"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res 
	else:
		data['status']="failed"
	data['method']='viewmedicalshop'
	return str(data)






@api.route('/doctor_view_dates')
def doctor_view_dates():
	data={}
	lid=request.args['lid']
	q="select * from schedule where doctor_id=(select doctor_id from doctors where login_id='%s')"%(lid)
	res=select(q)
	print(res)
	if res:
		data['status']="success"
		data['data']=res 
	else:
		data['status']="failed"
	data['method']='doctor_view_dates'
	return str(data)




@api.route('/doctor_add_available_dates')
def doctor_add_available_dates():
	data={}
	date=request.args['date']
	lid=request.args['lid']
	stime=request.args['stime']
	nops=request.args['nops']
	etime=request.args['etime']

	q="select * from schedule where date='%s' and doctor_id=(select doctor_id from doctors where login_id='%s')"%(date,lid)
	res=select(q)
	if res:
		data['status']="duplicate"
	else:
		q="insert into schedule values(null,(select doctor_id from doctors where login_id='%s'),'%s','%s','%s','%s','Available')" %(lid,date,stime,etime,nops)
		insert(q)
		data['status']="success"
	data['method']='doctor_add_available_dates'
	return str(data)





@api.route('/user_add_timing')
def user_add_timing():
	data={}
	adid=request.args['adid']
	time=request.args['time']
	endtime=request.args['endtime']


	x = time
	y = endtime
	hour_and_minute=x
	date_time_obj = datetime.strptime(x, '%H:%M')
	s=[]
	# s=""
	while hour_and_minute<y:
		if hour_and_minute<y:
			date_time_obj += timedelta(minutes=15)
			hour_and_minute = date_time_obj.strftime("%H:%M")
			print(hour_and_minute)

			q="insert into available_time values(null,'%s','%s')" %(adid,hour_and_minute)
			insert(q)
			s.append(hour_and_minute)
			
		else:
			break
	data['s']=s

	# for i in range(0,len(s)+1):

	# 	print(s,">>>>>>>>>>>>>>>>>>>>")

		
	data['status']="success"
	return str(data)




@api.route('/userviewdoctordate')
def userviewdoctordate():
	data={}
	docc_ids=request.args['docc_ids']


	q="select * from schedule where doctor_id='%s'"%(docc_ids)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res 
	else:
		data['status']="failed"
	return str(data)




@api.route('/userviewtimeslot')
def userviewtimeslot():
	data={}
	ids=request.args['ids']


	q="SELECT * FROM `available_time` WHERE `times` NOT IN(SELECT `time` FROM `appoinments`) and  available_date_id='%s'"%(ids)
	print(q)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res 
	else:
		data['status']="failed"
	data['method']="userviewtimeslot"
	return str(data)



from keras import backend as K

@api.route('/Farmer_upload_image',methods=['get','post'])
def Farmer_upload_image():
	K.clear_session()
	data={}
	image=request.files['image']
	path='static/uploads/'+str(uuid.uuid4())+ ".jpg"
	image.save(path)
	log_id=request.form['log_id']
	values=preprocess_image(path)
	q="INSERT `images` VALUES(NULL,(SELECT `user_id` FROM `users` WHERE `login_id`='%s'),'%s','%s')"%(log_id,path,values)
	print(q)
	res=insert(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="Farmer_upload_image"
	return str(data)



@api.route('/viewimg')
def viewimg():
	data={}
	log_id=request.args['log_id']
	q="SELECT * FROM `images` WHERE `user_id`=(SELECT `user_id` FROM `users` WHERE `login_id`='%s') ORDER BY `predict_id` DESC"%(log_id)
	print(q)
	result=select(q)
	if result:
		data['status'] = 'success'
		data['data'] = result
	else:
		data['status'] = 'failed'
	data['method'] = 'viewimg'
	return str(data)
