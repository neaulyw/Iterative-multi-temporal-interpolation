import netCDF4 as nc
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.signal import savgol_filter
from osgeo import gdal
import os
import matplotlib.pyplot as plt
from PIL import Image

Data=nc.Dataset('C:/Users/admin/Desktop/GWR DATA/EVI_1km_46.nc', 'r', format = 'NETCDF4')
Data_Arr=np.asarray(Data.variables['EVI'])
Data_Arr_Tra=Data_Arr.transpose(1,2,0)

# Savitzky-Golay滤波
SG_filter=[]
for i in range(225):
    for j in range(300):
        SG_filter.append(savgol_filter(Data_Arr_Tra[i,j,:],3,1))

Data_SG=np.array(SG_filter).reshape(225,300,46)
# # 线性插值
xp = np.linspace(1,46,46)
xp = np.array(xp)
x = np.linspace(1,366,366)
x = np.array(x)
#
SMAP_Arr=[]
for a in range(225):
    for b in range(300):
        fp = Data_SG[a][b][:]
        pre = np.interp(x, xp, fp)
        SMAP_Arr.append(pre)
SMAP_Arr_matric=np.array(SMAP_Arr)
pre_Arr_matrix=SMAP_Arr_matric.reshape(225,300,366)
Data_Arr_Tra=pre_Arr_matrix.transpose(2,0,1)

EVI_366=np.array(Data_Arr_Tra) #EVI最终结果
#
# def Iteration(day_x,day_y,DEM,EVI):
#     Threshold = 0
#     coords = []  # 无云
#     LST_x_value = []
#     LST_y_value = []
#     DEM_value = []
#     EVI_value = []
#
#     coords_yun = []  # 有云
#     DEM_value_yun = []
#     EVI_value_yun = []
#     LST_x_value_yun = []
#
#     for x in range(xCount):
#         for y in range(yCount):
#             if day_y[x][y] > Threshold:
#                 coords.append((x, y))
#                 LST_y_value.append(day_y[x, y])
#                 LST_x_value.append(day_x[x, y])
#                 DEM_value.append(DEM[x, y])
#                 EVI_value.append(EVI[x, y])
#             else:
#                 if day_y[x][y] == Threshold:
#                     coords_yun.append((x, y))
#                     LST_x_value_yun.append(day_x[x, y])
#                     DEM_value_yun.append(DEM[x, y])
#                     EVI_value_yun.append(EVI[x, y])
#     coords = np.array(coords)
#     LST_x_value = np.array(LST_x_value)
#     DEM_value = np.array(DEM_value)
#     EVI_value = np.array(EVI_value)
#     x = np.stack((LST_x_value, DEM_value, EVI_value), axis=0).T
#     y = np.array(LST_y_value).reshape(-1, 1)
#     lineModel = LinearRegression()
#     lineModel.fit(x, y)
#     coef = lineModel.coef_  # 系数值
#     coef_arr = coef.flatten() # w=coef.shape
#     intercept = lineModel.intercept_  # 截距
#
#     coords_yun = np.array(coords_yun)
#     LST_x_value_yun = np.array(LST_x_value_yun)
#     DEM_value_yun = np.array(DEM_value_yun)
#     EVI_value_yun = np.array(EVI_value_yun)
#     x_pre = np.stack((LST_x_value_yun, DEM_value_yun, EVI_value_yun), axis=0).T
#     y_pre_arr = []
#     total_count=len(coords_yun)
#     for w in range(total_count):
#         y_pre = coef_arr[0] * x_pre[w, 0] + coef_arr[1] * x_pre[w, 1] + coef_arr[2] * x_pre[w, 2] + intercept
#         y_pre_arr.append(y_pre)
#     y_pre_arr = np.array(y_pre_arr)
#     # 插值后的影像值
#     coords = np.array(coords)
#     coords_0 = coords[:, 0].T
#     coords_1 = coords[:, 1].T
#     pixel = np.array(LST_y_value).reshape(-1, 1).flatten()
#     img = np.stack((coords_0, coords_1, pixel), axis=0).T
#
#     coords_yun = np.array(coords_yun)
#     coords_yun_0 = coords_yun[:, 0].T
#     coords_yun_1 = coords_yun[:, 1].T
#     pixel_yun = np.array(y_pre_arr).reshape(-1, 1).flatten()
#
#     img_yun = np.stack((coords_yun_0, coords_yun_1, pixel_yun), axis=0).T
#     img_all = np.concatenate((img, img_yun), axis=0)  # 最终的结果
#
#     img_all_T=img_all
#     img_all_T_sorted = np.lexsort((img_all_T[:, 1], img_all_T[:, 0]))  # 先按第0列，再按第1列
#     sorted_arr = img_all_T[img_all_T_sorted].T
#     img_all_T_2=sorted_arr[2].reshape(xCount,yCount)
#     return img_all_T_2
#
# DEM_img=nc.Dataset('C:/Users/Yuwan/Desktop/Modis/DEM.nc', 'r', format = 'NETCDF4')
# DEM_Arr=np.asarray(DEM_img.variables['DEM'])
# #
# LST_img=nc.Dataset('C:/Users/Yuwan/Desktop/Modis/LST.nc', 'r', format = 'NETCDF4')
# LST_Arr=np.asarray(LST_img.variables['LST'])
# #
# EVI_Arr=EVI_366
#
# xCount=DEM_Arr.shape[0]
# yCount=DEM_Arr.shape[1]
# Total = xCount*yCount
#
# image_A = []
# for i in range(366):
#     data=LST_Arr[i]
#     sum_count = np.count_nonzero(data > 0)
#     P = sum_count / Total
#     if 0.9 <= P <=1 or 0 <= P <= 0.1:
#         image_A.append(data)
#     elif 0.1 < P <0.9:
#         image_def=Iteration(LST_Arr[i-1],LST_Arr[i],DEM_Arr,EVI_Arr[i])
#         image_A.append(image_def)
#
# LST_366=np.array(image_A)
#
# coords_0=[[0,0],[0,1],[0,3],[0,4],[0,5],[0,8],[0,9],[0,10],[0,11],
#           [1,10],[1,11],
#           [2,11],
#           [3,0],[3,11],
#           [4,0],
#           [5,0],[5,1],[5,2],[5,3],[5,4],[5,5],[5,6],
#           [6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],
#           [7,0],[7,1],[7,2],[7,3],[7,4],[7,5],[7,6],[7,7],[7,8],
#           [8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[8,6],[8,7],[8,8],[8,9],[8,10]]
# coords_0_Arr=np.array(coords_0)
#
# LST_366_T=np.array(LST_366).transpose(1,2,0)
# for coord in coords_0_Arr:
#     m,n = coord
#     LST_366_T[m, n, :] = 0
# LST_366_0=np.array(LST_366_T)
# LST_366_F=LST_366_0.transpose(2,0,1)
# LST_366_result=LST_366_F  #多时相迭代LST插值结果
# print(LST_366_result.shape)
# #晴空像元比例
# def Percent(file_names):
#     per = []
#     Total = 59
#     for m in range(366):
#             data = np.array(file_names)
#             sum_count = np.count_nonzero(data[m] > 0)
#             P = sum_count / Total
#             per.append(P)
#     return per
#
# Before_LST = np.array(Percent(LST_Arr))
# After_LST = np.array(Percent(LST_366_result))
# print(After_LST)
#
# xbar=np.arange(1,367,1)
# # ybar_Before=Before_LST
# ybar_After=After_LST
# plt.figure(figsize=(20, 6))
# # plt.scatter(xbar,ybar_Before)
# plt.scatter(xbar,ybar_After)
# plt.savefig('C:/Users/Yuwan/Desktop/B/多时相迭代LST影像.jpg')
# plt.show()
#
input_NCdata=np.array(EVI_366) #输入数据
lon=np.asarray(Data.variables['lon'])
lat=np.asarray(Data.variables['lat'])
# print(lon,lat)

