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

def show_change_in_utility(w):
    plt.plot(np.log(w),np.log(erg.change_in_utility(w)))
    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90
    plt.ylabel("Change in utility (log scale)", fontsize=16 )
    plt.xlabel("Wealth (log scale)", fontsize=16 )


if __name__ == "__main__":
    w = np.array(list(map(lambda x: 10.0**x,np.arange(-10,10))) )
    show_change_in_utility(w)
    plt.savefig(name+".pdf",pad_inches =0,transparent =True,frameon=True)
    plt.savefig(name+".png",pad_inches =0,transparent =True,frameon=True,dpi=90)
    bash_cmd = "pdfcrop --margins '0 0 0 0' {0}.pdf {0}.pdf".format(name)
    os.system(bash_cmd)
    
