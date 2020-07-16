from flask import Flask, session, redirect, url_for, request, render_template,flash
from random import randrange
import db
import os
import random
from datetime import date
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key='asdsdfsdfs13sdf_df%&'
app.config["IMAGE_UPLOADS"] = 'C:\\Users\\USER\\Documents\\dbms1\\static'


alert=dict()
info=[]
info1=[]
c=0
c1=0
@app.route('/')
def session():
	return render_template('index.html')


	"""-----------------------------------Warden------------------------------------------"""
	
@app.route('/wlogin',methods=['POST'])
def wlogin():
	if request.method == 'POST':
		user = request.form['uid']
		pwd=request.form['pwd']
		if user=="123" and pwd=="*****":
			return render_template("profile.html")
		else:
			return redirect("/")
@app.route('/backp')
def backp():
	return render_template('profile.html')

	"""-------------------------------STUDENT--------------------------------------------"""

@app.route('/signup')
def signup():
		return render_template("ssignup.html")

@app.route('/signsuccess',methods=['POST'])
def signsuccess():
	if request.method == 'POST':
		uid = request.form['uid']
		name=request.form['name']
		pwd=request.form['pwd']
		ph = request.form['ph']
		city=request.form['city']
		dob = request.form['dob']
		fees=request.form['fees']
		room = request.form['room']
		d=db.Student(name,uid,ph,city,dob,pwd,fees,room,0)
		d.save_to_db()
		return redirect("/signup")



@app.route('/slogin',methods=['POST'])
def slogin():
	cmd=""
	if request.method == 'POST':
		uid =  request.form['uid']
		pwd = request.form['pwd']
		if uid=="" or pwd=="":
			cmd='*please enter all the details'
		else:
			url='/backs/'+uid
			info=db.Student.load_from_db(uid)
			if info!=None:
				if(pwd==info[0]):
					login_user(uid)
					return redirect(url)
				else:
					cmd='*enter correct password'

		return render_template('index.html',info=cmd)

@app.route('/forgot')
def forgot():
	return render_template("reset_password.html")

@app.route('/reset',methods=['POST'])
def reset():
	if request.method == 'POST':
		uid = request.form['uid']
		pwd=request.form['pwd']
		rpwd=request.form['rpwd']
		if pwd==rpwd:
			db.Student.setpwd(uid,pwd)
	return redirect('/')



@app.route('/backs/<uid>',methods=['POST','GET'])
def backs(uid):
	info=db.Student.load_from_db(uid)
	return render_template('student.html',info=info,uid=uid)


@app.route('/logout')
def logout():
	logout_user()
	return render_template('index.html')

@app.route('/sdetails',methods=['POST','GET'])
def sdetails():
	info=db.Student.load_all()
	return render_template('sdetails.html',info=info)

@app.route('/sattendance',methods=['POST','GET'])
def sattendance():
	global info
	global c
	if c==0:
		info=db.Student.load_all()
		c=1
	return render_template('sattendance.html',info=info)

@app.route('/satt',methods=['POST','GET'])
def satt():
	global info
	print(info)
	if request.method == 'POST':
		att = list(request.form.keys())
		for i in att:
			for j in info:
				if i==str(j[0]):
					db.Student.put_att(j[0])
					info.remove(j)
	if len(info1)!=0:
		return redirect('/sattendance')
	return redirect('/backp')

@app.route('/student_remove',methods=["POST","GET"])
def sremove():
	if(request.method=='POST'):
		sid=request.form['sid']
		return_value=db.Student.remove_from_db(sid)
		if return_value==1:
			flash("success")
		elif return_value==0:
			flash("Enter the correct id")
	return render_template("student_remove.html")


"""------------------------------------ROOM----------------------------------"""
#request for the room
@app.route('/roomc/<uid>',methods=['POST','GET'])
def roomc(uid):
	return render_template('room.html',uid=uid)

@app.route('/rrequest/<uid>',methods=['POST'])
def rrequest(uid):
	if request.method == 'POST':
		room_id = request.form['id']
		db.Room.request(room_id,uid)
		#return redirect('/rooms/'+uid)
	return redirect('/backs/'+uid)

#request for swapping

@app.route('/rooms/<uid>',methods=['POST','GET'])
def rooms(uid):
	return render_template('form.html',uid=uid)

@app.route('/swap/<uid>',methods=['POST'])
def swap(uid):
	global alert
	print(alert)
	if request.method == 'POST':
		room_id = request.form['id']
		for i in list(alert):
			if i==uid:
				alert.pop(i)
		try:
			alert[uid]=[room_id,random.randrange(0,1000)]
		except:
			print('Error')
		return render_template('code.html',uid=uid,uid1=room_id)

@app.route('/success/<uid>/<uid1>',methods=['POST','GET'])
def success(uid,uid1):
	global alert
	if request.method == 'POST':
		code = request.form['code']
		for i in list(alert):
			if str(i==str(uid)):
				print('Hi')
				if str(code) == str(alert[i][1]):
					print('Success')
					db.Room.swap(uid,uid1)
					for i in list(alert):
						if alert[i][0]==uid1:
							alert.pop(i)
	return redirect('/backs/'+uid)

#list of all the codes

@app.route('/codes/<uid>',methods=['POST','GET'])
def codes(uid):
	c=0
	l=[]
	for i in list(alert):
		if alert[i][0]==uid:
				l.append([i,alert[i][1]])
				c=1
	print('l=',l)
	if len(l)!=0:
		return render_template('request.html',l=l,uid=uid)
	return redirect('/backs/'+uid)



@app.route('/rdetails')
def rdetails():
	info=db.Room.load_all()
	return render_template('rdetails.html',info=info)

"""--------------------------------EMPLOYEE----------------------------------------------------------"""
@app.route('/esignup')
def esignup():
	return render_template("esignup.html")

