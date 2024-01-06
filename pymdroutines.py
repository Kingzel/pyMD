import pandas

def populate(empty_df:pandas.DataFrame,populated_df:pandas.DataFrame) -> pandas.DataFrame:
    for i in range(len(populated_df)):
        patient = populated_df.iloc[i]
        age,sex,symps =patient['AGE'],patient['SEX'], patient['EVIDENCES']
        if sex == 'M':
            sex = 0
        elif sex == 'F':
            sex = 1
        empty_df.loc[i, 'AGE'],empty_df.loc[i, 'SEX'] = age,sex
        symps = eval(symps)
        for symp in symps:
            if symp in empty_df.columns:
                empty_df.loc[i, symp] = 1
            else:
                t_index = symp.index('@')-1
                intensity = int(symp[symp.index('@')+2:])
                t_column = symp[0:t_index]
                empty_df.loc[i, t_column] = intensity


    return empty_df

def parse_data(filepaths:list)->list:
 to_return = []
 for path in filepaths:
    extension = path.split('.')[1]
    if extension == 'csv':
        temp_df = pandas.read_csv(path)
    else:
        temp_df = pandas.read_json(path)
    
    x = temp_df.drop(['PATHOLOGY','DIFFERENTIAL_DIAGNOSIS','INITIAL_EVIDENCE'],axis=1,inplace=False)
    y = temp_df['PATHOLOGY']
    to_return.extend([x,y])

 return to_return


def gen_empty(features: list, length:int) -> pandas.DataFrame:
   return pandas.DataFrame(0, index=range(length), columns=features)


def gen_multichoice_features(evids: pandas.DataFrame) -> list:
   evids = transpose_drop(evids)
   m_collection =[]
   m_collection_id =[]
   for i in range(len(evids)):
     if evids.iloc[i]['data_type'] == 'M':
        for each_val in evids.iloc[i]['possible-values']:
            col_name = evids.iloc[i]['name']+"_@_"+each_val
            m_collection.append(col_name)
        m_collection_id.append(evids.iloc[i]['name'])
#    print(m_collection_id)
   return (m_collection,m_collection_id)

def gen_singlechoice_features(evids: pandas.DataFrame)->list:
   evids = transpose_drop(evids)
   c_collection =[]
   ordinal_c = []
   categorical_c = []
   for i in range(len(evids)):
     if evids.iloc[i]['data_type'] == 'C':
        if all(isinstance(each_val,int) for each_val in evids.iloc[i]['possible-values']):
            c_collection.append(evids.iloc[i]['name'])
            ordinal_c.append(evids.iloc[i]['name'])
        else:
            for each_val in evids.iloc[i]['possible-values']:
                col_name = evids.iloc[i]['name']+"_@_"+str(each_val)
                c_collection.append(col_name)
            categorical_c.append(evids.iloc[i]['name'])

   return (c_collection,ordinal_c,categorical_c)


def gen_binary_features(evids: pandas.DataFrame)->list:
   evids = transpose_drop(evids)
   b_collection =[]
   for i in range(len(evids)):
    if evids.iloc[i]['data_type'] == 'B':
        col_name = evids.iloc[i]['name']
        b_collection.append(col_name)
   return b_collection
    

def transpose_drop(evids:pandas.DataFrame)->pandas.DataFrame:
    evids =evids.T
    evids.drop(['question_fr', 'question_en','code_question'], axis=1, inplace=True)
    return evids


def disp(class_val  : int, question_en :str, value_meaning: dict ={}, possible_values :list =[]):
   if class_val == 0: #binary question
      print(question_en)
   elif class_val == 1: #single choice categorical question
      print(question_en)
      for k,i in zip(value_meaning.keys(),value_meaning.items()):
        print(k,i[1]['en'])
   elif class_val == 2: #single choice ordinal question
      print(question_en)
   else: #multi choice question
        for k,i in zip(value_meaning.keys(),value_meaning.items()):
           print(k,i[1]['en'])
