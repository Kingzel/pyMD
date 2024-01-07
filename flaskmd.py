from flask import Flask, render_template, redirect, request, url_for, session
from main import put_place, pick
import logging

app = Flask(__name__,template_folder='web/html', static_folder='web' )
app.secret_key = 'pymdsecret1234@!!@'
glob={}
log = logging.getLogger('werkzeug')
log.disabled = True



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("diagnose"))

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/sent',methods = ['POST','GET'])
# def sent():
#      if request.method == 'POST':
             
     
@app.route('/diagnose',methods = ['POST','GET'])
def diagnose():
    if 'name' in session:
        if request.method=='GET':
            glob["picked"] =pick()
            glob["picked_question_data"] = glob["picked"][0]
            glob["picked_question"] =glob["picked_question_data"]['question_en']
            glob["picked_options"] = glob["picked"][1]
            glob["picked_question_type"] = glob["picked"][2]
            # print('New question loaded!')
        elif request.method=='POST':
             if glob["picked_question_type"]  ==0: #binary:
                    # print(glob["picked_question_data"]['name'])
                    colname =glob["picked_question_data"]['name']
                    val = 0
                    if 'yes' in request.form.to_dict().keys():
                         val = 1
                    print(put_place(colname,val)) 
                         
             elif glob["picked_question_type"] ==1: #cat sc:
                    # print(glob["picked_question_data"]['name'],request.form.to_dict())
                    colname = glob["picked_question_data"]['name']+"_@_"+str(list(request.form.to_dict().values())[0])
                    val = 1
                    print(put_place(colname,val)) 
             
             
             elif glob["picked_question_type"] ==2: #ord sc:
                    # print(glob["picked_question_data"]['name'],request.form.to_dict())
                    colname = glob["picked_question_data"]['name']
                    val = int(list(request.form.to_dict().values())[0])
                    print(put_place(colname,val)) 


             elif glob["picked_question_type"] ==3: #multi choice:
                    for V in request.values.getlist("group"):
                        colname = glob["picked_question_data"]['name']+"_@_"+str(V)
                        val =1
                        print(put_place(colname,val)) 

             
             
             
             return redirect(url_for("diagnose"))
        
        
        
        return render_template('diagnose.html',question =glob["picked_question"],options =glob["picked_options"],q_type =glob["picked_question_type"])
    else:
         return redirect(url_for("start_form"))

@app.route('/start', methods = ['POST','GET'])
def start_form():
        if request.method == 'POST':
             session.permanent = False
             session["name"],session["email"],session["gender"],session["is_send"] = request.form['name'],request.form['email'],request.form['gender'],request.form.get('send-chk')
             return redirect(url_for("diagnose"))
        else:
            return render_template('formstart.html')


if __name__ == "__main__":
    app.run(debug=True)