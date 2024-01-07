import numpy as nump
import matplotlib.pyplot as plt
from scipy.stats import beta



n_pos = 0
n_neg= 0

def pick_bandit():
    iter_max =0
    for j in range(len(n_neg)):
        sampled_beta =  nump.random.beta(n_pos[j]+1,n_neg[j]+1)
        if iter_max < sampled_beta:
            iter_max = sampled_beta
            selected = j
    return selected
         
def gen_arrays(d:int):
    global n_neg
    global n_pos
    n_pos =nump.zeros(d)
    n_neg=nump.zeros(d)