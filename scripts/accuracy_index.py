'''!@brief Accuracy index by Mathieu Fauvel
'''
import scipy as sp

class CONFUSION_MATRIX:
    def __init__(self):
        self.confusion_matrix=None
        self.OA=None
        self.Kappa = None
        
    def compute_confusion_matrix(self,yp,yr):
        ''' 
        Compute the confusion matrix
        '''
        # Initialization
        n = yp.shape[0]
        C=int(yr.max())
        self.confusion_matrix=sp.zeros((C+1,C+1))
        self.confusion_matrix[0]=range(0,int(self.confusion_matrix[0].shape[0]))
        self.confusion_matrix[:,0]=range(0,int(self.confusion_matrix[0].shape[0]))
        
        
        # Compute confusion matrix
        for i in range(n):
            self.confusion_matrix[yp[i].astype(int),yr[i].astype(int)] +=1
        
        # Compute overall accuracy
        self.OA=sp.sum(sp.diag(self.confusion_matrix))/n
        
        # Compute Kappa
        nl = sp.sum(self.confusion_matrix,axis=1)
        nc = sp.sum(self.confusion_matrix,axis=0)
        self.Kappa = ((n**2)*self.OA - sp.sum(nc*nl))/(n**2-sp.sum(nc*nl))
        
        # TBD Variance du Kappa
if __name__=='__main__':
    import function_dataraster as dataraster
    # Convert vector to raster
    from osgeo import ogr, gdal
    import tempfile
    import os
    temp_folder = tempfile.mkdtemp()
    filename = os.path.join(temp_folder, 'temp.tif')
    inRaster = '/home/lennepkade/Bureau/datapag/02-Results/02-Data/spot/pansharp-Spot7.tif'
    data = gdal.Open(inRaster,gdal.GA_ReadOnly)
    inVector = '/home/lennepkade/Bureau/datapag/02-Results/02-Data/spot/pansharp-Spot7.shp'
    
    shp = ogr.Open(inVector)
    
    lyr = shp.GetLayer()
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(filename,data.RasterXSize,data.RasterYSize, 1,gdal.GDT_Byte)
    dst_ds.SetGeoTransform(data.GetGeoTransform())
    dst_ds.SetProjection(data.GetProjection())
    OPTIONS = 'ATTRIBUTE='+'class'
    gdal.RasterizeLayer(dst_ds, [1], lyr, None,options=[OPTIONS])
    data,dst_ds,shp,lyr=None,None,None,None

    X,Y = dataraster.get_samples_from_roi(inRaster,filename)

    yp=sp.random.randint(5,10,500).reshape(100,5)
    yt=sp.random.randint(5,10,500).reshape(100,5)
    CONF=CONFUSION_MATRIX()
    CONF.compute_confusion_matrix(yp,yt)
    print CONF.confusion_matrix
    print CONF.OA
    print CONF.Kappa