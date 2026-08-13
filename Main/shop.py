from flask import *
from database import *
import uuid
shop=Blueprint('shop',__name__)
 

@shop.route('/shophome',methods=['get','post'])
def shophome():
	if not session.get('lid') is None:

		sid=session['sid']
		sname=session['sname']
		return render_template('shophome.html',sname=sname)

	else:
		return redirect(url_for('public.login'))


@shop.route('/shop_manage_medicine',methods=['get','post'])
def shop_manage_medicine():
	data={}	
	if not session.get('lid') is None:

		sid=session['sid']
		q="select * from type"
		res=select(q)
		data['type']=res
		sid=session['sid']
		if 'submit' in request.form:
			typ=request.form['typ']
			med=request.form['med']
			det=request.form['det']
			rate=request.form['rate']
			m_date=request.form['mdate']
			edate=request.form['edate']
			qua=request.form['qua']
			q="insert into medicines values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s')"%(sid,typ,med,det,rate,qua,m_date,edate)
			lid=insert(q)
			flash("ADDED SUCESSFULLY")
			return redirect(url_for('shop.shop_manage_medicine'))
		q="select * from medicines inner join type using(type_id) where medicalshop_id='%s'"%(sid)
		res=select(q)
		if res:
			data['med']=res
			print(res)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="delete from medicines where medicine_id='%s'"%(id)
			delete(q)
			
			return redirect(url_for('shop.shop_manage_medicine'))
		if action=='update':
			q="select * from medicines where medicine_id='%s'"%(id)
			data['updater']=select(q)
		if 'update' in request.form:
			typ=request.form['typ']
			med=request.form['med']
			det=request.form['det']
			rate=request.form['rate']
			qua=request.form['qua']
			q="update medicines set type_id='%s',medicine='%s',details='%s',rate='%s',quantity='%s' where medicine_id='%s'"%(typ,med,det,rate,qua,id)
			update(q)
			return redirect(url_for('shop.shop_manage_medicine'))
		return render_template('shop_manage_medicine.html',data=data)


	else:
		return redirect(url_for('public.login'))

@shop.route('/shop_view_docterp',methods=['get','post'])
def shop_view_docterp():
	if not session.get('lid') is None:
		data={}
		sid=session['sid']
		q="SELECT * FROM `uploadprescription` INNER JOIN users USING(user_id) WHERE medicalshop_id='%s'"%(sid)
		res=select(q)
		print(res)
		data['orders']=res
		

		return render_template("shop_view_docterp.html",data=data)
	else:
		return redirect(url_for('public.login'))


@shop.route('/shop_upoload_medi',methods=['get','post'])
def shop_upoload_medi():
	data={}
	if not session.get('lid') is None:
		prescription_id=request.args['prescription_id']
		data['prescription_id']=prescription_id
		name=request.args['name']
		data['name']=name
		q="SELECT * from medicines"
		res=select(q)
		print(res)
		data['med']=res
		q="select * from uploadprescription where prescription_id='%s'"%(prescription_id)
		res=select(q)
		data['totalamount']=res[0]['totalamount']
		q="select *,medicinedetails.quantity as mdqua from medicinedetails inner join medicines using(medicine_id) inner join type using(type_id) where prescription_id='%s'"%(prescription_id)
		res=select(q)
		print(res)
		data['mdet']=res
		if 'action' in request.args:
			mid=request.args['id']
			q="select total from medicinedetails where medicine_id='%s' and prescription_id='%s'"%(mid,prescription_id)
			res=select(q)
			delamt=res[0]['total']
			q="delete from medicinedetails where medicine_id='%s'"%(mid)
			delete(q)
			q="update uploadprescription set totalamount=totalamount-'%s' where prescription_id='%s'"%(delamt,prescription_id)
			update(q)
			return redirect(url_for('shop.shop_upoload_medi',prescription_id=prescription_id,name=name))

		if 'submit' in request.form:
			med=request.form['med']
			qua=request.form['qua']
			qua=int(qua)
			q="select * from medicines where medicine_id='%s'"%(med)
			res=select(q)
			avlqua=int(res[0]['quantity'])
			r=res[0]['rate'].split(".")
			rate=int(r[0])
			if avlqua<qua:
				flash("REQUIRED QUANTITY IS NOT AVAILABLE IN OUR STOCK")
			else:
				amt=qua*rate
				print("555555555555555")
				print(amt)
				q="select * from medicinedetails where prescription_id='%s' and medicine_id='%s'"%(prescription_id,med)
				print(q)
				res=select(q)
				if res:
					print(res)
					preamt=res[0]['total']
					q="select * from uploadprescription where prescription_id='%s'"%(prescription_id)
					res=select(q)
					print(res)
					totalamount=res[0]['totalamount']
					newamt=int(totalamount)+int(amt)-(int(preamt))

					q="update uploadprescription set totalamount='%s' where prescription_id='%s'"%(newamt,prescription_id)
					print(q)
					update(q)
					q="update medicinedetails set total='%s',quantity='%s' where  prescription_id='%s' and medicine_id='%s'"%(amt,qua,prescription_id,med)
					update(q)
					flash("THIS MEDICINE ALREDY ADDED !UPDATED SUCCEDFULLY")
					return redirect(url_for('shop.shop_upoload_medi',prescription_id=prescription_id,name=name))
				else:
					q="insert into medicinedetails values(NULL,'%s','%s','%s','%s','%s')"%(prescription_id,med,qua,rate,amt)
					insert(q)
					q="update uploadprescription set totalamount=totalamount+'%s' where prescription_id='%s'"%(amt,prescription_id)
					update(q)
					flash("ADDED SUCESSFULLY")
					return redirect(url_for('shop.shop_upoload_medi',prescription_id=prescription_id,name=name))

		return render_template("shop_upoload_medi.html",data=data)

	else:
		return redirect(url_for('public.login'))




@shop.route('/shopviewpro',methods=['get','post'])
def shopviewpro():
	if not session.get('lid') is None:
		data={}
		prescription_id=request.args['prescription_id']
		data['prescription_id']=prescription_id
		name=request.args['name']
		data['name']=name
		q="SELECT * from medicines"
		res=select(q)
		print(res)
		data['med']=res
		q="select * from uploadprescription"
		res=select(q)
		data['totalamount']=res[0]['totalamount']
		q="select *,medicinedetails.quantity as mdqua from medicinedetails inner join medicines using(medicine_id) inner join type using(type_id) where prescription_id='%s'"%(prescription_id)
		res=select(q)
		print(res)
		data['mdet']=res
		return render_template("shopviewpro.html",data=data)

	else:
		return redirect(url_for('public.login'))


@shop.route('/shop_assigntodboy',methods=['get','post'])
def shop_assigntodboy():
	if not session.get('lid') is None:
		data={}

		prescription_id=request.args['prescription_id']
		q="select * from deliveryboy"
		res=select(q)
		data['dboy']=res
		if 'submit' in request.form:
			dboy=request.form['dboy']
			q="insert into delivery values(NULL,'%s','%s',curdate())"%(prescription_id,dboy)
			insert(q)
			
			q="update uploadprescription set status='dispatched' where prescription_id='%s'"%(prescription_id)
			update(q)
			flash("ASSIGNED SUCCESFULLY")
			return redirect(url_for('shop.shop_view_docterp'))


		return render_template("shop_assigntodboy.html",data=data)


	else:
		return redirect(url_for('public.login'))