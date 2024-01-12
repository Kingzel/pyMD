import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from flask import Flask, render_template, redirect, request, url_for, session
import logging
import pymdroutines as pmdr
import pickle as p
import pandas as pd
import numpy as np
import copy
import os
import random
import evaluate as e
from scipy.stats import beta


app = Flask(__name__,template_folder='web/html', static_folder='web')
app.secret_key = 'pymdsecret1234@!!@'
glob={}
#log = logging.getLogger('werkzeug')
#log.disabled = True




#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
os.system('cls')
evids =pd.read_json("data\\release_evidences.json")
evids1 = pd.read_json("data\\release_evidences.json")
conds  = pd.read_json('data\\release_conditions.json')
evids1 = evids1.T


conds = conds.T
conds.drop(['cond-name-fr','cond-name-eng','icd10-id'], axis=1, inplace=True)


cond_to_evi = {}
int_to_cond ={}
cond_to_int ={}
for i in range(len(conds)):
   condition=  conds.iloc[i]
   name =condition['condition_name']
   cond_to_evi[name] = set(condition['symptoms'].keys()).union(set(condition['antecedents'].keys()))
   int_to_cond[i]=name
   cond_to_int[name]=i





multi_evi = pmdr.gen_multichoice_features(evids,'M')
ordinal_evi_sc= pmdr.gen_singlechoice_features(evids,'MO')
categorical_evi_sc = pmdr.gen_singlechoice_features(evids,'MC')
binary_evi =pmdr.gen_binary_features(evids)



with open('trained_model.bin', 'rb') as f:
    rf =  p.load(f)
    cols  = p.load(f)
dummy= pmdr.gen_empty(cols,1)
all_classes_probab = e.all_classes_probab(rf,dummy)

questions_asked = []


#Thompson Sampling RL 
n_pos =np.zeros(len(conds))
n_neg=np.zeros(len(conds))


def pick_bandit():
    iter_max =0
    for j in range(len(n_neg)):
        sampled_beta =  np.random.beta(n_pos[j]+1,n_neg[j]+1)
        if iter_max < sampled_beta:
            iter_max = sampled_beta
            selected = j
    print("Selected:",int_to_cond[selected])
    return selected

with open("colors.txt", "r") as f:
     clist  = f.read().split()

def plot_bandits():
        for j in range(49):
            x = np.linspace(0,1,200)
            y= beta.pdf(x,n_pos[j]+1,n_neg[j]+1)
            plt.plot(x,y,color = clist[j])
        plt.xlabel("Estimated Probability")
        plt.ylabel("Probability of Conditions")
        plt.title("BetaPDF")
        name =random.randrange(3,100000)
        plt.savefig(f'{name}.png')

#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
glob['q_asked'] =20

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result')
def result():
    # print(glob['disease'],glob['probab'])
    return render_template('result.html', disease=glob['disease'], probab = glob['probab'])

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
            if glob['q_asked'] > 0:
                glob["picked"] =pick()
                glob["picked_question_data"] = glob["picked"][0]
                glob["picked_question"] =glob["picked_question_data"]['question_en']
                glob["picked_options"] = glob["picked"][1]
                glob["picked_question_type"] = glob["picked"][2]
                glob['q_asked'] = glob['q_asked']-1
            else:
                 all_classes = e.all_classes_probab(rf,dummy)
                 diseases=[]
                 probabilities = []
                 for dis in all_classes:
                      diseases.append(dis)
                      probabilities.append(np.round(np.round(all_classes[dis],4)*100,2))
                 glob["disease"] =diseases
                 glob['probab'] = probabilities
                #  print(all_classes)
                 return redirect(url_for('result'))
                 
            # print('New question loaded!')
        elif request.method=='POST':
             if glob["picked_question_type"]  ==0: #binary:
                    # print(glob["picked_question_data"]['name'])
                    colname =glob["picked_question_data"]['name']
                    val = 0
                    if 'yes' in request.form.to_dict().keys():
                         val = 1
                    put_place(colname,val)
                         
             elif glob["picked_question_type"] ==1: #cat sc:
                    # print(glob["picked_question_data"]['name'],request.form.to_dict())
                    colname = glob["picked_question_data"]['name']+"_@_"+str(list(request.form.to_dict().values())[0])
                    val = 1
                    put_place(colname,val)
             
             
             elif glob["picked_question_type"] ==2: #ord sc:
                    colname = glob["picked_question_data"]['name']
                    val = int(list(request.form.to_dict().values())[0])
                    put_place(colname,val)


             elif glob["picked_question_type"] ==3: #multi choice:
                    for V in request.values.getlist("group"):
                        colname = glob["picked_question_data"]['name']+"_@_"+str(V)
                        val =1
                        put_place(colname,val)

             
             
             
             return redirect(url_for("diagnose"))
        
        
        
        return render_template('diagnose.html',question =glob["picked_question"],options =glob["picked_options"],q_type =glob["picked_question_type"])
    else:
         return redirect(url_for("start_form"))

@app.route('/start', methods = ['POST','GET'])
def start_form():
        
        if request.method == 'POST':
             session.permanent = False
             session["name"],session["email"],session["gender"],session["is_send"] = request.form['name'],request.form['email'],request.form['gender'],request.form.get('send-chk')
            #  print("GENDER",session['gender'])
             if session['gender'] =='M':
                  dummy['SEX'] =0
             else:
                  dummy['SEX'] =1
                  
             return redirect(url_for("diagnose"))
        else:
            return render_template('formstart.html')




def put_place(colname:str, value:int):
    global all_classes_probab
    dummy[colname]=value
    current = e.all_classes_probab(rf,dummy)
    pos_keys=[]
    neg_keys=[]
    for key in current:
        if current[key] >  all_classes_probab[key]:
            pos_keys.append(key)
        elif current[key] <= all_classes_probab[key]:
            neg_keys.append(key)
    all_classes_probab = copy.deepcopy(current)
    for key in neg_keys:
        id=cond_to_int[key]
        n_neg[id] +=1
    for key in pos_keys:
        id=cond_to_int[key]
        n_pos[id] +=1   
    current={}
    plot_bandits()

def pick():
    symp_set =None
    while symp_set is None:
         picked_bandit = pick_bandit() # Pick disease with the current highest possibility (using beta sampling).
         disease = int_to_cond[picked_bandit] 
         symp_set = cond_to_evi[disease]
         if symp_set:
              break
    print(symp_set)
    enquiry_chosen = None
    while  enquiry_chosen is None or enquiry_chosen in questions_asked:
        enquiry_chosen = random.choice(list(symp_set))
    questions_asked.append(enquiry_chosen) # Choose a random symptom of that disease to enquire about disease.
    cond_to_evi[disease] = symp_set.remove(enquiry_chosen)
    question_data = evids1.loc[enquiry_chosen,["name","question_en",'possible-values','value_meaning']]
    feat_group_classify = lambda enquiry_chosen: 1 if enquiry_chosen in categorical_evi_sc else (0 if enquiry_chosen in binary_evi else ( 3 if enquiry_chosen in multi_evi else 2 )) 
    question_group_val = feat_group_classify(enquiry_chosen)
    return question_data, pmdr.disp(question_group_val, question_data["question_en"],question_data["value_meaning"],question_data["possible-values"]),question_group_val

if __name__ == "__main__":
    app.run(debug=True)