@app.route('/esignsuccess',methods=['POST'])
def esignsuccess():
	if request.method == 'POST':
		uid = request.form['uid']
		name=request.form['name']
		ph=request.form['ph']
		city=request.form['city']
		dob = request.form['dob']
		salary=request.form['salary']
		gen= request.form['gen']
		d=db.Employee(name,uid,ph,city,dob,gen,salary,0)
		d.save_to_db()
		return redirect("/esignup")

@app.route('/edetails',methods=['POST','GET'])
def edetails():
	info=db.Employee.load_all()
	if len(info)!=0:
		return render_template('edetails.html',info=info)
	else:
		return redirect('/backp')
@app.route('/eattendance',methods=['POST','GET'])
def eattendance():
	global info1
	global c1
	if c1==0:
		info1=db.Employee.load_all()
		c1=1
	return render_template('eattendance.html',info=info1)

@app.route('/eatt',methods=['POST','GET'])
def eatt():
	global info1
	if request.method == 'POST':
		att = list(request.form.keys())
		for i in info1:
			if(str(i[0])==str(att[0])):
				db.Employee.put_att(i[0])
				info1.remove(i)
	if len(info1)!=0:
		return redirect('/eattendance')
	return redirect('/backp')

@app.route('/employee_remove',methods=["POST","GET"])
def eremove():
	if(request.method=='POST'):
		eid=request.form['eid']
		info=db.Employee.remove_from_db(eid)
		if info==1:
			flash("success")
		elif info==0:
			flash("Enter the correct id")
	return render_template("employee_remove.html")





"""-------------------------receipe----------------------"""

@app.route('/add',methods=['POST','GET'])
def add():
	return render_template('add.html')

@app.route('/sadd',methods=['POST','GET'])
def sadd():
	if request.method == 'POST':
		name = request.form['name']
		type1 = request.form['type']
		db.Food.save_to_db(name,type1)
	return redirect('/add')


@app.route('/recipe_remove',methods=["POST","GET"])
def rremove():
	if(request.method=='POST'):
		rname=request.form['rname']
		info=db.Food.remove_from_db(rname)
		if info==1:
			flash("success")
		elif info==0:
			flash("Enter the correct Recipe Name")
	return render_template("recipe_remove.html")

@app.route('/fdetails')
def fdetails():
	info=db.Food.load_all()
	return render_template('fdetails.html',info=info)

@app.route('/poll/<uid>')
def poll(uid):	
	today=date.today()
	if today.day==24:
		info=db.Food.load_from_db()
		return render_template('poll.html',uid=uid,info=info)
	else:
		return redirect('/backs/'+uid)

@app.route('/pollc/<uid>', methods=['POST','GET'])
def pollc(uid):
	d=0
	url='/backs/'+uid
	if request.method == 'POST':
		poll_list=request.form.getlist('check')
		for i in request.form.getlist('check'):
			d=d+1
	if(d!=7):
		info=db.Food.load_from_db()
		return render_template('poll.html',uid=uid,info=info)
	for i in poll_list:
		db.Food.poll(i,uid)
	return redirect(url)


@app.route('/schedule',methods=['POST','GET'])
def schedule():
	count=db.Food.count()
	for i in range(len(count)-7):
		count.pop()
	flag=[0,0,0,0,0,0,0]
	temp=[]
	i=0
	while(i<len(count)):
		k=randrange(0,len(count))
		if flag[k]==0:
			temp.append(count[k][0])
			flag[k]=1
			i=i+1
	return render_template('schedule.html',info=temp)

@app.route('/food_scheme',methods=['POST','GET'])
def food_scheme():
	count=db.Food.count()
	for i in range(len(count)-7):
		count.pop()
	flag=[0,0,0,0,0,0,0]
	temp=[]
	i=0
	while(i<len(count)):
		k=randrange(0,len(count))
		if flag[k]==0:
			temp.append(count[k][0])
			flag[k]=1
			i=i+1
	return render_template('food_scheme.html',info=temp)

"""@app.route('/scheme/<uid>',methods=['POST','GET'])
def scheme(uid):
	global day
	cnt=0
	today=date.today()
	print(today.day)
	c=0
	if today.day==2:
		info=db.Food.result()
		for i in info:
			day[cnt]=i[0]
			cnt=cnt+1
		if cnt!=7:
			while cnt<7:
				info1=db.Food.load_all()
				for i in info1:
					k=0
					if i[1]=='Breakfast':
						for j in info:
							if i[0]==j[0]:
								k=1
						if k==0:
							day[cnt]=i[0]
							cnt=cnt+1
			
	return render_template('schedule.html',uid=uid,info=day)"""

"""------------------------------FEEDBACK--------------------------------"""
#feedback given by the student
@app.route('/send/<uid>',methods=['POST'])
def send(uid):
	if request.method == 'POST':
		content = request.form['content']
		d=db.Feedback(uid,content)
		d.save_to_db()
		url='/backs/'+uid
	return redirect(url)


#list of all the feedbacks
@app.route('/feedback',methods=['POST','GET'])
def feedback():
	info=db.Feedback.load_from_db()
	return render_template('feedback.html',info=info)

"""-------------------------------BILL--------------------------------"""
@app.route('/bill')
def bill():
	return render_template("bill.html")

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

	if request.method == "POST":

		if request.files:

			image = request.files["image"]
			image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			url='/static/'+image.filename
			db.Bill.save_to_db(url)

	return redirect("/bill")

@app.route('/bdetails',methods=['POST','GET'])
def bdetails():
	info=db.Bill.load_from_db()
	if len(info)!=0:
		return render_template('bdetails.html',info=info)
	return redirect('/backp')





  
if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug=True)











	