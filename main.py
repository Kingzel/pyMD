import pymdroutines as pmdr
import pandas as pd
import evaluate as e
import random as rand
import pickle as p
import thompsonsampling as ts
import os 

os.system('cls')
evids =pd.read_json("data\\release_evidences.json")
evids1 = pd.read_json("data\\release_evidences.json")
conds  = pd.read_json('data\\release_conditions.json')
evids1 = evids1.T


conds = conds.T
conds.drop(['cond-name-fr', 'antecedents','cond-name-eng','icd10-id'], axis=1, inplace=True)


cond_to_evi = {}
int_to_cond ={}
for i in range(len(conds)):
   condition=  conds.iloc[i]
   name =condition['condition_name']
   cond_to_evi[name] = set(condition['symptoms'].keys())
   int_to_cond[i]=name



with open('trained_model.bin', 'rb') as f:
    rf =  p.load(f)
    cols  = p.load(f)

multi_evi = pmdr.gen_multichoice_features(evids,'M')
ordinal_evi_sc= pmdr.gen_singlechoice_features(evids,'MO')
categorical_evi_sc = pmdr.gen_singlechoice_features(evids,'MC')
binary_evi =pmdr.gen_binary_features(evids)

ts.gen_arrays(len(conds))
def pick():
    picked_bandit = ts.pick_bandit() # Pick disease with the current highest possibility (using beta sampling).
    disease = int_to_cond[picked_bandit] 
    symp_set = cond_to_evi[disease]
    enquiry_chosen = rand.choice(list(symp_set)) # Choose a random symptom of that disease to enquire about disease.

    question_data = evids1.loc[enquiry_chosen,["name","question_en",'possible-values','value_meaning']]
    feat_group_classify = lambda enquiry_chosen: 1 if enquiry_chosen in categorical_evi_sc else (0 if enquiry_chosen in binary_evi else ( 3 if enquiry_chosen in multi_evi else 2 )) 
    question_group_val = feat_group_classify(enquiry_chosen)
    return question_data,pmdr.disp(question_group_val, question_data["question_en"],question_data["value_meaning"],question_data["possible-values"]),question_group_val

dummy= pmdr.gen_empty(cols,1)
all_classes_probab =  e.all_classes_probab(rf,dummy)

def put_place(colname:str, value:int):
    dummy[colname]=value
    current = e.all_classes_probab(rf,dummy)
    keys=[]
    for key in current:
        print(key,":",current[key],all_classes_probab[key],current[key]==all_classes_probab[key])
    for key in current:
        if current[key] > all_classes_probab[key]:
            keys.append(key)
    all_classes_probab = current
    return keys,len(keys)


