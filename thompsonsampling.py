import numpy as nump
import os as o
import matplotlib.pyplot as plt
from scipy.stats import beta



o.system('cls')

d = 49
nPosRew = nump.zeros(d)
nNegRew= nump.zeros(d)

def pick_bandit():
    iter_max =0
    for j in range(d):
        randBeta =  nump.random.beta(nPosRew[j]+1,nNegRew[j]+1)
        # print(j+1," presented with a proabability ",randBeta)
        if iter_max < randBeta:
            iter_max = randBeta
            selected = j
    return selected
         
#     print("Selected: ", selected+1)

#     if SlotData[i] [selected] == 1:
#         nPosRew[selected] +=1
#     else:
#         nNegRew[selected]+=1
#     clist = ['red','green','blue','cyan','magenta']
#     # for j in range(d):
#     #     x = nump.linspace(0,1,200)
#     #     y= beta.pdf(x,nPosRew[j],nNegRew[j])
#     #     plt.plot(x,y,color = clist[j])
#     #     plt.xlabel("Estimated Probability")
#     #     plt.ylabel("Probability")
#     #     plt.title("Beta Distribution")
        
#     #     nSelected = nPosRew[j]+nNegRew[j]
#     #     print( j+1," was selected ",nSelected)
#     #     print()
#     #     print()
#     # plt.show()
    
   
# clist = ['red','green','blue','cyan','magenta']
# for j in range(d):
#     x = nump.linspace(0,1,200)
#     y= beta.pdf(x,nPosRew[j],nNegRew[j])
#     plt.plot(x,y,color = clist[j])
#     plt.xlabel("Estimated Probability")
#     plt.ylabel("Probability")
#     plt.title("Beta Distribution")
    
#     nSelected = nPosRew[j]+nNegRew[j]
#     print( j+1," was selected ",nSelected)
#     print()
#     print()
# plt.show()
