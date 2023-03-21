 
from GeomagReadData import GeomagReadData
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
 




class GeomagQuickPlot(GeomagReadData):

    def __init__(self):
        super().__init__()    
        self.site_list = ''
        self.t_start   = datetime(2000, 1, 1)
        self.t_end     = datetime(2000, 1, 1)
        self.nsite     = 0
        self.unit      = 500.   # unit length in nT
        self.linecolor = 'black'
        pass



    

    def get_data(self):
        data = []
        dt   = []     # datetime
        self.nsite = len(self.site_list)
        #
        for site in self.site_list:
            self.site       = site
            #
            d1, d2 = self.GeomagReadData()
            data.append(d1)
            dt.append(d2)

        return data, dt





    def make_quickplot(self):

        data0, dt0 = self.get_data()
        #
        #
        t_start = self.t_start
        t_end   = self.t_end

        data = []
        dt   = []
        for i in range(self.nsite):
            d0   = data0[i]
            t0   = dt0[i]
            #
            idx  = [ i for i in range(len(d0)) if (t0[i] >= t_start) & (t0[i] <= t_end)] 
            d0   = d0[idx[0]:idx[-1]]
            t0   = t0[idx[0]:idx[-1]]

            data.append(d0)
            dt.append(t0)

            
        #
        # amplitude
        amp = []
        for i in range( self.nsite ):
            amp.append( max(data[i]) - min(data[i]) ) 
        amp = max(amp)
        
        unit    = self.unit
        #
        if unit < amp : 
            height = (amp - np.mod(amp, unit)) 
        else:
            height = unit

        center  = (self.nsite - 1. - np.arange( self.nsite ) ) * height + 0.5 * height  


        fig, ax = plt.subplots(1, 1, sharex='all')
        fig.subplots_adjust(hspace=0.)
        
        #
        # Supress Tick
        ax.tick_params(labelbottom=True, labelleft=False, \
                       labelright=False, labeltop=False)
        
        #
        # grid
        ax.grid(axis='x',linestyle='dotted', color='black')
        #ax.grid(axis='y',linestyle='dotted', color='black')
        ax.set_yticks([])
          
        #
        # plot
        for i in range(self.nsite):
            d0 = data[i]
            t0 = dt[i]
            # normalize
            mean = np.nanmean(d0)
            d0   = d0 - mean + center[i]
            ax.plot(t0, d0, color=self.linecolor)
            #
            # center line
            width = t0[-1] - t0[0]
            ax.plot([t0[0], t0[-1]], [center[i], center[i]], \
                     linewidth=1, linestyle='--', color='black')
            ax.set_xlim( [t0[0], t0[-1]] )
            #
            xl    = t0[0] - width * 0.12
            ax.text(xl, center[i] , ' ' + self.site_list[i] + '\n(' + \
                    '{:.0f}'.format( mean  ) + ' nT)', \
                    fontsize = 'x-large', fontweight='normal' \
                    )


        #
        #
        # unit bar 

        ylim  = ax.get_ylim()
        xlim  = ax.get_xlim()
        width = xlim[-1] - xlim[0]
        xb    = xlim[-1] + width*0.02
        #
        ax.annotate("", xy = [xlim[-1], center[-2] - unit/2.], \
                        xytext = [xlim[-1], center[-2] + unit/2.], \
                        clip_on = False, arrowprops=dict(arrowstyle='<|-|>',facecolor='b', \
                        edgecolor='b')) 

        ax.text(xb, center[-2], '{:.0f}'.format(unit) + ' nT' )



        ## date
        xt = xlim[-1] - width * 0.28
        yt = ylim[0] - height * 0.4
        tx = "Created at " + datetime.now().strftime("%h %d, %Y, %H:%M:%S") + ' JST'
        ax.text(xt, yt, tx, fontsize="x-small", fontstyle="italic")




        return fig
     





if __name__ == '__main__':
    #
    #  figure size
    plt.rcParams["figure.figsize"] = (10, 10)
    #
    # site
    gq = GeomagQuickPlot()
    #gq.site_list = ['HER', 'ABG', 'ABG', 'HER', 'ABG', 'HER', 'ABG', 'HER', 'HER', 'ABG']
    gq.site_list  = ['HON', 'ABG', 'HER', 'HER', 'HER']
    gq.t_start    = datetime(2017, 5, 1)       # self.t_start
    gq.t_end      = datetime(2017, 5, 10, 23)  # self.t_end
    gq.rootdir    = '/Users/haruto/python/pyspedas/wdc_oa_quickplot/sample'
    gq.subdir     = ['dst_realtime', 'zz_201705']
    gq.resolution = 'min'
    gq.padvalue   = 999999
    gq.unit       = 50
    gq.linecolor  = 'black'


    #
    #
    fig = gq.make_quickplot()  # return matplotlib figure object
    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))

    #
    # setting for plot
    #plt.grid(color='b', linestyle=':', linewidth=0.3)
    title = gq.t_start.strftime('%Y/%m/%d') + ' -> ' + gq.t_end.strftime('%Y/%m/%d')
    plt.title(title, color='black')




    plt.show()




