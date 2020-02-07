'''
        ___WutFinance___
This program was written by Joe Stephenson. 
You are free to use it however you please.
'''
import pandas as pd
import numpy as np
from numpy import isnan, array 
from sklearn.preprocessing import MinMaxScaler
from dateutil.parser import parse
import imageio
from matplotlib import pyplot
import os
from scipy.ndimage import gaussian_filter
scaler = MinMaxScaler(feature_range=(0, 1))
pyplot.style.use('fivethirtyeight')
#imageio.plugins.ffmpeg.download()

def list_companies():
    companies_1 = [
        #utlilities 
            'AES', 'LNT', 'AEE', 'AEP', 'AWK',
            'CNP', 'CMS', 'ED', 'D', 'DTE',
            'DUK', 'EIX', 'ETR', 'EVRG', 'ES',
            'EXC', 'FE', 'NEE', 'NI', 'NRG',
            'PNW', 'PPL', 'PEG', 'SRE', 'SO',
            'WEC', 'XEL',
        #energy
            'APC','APA', 'BHGE', 'COG',
            'CVX', 'XEC', 'CXO', 'COP', 'DVN', 
            'EOG', 'EQT', 'XOM', 'HAL', 'HP',
            'HES', 'KMI', 'MRO', 'MPC', 'NOV',
            'NBL', 'OXY', 'OKE', 'PSX',
            'PXD', 'RRC', 'SLB', 'FTI', 'VLO', 'WMB']
    return companies_1
#define function to fill missing values
def fill_missing_row(values):
    #check each element of list for NaN values
    for row in range(values.shape[0]):
        #If we come across an NaN value
        if isnan(values[row]):
            #We replace it with the previous row's value.
            values[row] = values[row - 1]
    return values
def wut_clean(metric):
    #define empty array to append to
    all_data = []
    #loop through all the companies
    for x in companies:
        #read data on all of our companies
        dataset = pd.read_csv(x+metric+'.csv', sep = ',', header=0, index_col=0, na_values = '0')   
        #flatten the data to a single row
        dataset = array(dataset).flatten()
        #apply our fill_missing_row function to company
        dataset = fill_missing_row(dataset)
        #convert to dictionary to easily label column
        dataset = pd.DataFrame({x:dataset})
        #append our data to our empty dataframe
        all_data.append(dataset)
    all_data = pd.DataFrame(all_data)
    all_data = np.squeeze(all_data)
    return all_data

def wut_process(all_data):
    #for every company do this
    for i in range(len(companies[0:-1])):
        #drop missing values
        all_data[i]= all_data[i].dropna()
        #normalize data to values between 0 and 1
        all_data[i] = scaler.fit_transform(all_data[i])
    return all_data

def wut_sparse_dates(dates, interval):
    #create empty array
    dates_1 = []
    #select the data on one company
    dates = dates[0]
    #clear missing values
    dates = dates.dropna()
    #clear column name
    dates.columns = ['']
    #for k in range of our entire datasets interval
    for k in range(len(dates)):
        #if we are at a numbber that divides into our interval
        #then we save this date
        if (k %interval) == 0:
            dates_1.append(str(dates[k:k+1]))
        #if not, then we append nothing
        else:
            dates_1.append('')
    #creates a sparse index that can be used for better animation
    return dates_1

def wut_datetime(dates, interval):
    #convert to list
    dates = list(dates)
    #for i in range of the index
    for i in range(len(dates)):
        #if we are at our interval value
        if (i %interval) == 0:
            #we only want the date, slice the string
            dates[i] = dates[i][-8:]
            #convert to datetime type
            dates[i] = parse(dates[i]).date()
            #dates[i] = dates[i].date()
        else:
        #if not, then continue.
            continue
    return dates

