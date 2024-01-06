import numpy as nump
import os as o
import matplotlib.pyplot as plt
from scipy.stats import beta



o.system('cls')

d = 49

n_pos = nump.zeros(d)
n_neg= nump.zeros(d)

def pick_bandit(d):
    iter_max =0
    for j in range(d):
        sampled_beta =  nump.random.beta(n_pos[j]+1,n_neg[j]+1)
        if iter_max < sampled_beta:
            iter_max = sampled_beta
            selected = j
    return selected
         
