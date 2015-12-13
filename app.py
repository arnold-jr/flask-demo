from flask import Flask, render_template, request, redirect
from quandle_eg import make_plot

app = Flask(__name__)
    
app.vars = {'ticker_name':'cmg',
    'script':'',
    'div':''}

flag,script,div = make_plot(app.vars['ticker_name'])
if flag:
  app.vars['script'] = script
  app.vars['div'] = div

@app.route('/',methods=['GET','POST'])
def main_redir():
  return redirect('/index')
      
@app.route('/index',methods=['GET','POST'])
def index():
  nquestions = 5
  if request.method == 'GET':
    # pass the script and div to the boilerplate html
    return render_template('boilerplate.html',
        script=app.vars['script'],div=app.vars['div'])
  else:
    # request was a POST
    app.vars['ticker_name'] = request.form['ticker_name']
    flag,script,div = make_plot(app.vars['ticker_name'])
    if flag:
      app.vars['script'] = script
      app.vars['div'] = div
    return render_template('boilerplate.html',
        script=app.vars['script'],div=app.vars['div'])


if __name__ == '__main__':
  #app.run(port=33507)
  app.run(host='0.0.0.0')
