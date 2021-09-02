# ----------------------------------------------------------------------------
# Data courtesy: O'Neill, P. E., S. Chan, E. G. Njoku, T. Jackson, R. Bindlish, and J. Chaubell. 2020. 
# SMAP L3 Radiometer Global Daily 36 km EASE-Grid Soil Moisture, Version 7. [Indicate subset used]. Boulder, Colorado USA.
# NASA National Snow and Ice Data Center Distributed Active Archive Center. doi: https://doi.org/10.5067/HH4SZ2PXSP6A. [31st August, 2021].
# Adaptation from https://github.com/nsidc/smap_python_notebooks

import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime as dt
import glob
import pandas as pd
from functools import reduce
pd.options.plotting.backend = "plotly"


# Bengaluru Lat Lon bounds
N_lat =  13.07
S_lat =  12.82 
W_lon =  77.1 
E_lon =   77.9
bounds = [N_lat, S_lat, W_lon, E_lon]




# get list of all files
this_dir = os.getcwd()
L3_SM_P_dir = os.path.join(this_dir, 'data/L3_SM_P/')

flist = glob.glob(os.path.join(L3_SM_P_dir, '*.h5'))


# Read binary files and reshape to correct size
lats = np.fromfile('EASE2_M36km.lats.964x406x1.double', 
						dtype=np.float64).reshape((406,964))#< reshape to dimensions above
lons = np.fromfile('EASE2_M36km.lons.964x406x1.double', 
						dtype=np.float64).reshape((406,964))




class SML3PSoilMoist:
	"""
	get soil moisture from L3 SMAP SCA-V algo for the specified date
	Parameters
	----------
	soil_moisture: numpy.array
	flag_id:  [str] Quality flag of retrieved soil moisture using SCA-V
	var_id: [str] can be replaced with scva algorithm which is the default (baseline)
	group_id: [str] retrive soil moisture for Ascending or descending pass
	file_list: [list] of downloaded files; File path of a SMAP L3 HDF5 file
	-------
	Returns Soil moisture values and time period as a DataFrame
	"""

	def __init__(self, file_list : 'list', orbit_pass: 'str'):
	
	self.file_list = file_list
	self.time_period = len(self.file_list)
	self.orbit_pass = orbit_pass
	self.group_id = 'Soil_Moisture_Retrieval_Data_' + self.orbit_pass.upper()
	self.flag_id = 'retrieval_qual_flag' 
	self.var_id = 'soil_moisture'  
	
	if orbit_pass.upper() =='PM':
		self.flag_id += '_' + self.orbit_pass.lower()
		self.var_id += '_' + self.orbit_pass.lower()
	
	with h5py.File(self.file_list[0], 'r') as f:
		self.shape_data = f[self.group_id][self.var_id].shape
	

	def run_(self):
	"""read files and return 3d array and time"""
	times = []
	sm_data_3d = np.empty([self.shape_data[0],self.shape_data[1],self.time_period])
	
	for i, fName in enumerate(self.file_list):
		sm_data_3d[:,:,i], time_i = self.read_SML3P(fName)
		times.append(time_i)

	return sm_data_3d, times


	def read_SML3P(self, filepath):
	''' This function extracts soil moisture from SMAP L3 P HDF5 file.
	# refer to https://nsidc.org/support/faq/how-do-i-interpret-surface-and-quality-flag-information-level-2-and-3-passive-soil

	Parameters
	----------
	filepath : str
		File path of a SMAP L3 HDF5 file
	Returns
	-------
	soil_moisture: numpy.array
	'''    
	with h5py.File(filepath, 'r') as f:

		group_id = self.group_id 
		flag_id = self.flag_id
		var_id = self.var_id

		flag = f[group_id][flag_id][:,:]

		soil_moisture = f[group_id][var_id][:,:]        
		soil_moisture[soil_moisture==-9999.0]=np.nan;
		soil_moisture[(flag>>0)&1==1]=np.nan # set to nan expect for 0 and even bits

		filename = os.path.basename(filepath)
		
		yyyymmdd= filename.split('_')[4]
		yyyy = int(yyyymmdd[0:4]); mm = int(yyyymmdd[4:6]); dd = int(yyyymmdd[6:8])
		date=dt.datetime(yyyy,mm,dd)

	return soil_moisture, date

	def generate_time_series(self, bbox: 'list -> [N_lat, S_lat, W_lon, E_lon]'):
	
	N_lat, S_lat, W_lon, E_lon = bbox
	subset = (lats<N_lat)&(lats>S_lat)&(lons>W_lon)&(lons<E_lon)
	sm_time = np.empty([self.time_period]);
	
	sm_data_3d, times = self.run_()
	for i in np.arange(0,self.time_period):
		sm_2d = sm_data_3d[:,:,i]
		
		sm_time[i] = np.nanmean(sm_2d[subset]);

	return pd.DataFrame({'time' : times, self.orbit_pass: sm_time })


def plot_time_series(dataframe):

	import plotly.graph_objects as go

	fig = go.Figure()

	# Add traces
	fig.add_trace(go.Scatter(x=dataframe.iloc[:,0], y=dataframe.iloc[:,1],
						mode='markers',  
						name='Desc Pass'))
	fig.add_trace(go.Scatter(x=dataframe.iloc[:,0], y=dataframe.iloc[:,2],
						mode='markers',
						name='Asc Pass'))

	fig.update_layout(
		# xaxis_title="X Axis Title",
		yaxis_title="'$cm^3 cm^{-3}$'",
		# font=dict(
		#     family="Courier New, monospace",
		#     size=18,
		#     color="RebeccaPurple"
		# ),
		title={
		'text': "Soil Moisture from July 1, 2021 to July 31, 2021",
		'y':0.9,
		'x':0.5,
		},
		xaxis = dict(
			tickmode = 'linear',
			tick0 = 0.1,
			dtick = 'D4',
			tickangle = -45,
		),
		xaxis_tickformat = '%d %B %Y'
	)

	fig.show()

if __name__ == '__main__':


	orbit_objs =  [SML3PSoilMoist(flist, orbitpass) for orbitpass in ['pm', 'am']]

	orbit_runs = [each_pass.generate_time_series(bbox = bounds) for each_pass in orbit_objs]

	df_merged = reduce(lambda x, y: pd.merge(x, y, on = 'time'), orbit_runs)
	df_merged = df_merged.sort_values(by='time')

	_ = plot_time_series(df_merged)