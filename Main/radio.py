from flask import *
from database import *
import uuid

radio=Blueprint('radio',__name__)

@radio.route('/radiohome')
def radiohome():
	return render_template('radiohome.html')

@radio.route('/radio_view_appointment')
def radio_view_appointment():
	data={}
	# q="select * from appoinments inner join  doctors using(doctor_id) inner join users using(user_id) where doctor_id='%s'" %(did)
	q="SELECT * FROM appoinments INNER JOIN `schedule` USING(`schedule_id`) INNER JOIN   doctors USING(doctor_id) INNER JOIN users USING(user_id)"
	data['view']=select(q)
	return render_template('radio_view_appointment.html',data=data)


@radio.route('/radio_view_customers')
def radio_view_customers():
	data={}
	appoinment_id = request.args.get('aid')
	user_id = request.args.get('uid')
	
	q="SELECT * FROM users JOIN appoinments WHERE appoinment_id = '{}' AND users.user_id = '{}'".format(appoinment_id, user_id)
	data['view']=select(q)
	return render_template('radio_view_customers.html',data=data)


import os
import uuid

from keras import backend as K
from newcnn import *

@radio.route('/radio_upload_prediction', methods=['GET', 'POST'])
def radio_upload_prediction():
	data={}
	appoinment_id = request.args.get('appoinment_id')
	user_id = request.args.get('uid')
	
	q="SELECT * FROM users JOIN appoinments WHERE appoinment_id = '{}' AND users.user_id = '{}'".format(appoinment_id, user_id)
	data['view']=select(q)

	if request.method == 'POST':
		uploaded_file = request.files["uploaded_file"]
		if uploaded_file:
			filename = f"{str(uuid.uuid4())}.jpg"
			path = os.path.join('static/images', filename)
			uploaded_file.save(path)

			q = "insert into upload_prediction_image (appoinment_id, doctor_id, filedetails, out_put_pre, user_id) VALUES ('%s', 100, '%s', 'pending', '%s')" % (appoinment_id, path, user_id)
			insert(q)

			# pre_img_id= "select pre_img_id from upload_prediction_image WHERE appoinment_id = '{}' AND users.user_id = '{}'".format(appoinment_id, user_id)
			# pre_img_id = select_pre_img_id(appoinment_id, user_id)

			values=preprocess_image(path)

			# q="INSERT `images` VALUES(NULL,'%s','%s','%s','%s')"%(user_id,path,values,pre_img_id)
			# insert(q)
   
			q2 = "select pre_img_id from upload_prediction_image WHERE appoinment_id = '{}' AND user_id = '{}'".format(appoinment_id, user_id)
			pre_img_id = select(q2)[-1]['pre_img_id']

			
			# Extract pre_img_id from the query result
			# if pre_img_id:
			# 	pre_img_id = pre_img_id[0]['pre_img_id']
			# else:
			# 	pre_img_id = None # Handle the case where pre_img_id is not found


			q3="INSERT INTO images (user_id, pre_image, predicted, pre_img_id) VALUES ('%s', '%s', '%s', %d)" %((user_id, path, values, pre_img_id))
			insert(q3)
			
			return redirect(url_for('radio.radioresults',  pre_img_id=pre_img_id))
		
	return render_template('radio_upload_prediction.html',data=data)

# def select_pre_img_id(appoinment_id, user_id):
#     q = "select pre_img_id from upload_prediction_image WHERE appoinment_id = %s AND user_id = %s"
#     pre_img_id = select(q % (appoinment_id, user_id))[0][0]
#     return pre_img_id


@radio.route('/radioresults',methods=['post','get'])
def radioresults():	
	data={}
	# appoinment_id = request.args.get('appoinment_id')
	# user_id = request.args.get('uid')
	pre_img_id = request.args.get('pre_img_id')

	q="select predicted from images where pre_img_id = '%s'" % pre_img_id
	data['view']=select(q)

	return render_template('radioresults.html', data=data)

	# q= "select pre_img_id, user_id, filedetails from upload_prediction_image where appoinment_id = '{}' AND user_id = '{}'".format(appoinment_id, user_id) 
	# data['view']=select(q)


	
	

# @radio.route('/radioresults',methods=['post','get'])
# def radioresults():
# 	data={}
# 	appoinment_id=request.args['appoinment_id']
# 	uid=request.args['uid']
# 	uploaded_file = request.files["uploaded_file"]

# 	path="static/images/"+str(uuid.uuid4())+ ".jpg"
# 	print("File Path:", path) 

# 	uploaded_file.save(path)
# 	flag=0
# 	q = "INSERT INTO upload_prediction_image (appoinment_id, doctor_id, filedetails, out_put_pre, user_id) VALUES ('%s', 100, '%s', 'pending', '%s')" % (appoinment_id, path, uid)
# 	insert(q)
# 	# print("File Path:", path) 
# 	try:
# 		insert(q)
# 		flag = 1  # Set flag to 1 if insert statement succeeds
# 		print("File inserted successfully:", path)
# 	except Exception as e:
# 		print("Error inserting file:", e)
# 	print("Flag:", flag)

# 	return render_template('radioresults.html',data=data,  flag=flag, appoinment_id=appoinment_id, user_id=uid)
# 	



	# if 'submit' in request.form:
	# 	upload=request.files['upload']
	# 	path="static/images/"+str(uuid.uuid4())+upload.filename
	# 	upload.save(path)
	# 	# med=request.form['med']
	# 	q="insert into upload_prediction_image values(null,'%s',100,'%s','pending','%s')"%(appoinment_id,path,uid)
	# 	insert(q)

	# q="select * from upload_prediction_image where appoinment_id='%s'"%(appoinment_id)
	# data['view']=select(q)
	# return render_template('radioresults.html',data=data)
	

