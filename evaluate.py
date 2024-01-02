import operator
import pandas as pd
def all_classes_probab(model,dataFrame: pd.DataFrame) -> dict:
    y_probabs = model.predict_proba(dataFrame)
    zipped = zip(model.classes_,y_probabs.tolist()[0])
    prob_to_label ={}
    for disease,probab in zipped:
        prob_to_label[disease] = probab
    prob_to_label = dict( sorted(prob_to_label.items(), key=operator.itemgetter(1), reverse=True))
    return prob_to_label

def get_most_confident_class(model,dataFrame: pd.DataFrame) -> tuple:
    output_dict = all_classes_probab(model,dataFrame)
    max_key = max(output_dict, key=lambda k: output_dict[k])
    return (max_key,output_dict[max_key])
