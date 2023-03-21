import os
import numpy as np
from io import StringIO
from datetime import datetime
import matplotlib.pyplot as plt




class GeomagReadData:

    def __init__(self):
        self.resolution    = 'hour'
        self.padvalue      = 9999
        self.data          = []
        self.datetime      = []
        self.site          = ''
        self.rootdir       = ''
        self.subdir        = ''
        self.component     = ''



    def file_search(self):
        #
        # file name format
        fn   =self.resolution + '_' + self.site + '_despike.merg'
        #
        path = ['', self.rootdir]
        #
        if type(self.subdir) is list:
            path.extend(self.subdir)
        else:
            path.append(self.subdir)
        #
        path.append(fn)
        #
        fn = os.path.join(*path) 
        if os.path.isfile(fn):
            return fn
        else:
            return ''


    #
    #
    # function for reading 1-hour data
    def read_hour(self):

        if not (self.resolution == 'hour'):
            return

        filename = self.file_search()

        if len(filename) == 0:
            print('No file: ' + filename)
            return
        
        f     = open(filename, 'r')
        lines = f.readlines()

        data  = np.zeros(0)  # data container
        date  = []           # data container
        ndays = len(lines)     # number of days in the month

        for i in range(ndays):
            line = lines[i]
            #
            # split metadata and data
            head  = line[0:10]         # like "ABG1705H05" 
            d0    = line[16:]
            #
            # replace error value
            pad = str(self.padvalue)
            #
            # split data string each 4 characters
            l     = int( len(d0) / 4 )
            d0    = [ d0[j*4:(j+1)*4] for j in range(l)]
            pad   = int(self.padvalue)
            d0    = [ pad if d0[j] == str(self.padvalue) else float(d0[j]) for j in range(len(d0)) ] 
            d0    = d0[1:-2]
            #
            # array -> ndarray
            d0   = np.array(d0)
            d0[ np.where(d0 == pad) ] = np.nan 

            #
            # set data
            data = np.append(data, d0)

            #
            # make datetime array
            year  = '20' + head[3:5]
            month = head[5:7]
            day   = head[8:10]
            #
            date = date + [year + '-' + month + '-' + day + '/' + \
                    str(hour).zfill(2) + ':' + '30:00' for hour in range(24)]
         


        date = [ datetime.fromisoformat(dt) for dt in date ] 

        #
        # remove pad value
        data[ data == self.padvalue ] = np.nan

        self.date = date
        self.data = data


        return data, date
        



    #
    #
    # function for reading 1-minute data
    def read_min(self):

        if not (self.resolution == 'min'):
            return

        filename = self.file_search()

        if len(filename) == 0:
            print('No file: ' + filename)
            return
        
        f     = open(filename, 'r')
        lines = f.readlines()

        data  = np.zeros(0)    # data container
        date  = []             # data container
        ndays = len(lines)     # number of days in the month        


        component = []

        for i in range( len(lines) ):
            line = lines[i]
            #
            # split metadata and data
            head = line[0:33]   # like "071362072872170501H00ABGI0C2"
            d0   = line[34:]

            #
            # split data string each 6 characters
            d0    = [ d0[j*6:(j+1)*6] for j in range(60) ]
            pad   = int(self.padvalue)
            d0    = [ pad if d0[j] == str(self.padvalue) else float(d0[j]) \
                      for j in range(len(d0)) ] 
            #
            component.append(line[18:19])

            #
            # array -> ndarray
            d0 = np.array(d0)
            d0[ np.where(d0 == pad) ] = np.nan

            #
            # set data
            data = np.append(data, d0)

            #
            # make datetime array
            year  = '20' + head[12:14]
            month = head[14:16]
            day   = head[16:18]
            hour  = head[19:21]
            date  = date + [year + '-' + month + '-' + day + '/' + hour + ':' + \
                    str(mm).zfill(2) + ':' + '30' for mm in range(60)]
                 

        date = [ datetime.fromisoformat(dt) for dt in date ]
        
        #
        # remove pad value
        data[ data == self.padvalue ] = np.nan

        self.date = date
        self.data = data

        return data, date


                         
        

    def GeomagReadData(self):
        if self.resolution == 'hour':
            return self.read_hour()
        if self.resolution == 'min':
            return self.read_min()




if __name__ == '__main__':
    g = GeomagReadData()
    g.rootdir = '/Users/haruto/python/pyspedas/wdc_oa_quickplot/sample'
    g.subdir  = ['dst_realtime', 'zz_201705']
    g.resolution = 'min'
    g.padvalue   = 999999
    g.site       = 'ABG'
    
    
    data, date = g.GeomagReadData()


    plt.plot(date, data)
    plt.show()