ncfile = nc.Dataset('C:/Users/admin/Desktop/GWR DATA/EVI_1km.nc' ,'w' ,format = 'NETCDF4') #保存NC路径

# 添加坐标轴（经度纬度和时间）
xdim = ncfile.createDimension('lon' ,300)
ydim = ncfile.createDimension('lat' ,225)
tdim = ncfile.createDimension('time',366)

# # 添加全局属性，比如经纬度和标题，主要是对数据进行一个简单的介绍
ncfile.setncattr_string('title' ,'TEMPERATURE')
ncfile.setncattr_string('geospatial_lat_min' ,'-36.476 degrees')
ncfile.setncattr_string('geospatial_lat_max' ,'-34.476 degrees')
ncfile.setncattr_string('geospatial_lon_min' ,'146.655 degrees')
ncfile.setncattr_string('geospatial_lon_max' ,'149.405 degrees')
#
# # 添加变量和局部属性，存入数据
var = ncfile.createVariable(varname='lon' ,datatype=np.float64,dimensions='lon')
var.setncattr_string('long_name' ,'longitude')
var.setncattr_string('units' ,'degrees_east')
var[: ] =lon
#
var = ncfile.createVariable(varname='lat' ,datatype=np.float64 ,dimensions='lat')
var.setncattr_string('long_name' ,'latitude')
var.setncattr_string('units' ,'degrees_north')
var[: ] =lat
#
tvar = ncfile.createVariable(varname='time', datatype=np.float64 ,dimensions='time')
tvar.setncattr_string('long_name' ,'time')
tvar.setncattr_string('units' ,'days since 0000-01-01')
tvar.calendar = "standard"
tvar[: ] =1
#
var = ncfile.createVariable(varname='LST' ,datatype=np.float64 ,dimensions=('time' ,'lat' ,'lon'))
var.setncattr_string('long_name' ,'LST')
var.setncattr_string('units' ,'C')
var[: ] =input_NCdata

# 关闭文件
ncfile.close()
print('finished')
