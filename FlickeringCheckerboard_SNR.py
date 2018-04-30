# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 10:30:23 2018

@author: Batuhan Erkat
"""
from operator import add
import random
import csv
import matplotlib.pyplot as plt
from psychopy import visual, event, core

#Display
disp = visual.Window(size=(1920, 1080),
                     fullscr=True,
                     monitor="Umram",
                     units="deg",
                     checkTiming=True)

# Stimulus Parameters
globalsize = (3, 3) # OBE - 4, 4
fixationsize = (0.1, 0.1) # OBE - 0.2, 0.2
posleft = (5, 0) # OBE 6, -6
posright = (-5, 0)
spatialfrequency = 1
disp.setRecordFrameIntervals(True)
frameint = disp.frameIntervals
disp.nDroppedFrames

#disp._refreshThreshold = 1/60 + 0.004

# Fixation point
fixation = visual.GratingStim(disp,
                              mask="circle",
                              size=fixationsize,
                              color="black")

# Make two radial or grating stim (in opposite colors) and alternate them for flashing effect

# Checkerboard stimuli
stim1 = visual.GratingStim(disp,
                           tex="sqrXsqr",
                           mask="circle",
                           pos=posleft,
                           size=globalsize, # size = (x,y) coordinates, 
                           sf=spatialfrequency,
                           color=(1, 1, 1))
stim2 = visual.GratingStim(disp,
                           tex="sqrXsqr",
                           mask="circle",
                           pos=posleft,
                           size=globalsize,
                           sf=spatialfrequency,
                           color=(-1, -1, -1))
stim3 = visual.GratingStim(disp,
                           tex="sqrXsqr",
                           mask="circle",
                           pos=posright,
                           size=globalsize,
                           sf=spatialfrequency,
                           color=(1, 1, 1))
stim4 = visual.GratingStim(disp,
                           tex="sqrXsqr",
                           mask="circle",
                           pos=posright,
                           size=globalsize,
                           sf=spatialfrequency,
                           color=(-1, -1, -1))

# Radial stimuli, comment the checkerboard, uncomment this if needed.
#stim1 = visual.RadialStim(disp,
#                          tex="sqrXsqr",
#                          radialCycles=4,
#                          angularCycles=6,
#                          size=globalsize,
#                          pos=posleft,
#                          color=(1,1,1)
#                          )
#stim2 = visual.RadialStim(disp,
#                          tex="sqrXsqr",
#                          radialCycles=4,
#                          angularCycles=6,
#                          size=globalsize,
#                          pos=posleft,
#                          color=(-1,-1,-1)
#                          )
#stim3 = visual.RadialStim(disp,
#                          tex="sqrXsqr",
#                          radialCycles=4,
#                          angularCycles=6,
#                          size=globalsize,
#                          pos=posright,
#                          color=(1,1,1)
#                          )
#stim4 = visual.RadialStim(disp,
#                          tex="sqrXsqr",
#                          radialCycles=4,
#                          angularCycles=6,
#                          size=globalsize,
#                          pos=posright,
#                          color=(-1,-1,-1)
#                          )

#Experimental Parameters
colorlist = ["red", "yellow"] # Fixation coloring
refreshrate = 0.06  # 60Hz, 60 frames in 1 second. 16.667 ms
TR = 2000 #mseconds
TRframes = int(TR*refreshrate) # 2*60 = 120 frames
trialduration = int(0.5*TRframes) # Fixation color change once in every x*TR
blocksize = 6
currentTR = 0
lastTR = 10 # Number of measurements
totalframes = lastTR*TRframes
totaltrials = totalframes/trialduration
i = 0 # List's first element, used for incrementing

## Random list generation
# Picks random colors for fixation.
randomcolors = []
for x in range(1, (totaltrials)+5):
    x = random.choice(colorlist)
    randomcolors.append(x)

# Picks random durations for fixation color change, between 100 - 200 ms.
frameinms = 1.00/60 # ~0.01667
framedur100ms = int(0.100/frameinms) # 0.10 = 100 ms; 0.20 = 200 ms
framedur200ms = int(0.200/frameinms) # 0.10 = 100 ms; 0.20 = 200 ms
randomdurations = []
for x in range(1, (totaltrials)+5):
    x = random.choice(range(framedur100ms, framedur200ms+1))
    randomdurations.append(x)

# Picks random frames for fixation color change start. Change it with for loop, restrain the upper threshold with duration.
randomframesnonscaled = []
for x in range(1, (totaltrials)+5):
    x = random.choice(range(1, trialduration-max(randomdurations)-int(framedur200ms)+1)) # To prevent consequtive color switchs before turning back to black, I substract the max random duration (11 in this case) and another max duration (12) from the total trial duration (138 here)
    randomframesnonscaled.append(x)
scalinglist = (range(0, (totalframes+3*trialduration)+1, (trialduration)))
randomframes = map(add, randomframesnonscaled, scalinglist)

# Calculates the color ending frames
z = 0
colorendframes = []
for x in randomframes:
    colorendframe = randomframes[z]+randomdurations[z]
    z += 1
    colorendframes.append(colorendframe)


#Some more parameters before experiment
responselist = []
#triggerlist = []
flickercycle = 0.125 # 1 cycle in 0.xx seconds
hzpersecond = 1.00/flickercycle
framecounter = 0

##Experiment
if event.waitKeys(keyList=["6"]):
    Clock = core.Clock()
    timestart = core.getTime()

    #Initial and further parameter update loop:     
    for f in range(1, totalframes+1):
        keys = event.getKeys(keyList=["1","2","3","4"], timeStamped=Clock)
#        triggers = event.getKeys(keyList=["6"], timeStamped=Clock)
        if f%trialduration == 1: #When f hits to 1, updates the current trial, and takes relevant list elements.
            randomcolor = randomcolors[i] #Better replace with a function, remaining frames need to be specified with a trial even though they may not be used.
            randomframe = randomframes[i]
            randomduration = randomdurations[i]
            colorendframe = colorendframes[i]
            i += 1 #Put it last so that new i is not expressed in random.. variables until next iteration.
        if f%TRframes == 1: #When f hits to 1, updates the currentTR value.
            currentTR += 1
        
        #Draws blank block stimuli
        if currentTR%(2*blocksize) < blocksize:
            if f == randomframe:
                fixation.color = randomcolor
            elif f == colorendframe:
                fixation.color = "black"
            if True:
                fixation.draw()
                disp.flip()
                framecounter += 1

        #Draws experimental block stimuli
        elif currentTR%(2*blocksize) >= blocksize:
            t = Clock.getTime()
            if f == randomframe:
                fixation.color = randomcolor
            elif f == colorendframe:
                fixation.color = "black"
            if (t%flickercycle) < (flickercycle/2.0):
                stim1.draw()
                stim3.draw()
                fixation.draw()
                disp.flip()
                framecounter += 1
            elif (t%flickercycle) >= (flickercycle/2.0):
                stim2.draw()
                stim4.draw()
                fixation.draw()
                disp.flip()
                framecounter += 1
        for key in keys:
            responselist.append(key)
#        for trigger in triggers:
#            triggerlist.append(trigger)
    
    timeend = core.getTime()
    timepassed = timeend-timestart

#Close
disp.close()
plt.plot(disp.frameIntervals)
plt.show()

#meanframeint = sum(frameint)/float(len(frameint))
#print 'Overall, %i frames were dropped.' % disp.nDroppedFrames

myfile = "C:\Users\Batuhan Erkat\Desktop\Bilkent\SNR Comparison Stimulus\ExperimentData.csv"

# Here I insert the names of the lists as the fisrt element so the csv is more understandable.
randomdurations.insert(0, "Randomduration")
randomframes.insert(0, "Randomframes")
randomcolors.insert(0, "Randomcolors")
colorendframes.insert(0, "Colorendframes")
responselist.insert(0, "Responses")
#triggerlist.insert(0, "Triggers")

# File wiriting part, it needs edit
rows = zip(randomdurations, randomframes, randomcolors, colorendframes, responselist) #, triggerlist)

with open(myfile, "wb") as file:
    writer = csv.writer(file)
    for row in rows:
        writer.writerow(row)