%matplotlib notebook
pyplot.ioff()
def wut_color():
    #create empty array
    colors =[] 
    #set y = 0
    y = 0
    for x in range(len(companies)):
        #for the first half of the companies, we loop through blue
        if x <= len(companies)//2:
            colors.append([.95, .05, x*(1/len(companies))])
        #for the second half, we loop through red
        else:
            colors.append([2*y*(1/len(companies)), .05, .95])
            y += 1
    return colors

def wut_plot_dates(TIME, STEPS):
    #create an empty figure
    plt, ax = pyplot.subplots(1,1)
    #set width of figure
    plt.set_figwidth(50)
    #set height of figure
    plt.set_figheight(25)
    #label the X-axis with our custom index we create earlier
    ax.set_xticks(array(range(len(all_data[0][0:TIME*STEPS]))))
    #set the labels
    ax.set_xticklabels(array(dates[0:TIME*STEPS]))
    #set the size of the ticks
    pyplot.tick_params(labelsize = 25)
    #set the title of the animation
    pyplot.title('Animating Utility and Energy Market Correlation - WutFinance', 
                 fontsize = 35)
    #set the x-axis to be constant
    pyplot.xlim(0, STEPS*(TIME-1))
    #set the y-axis to be constant
    pyplot.ylim(0, 1)
    #labbel the x-axis
    pyplot.xlabel('Date', fontsize = 30)  
    #label the y-axis
    pyplot.ylabel('Normalized Price', fontsize = 35)
def wut_plot(TIME, STEPS):
    #same as wut_plot_dates() but substantially faster.
    plt, ax = pyplot.subplots(1,1)
    plt.set_figwidth(50)
    plt.set_figheight(25)
    #ax.set_xticks(array(range(len(all_data[0][0:TIME*STEPS]))))
    #ax.set_xticklabels(array(dates[0:TIME*STEPS]))
    pyplot.tick_params(labelsize = 25)
    pyplot.title('Animating Utility and Energy Market Correlation - WutFinance', 
                 fontsize = 35)
    pyplot.xlim(0, STEPS*(TIME-1))
    pyplot.ylim(0, 1)
    pyplot.xlabel('Date', fontsize = 30)  
    pyplot.ylabel('Normalized Price', fontsize = 35)
    
def wut_draw(n, colors, STEPS): 
    #draw the data for each of our companies
    for j in range(len(companies)):
            #get the data for company j up to point n*STEPS
            data = all_data[j][0:n*STEPS]
            #plot our data passing it through gaussian filter
            pyplot.plot(gaussian_filter(data, sigma = 30),
                        #pass our color argument
                        color = colors[j],
                        #label it
                        label = companies[j]+VARIABLE, 
                        #specify linewidth
                        linewidth = 1.0)     
    #create the legend in the image.
    pyplot.legend( fontsize = 17.80, loc = 1)
    
def wut_save(n, images):
    #convert n to a string, we are going to use it a lot
    n = str(n)
    #save the figure as a png. dpi: (dots-per-inch)
    pyplot.savefig(n+'.png', dpi = 80)
    #read this file from our directory and append to empty array
    images.append(imageio.imread(n+'.png'))
    #remove that image from our directory
    os.remove(n+'.png')
    
def wut_animate(TIME, ANI_TIME, STEPS):
    #[colors.append([.6, .05, i*(1/len(companies))]) for i in range(len(companies))]
    #create a color array for our variables
    colors = wut_color()
    #create memory to store our images to
    images = []
    #we want to animate as many frames as we pass in the time variable
    for n in range(TIME): 
        print(n)
        wut_plot(TIME, STEPS) #This will be substantially faster
        #create our empty figure
        #wut_plot_dates(TIME, STEPS)
        #draw our data up to point N
        wut_draw(n, colors, STEPS)
        #save the image we just made
        wut_save(n, images)    
    #calculate the FPS parameter we will pass
    FPS = TIME*(1/ANI_TIME)
    #use imageio to save our images as an mp4
    #rimageio.mimsave('movie.mp4', images, fps= FPS)