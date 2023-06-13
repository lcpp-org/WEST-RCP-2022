import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
import sys
import re

def plot_iead(filename, dE_eV, w):
    fontsize = 24
    fig = plt.figure(layout='constrained', figsize=(12, 12))
    # widths = [1.5, 1, 1]
    # widths = [1, 1, 1]
    widths = [1.5, 1, 0.8]
    ax = fig.subplots(1, 3, sharey=True, width_ratios=widths)

    Nrows = len(np.genfromtxt(filename[0],delimiter=' '))
    for nn, axis in enumerate(ax):
        axis.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
        axis.set_xticks([0,30,60,90])
        axis.set_xticklabels(['0','30','60','90'])

        if w == 0:
            IEAD = np.concatenate( (np.genfromtxt(filename[3*nn],delimiter=' '),np.genfromtxt(filename[3*nn + 1],delimiter=' '),np.genfromtxt(filename[3*nn + 2],delimiter=' ')),axis = 0 )
            energy = np.concatenate( (np.linspace(0.0, Nrows*dE_eV[3*nn], Nrows),np.linspace(0.0, Nrows*dE_eV[3*nn + 1], Nrows),np.linspace(0.0, Nrows*dE_eV[3*nn + 2], Nrows)),axis = None )
        else:
            IEAD = np.concatenate( (np.genfromtxt(filename[2*nn],delimiter=' '),np.genfromtxt(filename[2*nn + 1],delimiter=' ')),axis = 0 )
            energy = np.concatenate( (np.linspace(0.0, Nrows*dE_eV[2*nn], Nrows),np.linspace(0.0, Nrows*dE_eV[2*nn + 1], Nrows)),axis = None )
            
        # assume there will always be 90 angles and 90 angle bins
        angles = np.linspace(0,90,90)

        E,A = np.meshgrid(angles,energy)
        IEAD = np.log10(IEAD)

        cmap_jet = mpl.colormaps['jet'].resampled(25)
        # cmap_jet = plt.cm.get_cmap('jet',25)
        colors = list(cmap_jet(np.arange(25)))
        
        #replace first color with white
        colors[0] = "white"
        cmap = mpl.colors.ListedColormap(colors[:-1], "")
        CS = axis.contourf(E,A,IEAD,cmap = cmap,levels=25,vmin=11)
        
        if nn == 0: # Sample 1
            axis.set_ylabel('Energy [eV]',fontsize = fontsize)
            axis.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
            axis.set_ylim((0,450))
            if w == 0: # With Oxygen
                axis.text(30, 125, r'He$^{++}$', fontsize=fontsize)
                axis.text(30, 60, r'He$^{+}$', fontsize=fontsize)
                axis.text(15, 400, r'O$^{8+}$', fontsize=fontsize)
            else: # Without Oxygen
                axis.text(30, 125, r'He$^{++}$', fontsize=fontsize)
                axis.text(30, 60, r'He$^{+}$', fontsize=fontsize)
        elif nn == 1: # Sample 2
            axis.set_xlabel('Angle [deg]',fontsize = fontsize)
            if w == 0: # With Oxygen
                axis.text(25, 60, r'He$^{++}$', fontsize=fontsize)
                axis.text(30, 30, r'He$^{+}$', fontsize=fontsize)
                axis.text(7, 170, r'O$^{8+}$', fontsize=fontsize)
            else: # Without Oxygen
                axis.text(20, 60, r'He$^{++}$', fontsize=fontsize)
                axis.text(27, 30, r'He$^{+}$', fontsize=fontsize)
        else: # Sample 3
            if w == 0: # With Oxygen
                axis.text(20, 25, r'He$^{++}$', fontsize=fontsize)
                axis.text(40, 10, r'He$^{+}$', fontsize=fontsize)
                axis.text(5, 80, r'O$^{8+}$', fontsize=fontsize)
            else: # Without Oxygen
                axis.text(25, 30, r'He$^{++}$', fontsize=fontsize)
                axis.text(50, 10, r'He$^{+}$', fontsize=fontsize)

    if w == 0:
        plt.savefig('IEAD_w_Ox.png')
    else:
        plt.savefig('IEAD_wo_Ox.png')

def main():
    for w in range(2):
        # w = 0 is with oxygen and w = 1 is without oxygen
        filename = []
        dE_eV = []
        index = 0
        
        for i in range(1,4):
            if w == 0:
                directory = 'Sample_'+str(i)+'_w_Ox'
            else:
                directory = 'Sample_'+str(i)+'_wo_Ox'
        
            for files in os.listdir(directory):
                #f = os.path.join(directory, files)
                f = str(directory)+'/'+str(files)
                # checking if it is a file
                if os.path.isfile(f):
                    filename.append(f)

                filename_pattern = pat = re.compile(
                    '^.*\/(.*)_dE_eV_([0-9\.]+)_(.*)_t[0-9]{7}.dat$')

                m = filename_pattern.match(filename[index])
                if not m:
                    print('ERROR: failed to extract necessary energy bin information from'
                        + f' IEAD file {filename[index]}. Expected to find "dE_eV_#####" in filename.')
                    sys.exit(1)

                groups = m.groups()
                dE_eV.append(float(groups[1]))
            
                index = index + 1
        plot_iead(filename, dE_eV, w)

if __name__ == '__main__':
    print(sys.version)
    main()
