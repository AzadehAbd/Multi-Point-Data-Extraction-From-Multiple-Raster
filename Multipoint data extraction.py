# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:12:02 2022

@author: azade
"""

import geopandas as gpd
import os
import rasterio
import scipy.sparse as sparse 
import pandas as pd
import numpy as np


#create the table to store te extracted data
table =pd.DataFrame(index= np.arange(0,1) )



#reading and loading the village data
village = gpd.read_file(r"D:/GitHub Uploads/Multi-Point-Data-Extraction-From-Multiple-Raster/villages2.shp")
village.plot()
village["lan"]= village["geometry"].x
village["lat"]= village["geometry"].y

Matrix = pd.DataFrame()

# itraites through te rasters and save the files te data as indivitual arrayes to Matrix
for files in os.listdir(r'D:/GitHub Uploads/Multi-Point-Data-Extraction-From-Multiple-Raster'):
    #only files that the last four digits are .tif
    if files[-4:]==".tif":
        dataset=rasterio.open(r'D:/GitHub Uploads/Multi-Point-Data-Extraction-From-Multiple-Raster' + "\\" + files)
        data_array=dataset.read(1)
        data_array_sparse = sparse.coo_matrix(data_array, shape=(334,398) )
        data= files[ : -4]
        Matrix [data]=data_array_sparse.toarray().tolist()
        print("processing is done for" + files[ : -4])
            
for index, row in village.iterrows():
            village_name= str(row["Village_na"])
            lon=float (row["lan"])
            lat=float(row["lat"])
            x,y= (lon, lat)
            row, col = dataset.index(x, y)
            print("processing:" + village_name)

        #pick the extracted data and store in on a table 
            for records_data in Matrix.columns.tolist():
                a = Matrix[records_data]
                w_value=a.loc[int(row)][int(col)]
                table [records_data]=w_value
                transpose_mat=table.T
                transpose_mat.rename(columns={0: village_name }, inplace=True)
                transpose_mat2=transpose_mat.T
                
                
            transpose_mat2.to_csv(r'D:/GitHub Uploads/Multi-Point-Data-Extraction-From-Multiple-Raster' + '\\' +village_name+ '.csv')
    
    
