# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 12:57:08 2023

@author: jt16596
"""

import os
import imageio as iio
from matplotlib import pyplot as plt
from scipy import signal as sig
import numpy as np
import pandas as pd
import matplotlib.animation as animation
import random
# import Tkinter
# import tkMessageBox

def readin(file,PicoList,Bin):
    pico=np.array(pd.read_csv(file))
    for i in pico:
        PicoList.append(np.array(noisefn(i,Bin)))
    return np.array(PicoList),pico

def spectrum():
    data=pd.read_csv('Spectrum.txt',delimiter='	')
    Bin=data['Bin']
    Cr=data['Cr']/np.amax(data['Cr'])
    return Bin,Cr

goal=18000

def noisefn(adc,Bin):
    s1=adc/65535
    s2=s1*(np.tanh(0.01*(Bin-150))+1)+np.cos(2*np.pi*Bin/3.5)**2
    return s2


def main(file):
    PicoList=[]
    global X,Y,track,checkvar
    X=[]
    Y=[]
    track=[]
    checkvar=0
    Bin,Cr=spectrum()
    PicoList=readin(file,PicoList,Bin)
    Mixed=np.array(Cr*noisefn(goal,Bin)+noisefn(goal,Bin))
    fig,ax=plt.subplots(3)
    fig.set_figheight(8)
    fig.set_figwidth(12)
    line,=ax[1].plot(Bin,Mixed,drawstyle='steps-post',color='blue')
    diff,=ax[2].plot([],[],drawstyle='steps-post',color='k',marker='o')
    X,Y=[],[]
    ax[2].set_ylim(-100,100)
    ax[2].set_xlim(np.amin(PicoList[1]),np.amax(PicoList[1]))

    # def restart():
    #     root=Tkinter.Tk()
    #     root.withdraw()
    #     result=tkMessageBox.askyesno("Restart?","Would you like to restart animation?")
    #     if result:
    #         ani.frame_seq=ani.new_frame_seq()
    #         ani.event_source.start()
    #     else:
    #         plt.close()
    def animate(i):
        
        newy=(Mixed-PicoList[0][i])/PicoList[0][i]
        newymin,newymax=np.amin(newy),np.amax(newy)
        line.set_ydata(newy)
        ax[1].set_title('Noisy signal - Potentiometer ADC: '+str(PicoList[1][i][0]))
        ax[1].set_ylim(0.9*newymin,1.1*newymax)
        dx=PicoList[1][i]
        dy=100*(goal-PicoList[1][i])/goal
        X.append(dx)
        Y.append(dy)
        diff.set_data(X,Y)
        
        checkvar=np.abs(PicoList[1][i][0]-goal)
        if checkvar<=500:
            track.append(PicoList[1][i][0])
        try:
            ax[2].fill_between(track,-100,100,color='green')
            for i in np.arange(0,len(track)):
                ax[2].text(track[i], 80+10*(-1)**i,track[i])
        except:
            IndexError
        # if i==len(PicoList[0]):
        #     restart()
        return line,diff,track
    ani=animation.FuncAnimation(fig,animate,interval=20,save_count=0,frames=len(PicoList[1]),repeat=False)

    ax[0].plot(Bin,Cr,color='r',drawstyle='steps-post')
    ax[0].set_title('Desired Signal')
    ax[0].set_xlabel('Pulse Height (ADC counts)')
    ax[0].set_ylabel('Count rate')
    ax[0].set_xlim(0,400)
    ax[1].set_xlim(0,400)
    ax[1].set_ylabel('Count rate')
    ax[1].set_xlabel('Pulse Height (ADC counts)')
    ax[2].set_ylabel('Percentage difference ')
    ax[2].set_xlabel('Potentiometer voltage (ADC counts)')
    ax[2].set_title('Percentage difference between measured ADC and desired ADC')
    ax[2].set_ylim(-100,100)

    plt.tight_layout()
    os.system('cls')
    

    return ani