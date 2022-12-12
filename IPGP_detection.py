"""
    A function to detect the Initiation of Phytoplankton Growing Period (IPGP) 
    as defined in Poppeschi et al. (2022), Biogeosciences

    Written by Coline Poppeschi, Ifremer, France, May 2022: coline.poppeschi@ifremer.fr
"""

import numpy as np
from datetime import date 
import datetime
import matplotlib.pyplot as plt

def annual_ipgp(time, data, year=2012, slope_window=5, plot_serie=False, fig_name='IPGP.png'):
    
    '''
    
    Detect the IPGP from Poppeschi et al. (2022) definition to an input time series of fluorescence ('data') along with a time vector ('time'). 
    The computation needs to be done over a one year timeseries without missing values and it is performed to detect the IPGP.
    The specific year of study can be choose ('year') and the slope can be calculated over two to multiple days ('slope_window').
    Outputs are the IPGP date ('date_IPGP') and a figure illustrating the method (plot_serie=True).   
    
    Inputs:
        
        time            Time vector of daily values, in datetime.datetime object (e.g. datetime.datetime(2015, 7, 31, 12, 0, 30))
                        [List or 1D numpy.array of length X]
        data            Florescence vector 
                        [1D numpy.array of length X] 
                
    Optionnal inputs:
        
        slope_window    Number of days for the linear slope computation (integer), default = 5 days
        year            Year of fluorescence data, default year = 2012
        plot_serie      Activate the figure output fluorescence time series with date_IPGP (Boolean True or False)
        fig_name        Name of the generated figure
        
    Outputs:
        
        date_IPGP       Day of the IPGP from the January first of current year (from 0 to 365/366)
        
    Optionnal outputs:
        
        IPGP.png        Figure of the fluorescence time series with date_IPGP (png file)   
        
    '''

# Cumulate fluorescence data   
data_cumul=np.cumsum(data)

# Generate indices of one year length
n=np.arange(0,366,1)  
 
    # Initialize variable slopes    
    slopes=[]
    
    # Computation of slopes
    for i in n:
        coeff = np.polyfit(time[i:i+slope_window],data_cumul[i:i+slope_window],1)
        slope=coeff[0]
        slopes.append(slope)
    
    # Definition of threshold with the median of slopes    
    slopes=np.array(slopes)
    median_slope=np.median(slopes)
    
    # Detection of IPGP
    ind=np.where(slopes>=median_slope)
    d=ind[0]
    
    # Write IPGP dates
    print('IPGP julian date : date'+str(d))
    ipgp_str_date=(date(year,1,1)+datetime.timedelta(days=d)).strftime('%Y/%m/%d')
    print('IPGP date : date'+ipgp_str_date)
    
    # Figure to illustrate the method
    if plot_serie:
        plt.figure(figsize = (12,6))
        
        plt.subplot(211)
        plt.plot(data,'.g')
        plt.axvline(x=d,color='red',label='Start date')
        plt.ylabel('Chl-a fluorescence \n (FFU)',fontsize=18, color='green')
        plt.title('IPGP detection',fontsize=18)
        plt.yticks(fontsize=18, color='green')
        plt.xlim(0,366)
        plt.xticks([])
        plt.legend(fontsize=14)
        
        plt.subplot(212)
        plt.plot(slopes,'.k')
        plt.axvline(x=d,color='red')
        plt.xlabel('Day of year',fontsize=18)
        plt.ylabel('Slope values',fontsize=18)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.xlim(0,366)
        plt.axhline(y=median_slope,color='grey',label='Median of slopes', linestyle='--')
        plt.legend(fontsize=14)
              
        plt.savefig(fig_name,dpi=300)
        plt.close()
        
        