import os
name = os.path.basename(__file__).split(".py")[0]
import matplotlib.pyplot as plt
##########
import sys
import numpy as np
sys.path.append('..')
import ergodicity as erg
#from importlib import reload  # Python 3.4+ only.
#reload(ergodicity)

def show_utility(w):
    """
    w = np.arange(-10,10,step=0.1) 
    show_utility(w)
    np.log(10**-10)
    """
    plt.plot(w,(erg.utility(w)))
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    plt.ylabel("Utility", fontsize=16 )
    plt.xlabel("Wealth", fontsize=16 )



if __name__ == "__main__":
    w = np.arange(-10,10,step=0.1) 
    show_utility(w)
    plt.savefig(name+".pdf",pad_inches =0,transparent =True,frameon=True)
    plt.savefig(name+".png",pad_inches =0,transparent =True,frameon=True,dpi=90)
    bash_cmd = "pdfcrop --margins '0 0 0 0' {0}.pdf {0}.pdf".format(name)
    os.system(bash_cmd)
    
