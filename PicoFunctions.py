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

import matplotlib
matplotlib.use('TkAgg')


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

goal=17500

def noisefn(adc,Bin):
    s1=adc/65535
    s2=s1*(np.tanh(0.01*(Bin-150))+1)+np.cos(2*np.pi*Bin/3.5)**2+np.pi*(Bin+13)**-3.2+3*np.cos(Bin)**2
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
    anim_running=True
    def onClick(evn):
        nonlocal anim_running
        if anim_running:
            ani.event_source.stop()
            anim_running = False
        else:
            ani.event_source.start()
            anim_running = True
        
    
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
            ax[2].fill_between(track,-310,110,color='green')
        except:
            IndexError

        return line,diff,track
    fig.canvas.mpl_connect('button_press_event', onClick)
    ani=animation.FuncAnimation(fig,animate,interval=300,save_count=0,frames=len(PicoList[1]),repeat=False)
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
    ax[2].set_ylim(-310,110)
    
    plt.tight_layout()
    os.system('cls')

    return ani
