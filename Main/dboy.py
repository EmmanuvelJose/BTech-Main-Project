from flask import *
from database import *
import uuid
dboy=Blueprint('dboy',__name__)
 

@dboy.route('/dboyhome',methods=['get','post'])
def dboyhome():
	if not session.get('lid') is None:
		did=session['did']
		dname=session['dname']
		return render_template('dboyhome.html',dname=dname)
	else:
		return redirect(url_for('public.login'))




@dboy.route('/dboy_view_assigned',methods=['get','post'])
def dboy_view_assigned():
	if not session.get('lid') is None:
		did=session['did']
		data={}
		dname=session['dname']
		q="select *,`uploadprescription`.`date` AS pdate from delivery inner join uploadprescription using(prescription_id) inner join users using(user_id) where boy_id='%s' and `status`='dispatched'"%(did)
		print(q)
		res=select(q)
		data['assigned']=res
		if 'action' in request.args:
			id=request.args['bid']
			action=request.args['action']
		else:
			action=None
		if action=='delivered':
				q="update uploadprescription set status='delivered' where prescription_id='%s'"%(id)
				update(q)
				q="update delivery set date=NOW() where prescription_id='%s'"%(id)
				update(q)
				flash("UPDATED SUCCESFULLY")
				return redirect(url_for('dboy.dboy_view_assigned'))
		return render_template('dboy_view_assigned.html',data=data)
	else:
		return redirect(url_for('public.login'))


@dboy.route('/dboy_view_rating',methods=['get','post'])
def dboy_view_rating():
	if not session.get('lid') is None:
		did=session['did']
		data={}
		q="select * from rating inner join users using(user_id) where boy_id='%s'"%(did)
		res=select(q)
		print(res)
		data['rating']=res
		print(res)

		return render_template('dboy_view_rating.html',data=data)

	else:
		return redirect(url_for('public.login'))