from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.vars = {}

app.questions={}
app.questions['How many eyes do you have?']=('1','2','3')
app.questions['Which fruit do you like best?']=('banana','mango','pineapple')
app.questions['Do you like cupcakes?']=('yes','no','maybe')

app.nquestions = len(app.questions)

@app.route('/index_lulu',methods=['GET','POST'])
def index_lulu():
  nquestions = 5
  if request.method == 'GET':
    return render_template('userinfo_lulu.html',num=nquestions)
  else:
    # request was a POST
    app.vars['name'] = request.form['name_lulu']
    app.vars['age'] = request.form['age_lulu']

    f = open('%s_%s.txt'%(app.vars['name'],app.vars['age']),'w')
    f.write('Name: %s\n'%(app.vars['name']))
    f.write('Age: %s\n\n'%(app.vars['age']))
    f.close()

    return redirect('/main_lulu') 

@app.route('/main_lulu',methods=['POST'])
def main_lulu2():
  if len(app.questions)==0:
    return render_template('end_lulu.html')
  return redirect('/next_lulu')

@app.route('/next_lulu',methods=['GET'])
def next_lulu():
  n = app.nquestions - len(app.questions) + 1
  q = app.questions.keys()[0]
  a1, a2, a3 = app.questions.values()[0]

  # save the current question key
  app.currentq = q
  
  return render_template('layout_lulu.html',num=n,question=q,
      ans1=a1,ans2=a2,ans3=a3)

@app.route('/next_lulu',methods=['POST'])
def next_lulu2():
  f = open('%s_%s.txt'%(app_lulu.vars['name'],app_lulu.vars['age']),'a') #a is for append
  f.write('%s\n'%(app_lulu.currentq))
  f.write('%s\n\n'%(request.form['answer_from_layout_lulu'])) #this was the 'name' on layout.html!
  f.close()

  # Remove question from dictionary
  del app.questions[app.currentq]

  return redirect('/main_lulu')
       


if __name__ == '__main__':
  #app.run(port=33507)
  app.run(host='0.0.0.0')
