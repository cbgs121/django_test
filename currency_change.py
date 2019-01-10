from flask import Flask,render_template,request
import requests
app = Flask('__name__')

bes = requests.get("http://data.fixer.io/api/latest?access_key=f5fa97d30aadbd1c44f9df7e8319d106")
res = requests.get("http://data.fixer.io/api/2013-03-16?access_key=f5fa97d30aadbd1c44f9df7e8319d106&symbols=USD,AUD,CAD,PLN,INR&format=1")
detail = requests.get("http://data.fixer.io/api/symbols?access_key=f5fa97d30aadbd1c44f9df7e8319d106")
if res.status_code != 200:
    raise Exception("Error:Api request is unsuccessful")
if bes.status_code != 200:
    raise Exception("Error:Api request is unsuccessful")
if detail.status_code != 200:
    raise Exception("Error:Api request is unsuccessful")
details = detail.json()
data = res.json()
dat = bes.json()
cur = details['symbols'].items()
@app.route('/', methods=['POST', "GET"])
def index():
    if request.method =="GET":
        return render_template('currency.html',currency=cur)
    else:
        base = request.form.get('base')
        other = request.form.get('other')
        amt = float(request.form.get('amount'))
        base = base[-4:-1]
        other = other[-4:-1]
        val = dat['rates'][other] * 1 / dat['rates'][base]
        res = val*amt
        return render_template('currency.html',message=base[-4:], other=other[-4:], value=val, result=res,amt=amt)

