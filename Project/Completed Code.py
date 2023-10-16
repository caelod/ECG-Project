import os #allows to create a directory and fetch its contents 
import numpy as np #allows use of mathemathical numpy functions
import tkinter #allows creation of GUIs

from tkinter import * #imports all functions from the library and allows user to open the file directory 
from tkinter import filedialog
from matplotlib import * #imports all functions from the library and allows user to plot a graph

from matplotlib.figure import Figure #imports the figure module from the matplotlib library
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) #allows setting of a backend for the figure to render the figure
from scipy.signal import find_peaks #import find_peaks from scipy.signal to be able to use the function to find peaks

# plot function is created for plotting the graph in the tkinter window
def plot():
    # the figure that will contain the plot
    fig = Figure(figsize = (6, 6),dpi = 100) #sets figure size as well as dots per inches which determines how many pixels the figure comprises.
    
    root = tkinter.Tk() #displays the root window and manages all other tkinter components
    root.withdraw() #removes the window from the screen without destroying it
    currdir = os.getcwd() #gets current working directory
    PathECG = filedialog.askopenfilename(parent=root, initialdir = currdir, title = 'Please select ECG .txt file.' ) #creates a file path which prompts the user to select a file
    filename = os.path.basename(PathECG) #used to get the basename in the specified path
    cardiac = np.loadtxt(PathECG , skiprows=1, usecols=[3,4]) #loads the data from the text file and assigns it to a value
    
    ecgtime = cardiac[:,0] #keeps all rows but only the first column and assigns these values as ecgtime
    ecgmV = cardiac[:,1] #keeps all rows but only the second column and assigns these values as ecgmV
    
    ecgtime_list = ecgtime.tolist()#Converting ecgtime to a list
    
    
    
    
    # adding the subplot
    plot1 = fig.add_subplot(211) #2x1 grid, 1st subplot
    plot2 = fig.add_subplot(212) #2x1 grid, 2nd subplot
    
    # plotting the fitst graph
    plot1.plot(ecgtime,ecgmV, linewidth = 1, color='green') #plots the first graph, changes width and colour of line
    plot1.set_title(filename) #sets the title as the name of the text file used
    plot1.set_xlabel("Time (sec)") #sets ylabel
    plot1.set_ylabel("Voltage (mV)") #sets xlabel
    plot1.grid() #displays a grid formation on the graph
    
    
    max_value = np.max(ecgmV) #Find max value from data
    thresholdmax = max_value * 0.75 #Set threshold of upper values to find peaks
    print("Threshold of max values", thresholdmax) # Print threshold
    peakR, _ = find_peaks(ecgmV, height=thresholdmax) #Find peaks from data above the threshold set
    peaksR = ecgmV[peakR] #Xaxis vlues were assigned to Yaxis values
    print("R peaks values=", peaksR)
    time_peakR = ecgtime[peakR] #the time value matching to the x axis being used in conjunction to find the R Peaks.
    print("Time of R peaks=", time_peakR) #Printing the times of the peak values
    

    
    cardiac_cyclesR = np.size(time_peakR) - 1 #Finding cardiac cycle by findindg how many peaks there was in data and taking away 1 to find number of cycles
    time_for_cyclesR = (time_peakR[-1] - time_peakR[0]) #Finding time between first cycle and last cycle
    print(time_for_cyclesR) #Printing the time of all cycles
    time_for_one_peakR = time_for_cyclesR / cardiac_cyclesR #Calculating the time of one cycle by dividing the size of cycles into the time taken for all cycles
    print("Time for one cardiac cycle", time_for_one_peakR) #Print time for one cycle
    BPM = 60 / time_for_one_peakR #Calculate heart rate per minute
    print(BPM)
    if BPM >= 60 and BPM <= 100: #Use if statement to assign 'Normal sinus' to 'condition' when BPM is graeater then equal to 60 and less then equal to 100
        condition = "Normal Sinus"
    elif BPM < 60: #Use elif statment to assign 'Bradycardia' to 'condition' when BPM is less then 60
        condition = "Bradycardia"
    else: #Use else statement to assign 'Tachycardia' to 'condition' if both above statment not true
        condition = "Tachycardia"
    
    #Finding S troughs
    limitS = time_for_one_peakR * 0.15 #Setting limits
    limitS = round(limitS, 2) #Rounding limits to 2 decimal places
    print("limit S", limitS) #print limit
    endS =[] #Declering a list
    locationSS = [] #Declering a list
    time_peakS = [] #Declering a list
    for i in time_peakR[1::]: #In a loop look at values of R peaks
        x = i + limitS #Add limit time to R peak to find end of section value
        x = round(x, 2) #Round to 2 decimal places
        endS.append(x) #Add all values to variable endS
        indexSS = ecgtime_list.index(i)  #Find location of R peaks in the dataset
        locationSS.append(indexSS)#Add all locations of R peaks to a variable called locationSS (the section starts at this location)
    print("Starting location for sections of S peak =", locationSS) #Print start location of S section
    locationSE = [] #Declare a list
    peakS = [] #Declare a list
    peakSL= [] #Declare a list
    min_xS =[] #Declare a list
    for i in endS: #In a loop look at all end of section values
        indexSE = ecgtime_list.index(i) #Find all locations of the end of section vlaues
        locationSE.append(indexSE) #Add all locations to a variable locationSE
    print("End location of sections of S peak =", locationSE) #Print end location of S section
    for i in range(0, len(locationSS)):#In a loop that runs for the amount of how many starting sections vlaues there is
        sectionS = ecgmV[locationSS[i]:locationSE[i]] #Looking at all values in seperate sections of the graph based on the R peaks and end value set by the limit
        min_yS = min(sectionS) #Find minimum vlaue of the section
        min_xS = np.argmax(sectionS) #Look for the location of min_yS in each section
        xaxisS = min_xS + locationSS[i] #Add starting location value to the location vlaue of min_yS in each section
        peakSL.append(xaxisS) #Add all xaxisS values to peakSL variable (Location of S peak)
        peakS.append(min_yS) #Add all min_yS values to peakS (Value of S peak )
    time_peakS =  ecgtime[peakSL] #The Xaxis values were assigned to appropriate time value from data
    print("S peak values=", peakS) #Print S peak values

    #Finding T peak
    limitT = time_for_one_peakR * 0.35 #Setting limits
    limitT = round(limitT, 2) #Round limits
    print("limit T", limitT) #print limit
    endT =[] #Declering a list
    locationTS = [] #Declering a list
    time_peakT = [] #Declering a list
    for i in time_peakS[0::]: #In a loop look at values of S trophs
        x = i + limitT #Add limit time to S troph to find end of section value
        x = round(x, 3) #Round to 3 decimal places
        endT.append(x) #Add all values to variable endT
        indexTS = ecgtime_list.index(i+0.10)  #Find location of starting of the section value
        locationTS.append(indexTS)#Add all locations of staring of the section value to a variable called locationTS (the section starts at this location)
    print("Starting location for sections of T peak =", locationTS) #Print starting locations of T sections
    locationTE = [] #Declare a list
    peakT = [] #Declare a list
    peakTL= [] #Declare a list
    max_xT =[] #Declare a list
    for i in endT: #In a loop look at all end of section values
        indexTE = ecgtime_list.index(i) #Find all locations of the vlaues
        locationTE.append(indexTE) #Add all locations to a variable locationTE
    print("End location of sections of T peak =", locationTE) #Print end of sections values
    for i in range(0, len(locationTS)):#In a loop that runs for the amount of how many starting sections vlaues there is
        sectionT = ecgmV[locationTS[i]:locationTE[i]] #Looking at all values in seperate sections of the graph based on the S peaks and end value set by the limit
        max_yT = max(sectionT) #Find maximum vlaue of the section
        max_xT = np.argmax(sectionT) #Find location of the maximum in each section
        xaxisT = max_xT + locationTS[i] #Add starting of the section vlaue to the maximum value location in each section to find the location of the vlaue in the ecgmV
        peakTL.append(xaxisT) #Add all xaxisT values to peakTL variable (Location of T peak)
        peakT.append(max_yT) #Add all max_yT values to peakT (Value of T peak )
    time_peakT =  ecgtime[peakTL] #The XaxisT values were assigned to appropriate time value from data
    print("T peak values=", peakT) #Print T peak vlaues

    #Finding Q peak
    limitQ = time_for_one_peakR * 0.20 #Setting limits
    limitQ = round(limitQ, 2) #Round limits
    print("limit Q", limitQ) #print limit
    startQ =[] #Declering a list
    locationQE = [] #Declering a list
    time_peakQ = [] #Declering a list
    for i in time_peakR[1::]: #In a loop look at values of R peaks
        x = i - limitQ #Take away limit time to R peak values to find staritng of section value
        x = round(x, 2) #Round to 2 decimal places
        startQ.append(x) #Add all values to variable startQ
        indexQE = ecgtime_list.index(i-0.005)  #Find location of the end section vlaue
        locationQE.append(indexQE)#Add all locations of end location vlaue  to a variable called locationQE (the section ends at this location)
    print("End location for sections of Q peak =", locationQE) #Print end location of section Q
    locationQS = [] #Declare a list
    peakQ = [] #Declare a list
    peakQL= [] #Declare a list
    max_xQ =[] #Declare a list
    for i in startQ: #In a loop look at all end of section values
        indexQS = ecgtime_list.index(i) #Find all locations of the vlaues
        locationQS.append(indexQS) #Add all locations to a variable locationTE
    print("Startng location of sections of Q peak =", locationQS) #Print starting location of the Q section
    for i in range(0, len(locationQS)):#In a loop that runs for the amount of how many starting sections vlaues there is
        sectionQ = ecgmV[locationQS[i]:locationQE[i]] #Looking at all values in seperate sections of the graph based on the R peak and end value set by the limit
        min_yQ = min(sectionQ) #Find minimum vlaue of section
        min_xQ = np.argmax(sectionQ) #Find location of min_yQ in the section
        xaxisQ = min_xQ + locationQS[i] #Add starting location of each section to the location of min_yQ
        peakQL.append(xaxisQ) #Add all xaxisQ values to peakQL variable (Location of Q peak)
        peakQ.append(min_yQ) #Add all max_yQ values to peakQ (Value of Q peak )
    time_peakQ =  ecgtime[peakQL] #The XaxisQ values were assigned to appropriate time value from data
    print("Q peak values=", peakQ) #Print Q peak vlaues

    limitP = time_for_one_peakR * 0.26 #Setting limits
    limitP = round(limitP, 2) #Rounding the limits
    print("limit P", limitP) #print limit
    startP =[] #Declering a list
    locationPE = [] #Declering a list
    time_peakP = [] #Declaring a list
    for i in time_peakQ[0::]: #In a loop look at values of Q peaks
        x = i - limitP #Take away limit time to Q peaks to find staritng vlaue of section value
        x = round(x, 3) #Round to 2 decimal places
        startP.append(x) #Add all values to variable startP
        indexPE = ecgtime_list.index(i-0.02)  #Find location of the end location vlaue
        locationPE.append(indexPE)#Add all locations end location values to a variable called locationPE (the section end at this location)
    print("End location for sections of P peak =", locationPE) #Print end location vlaues
    locationPS = [] #Declare a list
    peakP = [] #Declare a list
    peakPL= [] #Declare a list
    max_xP =[] #Declare a list
    for i in startP: #In a loop look at all end of section values
        indexPS = ecgtime_list.index(i) #Find all locations of the vlaues
        locationPS.append(indexPS) #Add all locations to a variable locationTE
    print("Starting location of sections of P peak =", locationPS) #Print start location
    for i in range(0, len(locationPS)):#In a loop that runs for the amount of how many starting sections vlaues there is
        sectionP = ecgmV[locationPS[i]:locationPE[i]] #Looking at all values in seperate sections of the graph based on the Q peaks and end value set by the limit
        max_yP = max(sectionP) #Find maximum value of sections
        max_xP = np.argmax(sectionP) #Find location of maximum value in the section
        xaxisP = max_xP + locationPS[i] #Add starting of section vlaue
        peakPL.append(xaxisP) #Add all xaxisP values to peakPL variable (Location of P peak)
        peakP.append(max_yP) #Add all max_yP values to peakP (Value of P peak )
    time_peakP =  ecgtime[peakPL] #The Xaxis values were assigned to appropriate time value from data
    print("P peak values=", peakP) #Print P peak vlues



    plot2.plot(ecgmV) #plots the second graph
    plot2.plot(peakR, peaksR, "X", linewidth = 1, color='red')
    plot2.plot(peakSL, peakS, "X")
    plot2.plot(peakTL, peakT, "X")
    plot2.plot(peakQL, peakQ, "X", color='purple')
    plot2.plot(peakPL, peakP, "X", color='yellow')
    plot2.set_xlabel("Location in ECG Time")
    plot2.set_ylabel("Voltage (mV)")
    plot2.grid()
    fig.tight_layout() #adjusts subplots to fit in the figure neatly

    #AV block
    AVblock = time_peakR[1::] - time_peakP #Calculating PR intrevals
    for i in AVblock: #In a loop look at each PR intreval for each section
        if i > 0.20: #If PR intreval is greater then 20 AV block is present
            AVp= "Present"
        else: #If PR intreval is less then equal to 20 AV block is absent
            AVp= "Absent"
    
    #QT intreval
    QTintreval = time_peakT[0::] - time_peakQ #Calculate QT intreval
    QTc = QTintreval/time_for_one_peakR #Calculate if QT intreval is normal
    for i in QTc: #In a loop of each QTc intreval
        if i <= 0.42: #If intreval is smaller then 0.42s, intreval is normal
            QTp="Normal"
        else: #If intreval is bigger then 0.42s, intreval is not normal
            QTp="Abnormal"

    textstr = '\n'.join(( #takes all elements and joins them into a single string
    r'BPM =  %.2f' % (BPM, ), #% = special character, 2 = 2 characters, F = float
    r'Condition =  %.12s' % (condition, ), #12 characters, string
    r'AV =  %.7s' % (AVp, ),
    r'QTc =  %.10s' % (QTp, )))
    
    
    props= dict(boxstyle='square', facecolor='wheat', alpha=0.75) #creates a dictionary for the bounding box
    plot1.text(0.70, 0.95, textstr, fontsize = 8 , transform=plot1.transAxes, verticalalignment = 'top', bbox = props) #plots text in the bounding box
   
    #creats the Tkinter canvas
    #contains the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,master = window)
    canvas.draw()
    
    #places the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    
    #creats the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    
    #placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()
    

#the main Tkinter window
window = Tk()

#sets the title
window.title('Plotting in Tkinter')

#dimensions of the main window
window.geometry("600x600")
window.configure(bg="white")

#button that displays the plot
plot_button = Button(master = window,
					command = plot,
					height = 2,
					width = 10,
					text = "Analyse ECG",
                    fg= "black", #foreground colour
                    bg="white") #background colour

#packs button which places it
plot_button.pack(side=TOP, padx=15, pady=20) #sets button location and adds external padding around the button 

def disable_button(): #creates a function that will destroy the window completely
    window.destroy()
    window.quit()

exit_button = Button(window, #creates an exit button 
             text= "Exit", 
             command= disable_button,
             fg= "white",
             bg="black",
             height =2,
             width= 10)

#packs button which places it
exit_button.pack(side=BOTTOM, padx=15, pady=20) #sets button location and adds external padding around the button


# runs the gui
window.mainloop()


#f = open('analysis.txt', 'w' )
#f.write(textstr)
#f.close()
