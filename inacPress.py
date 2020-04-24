import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

# Import the data
leaseBoundary = pd.read_csv('leaseBoundary.csv')

inacP = pd.read_csv('Data\\inactiveWellPressures_clean.csv')
inacP['Top perf, ft'] = inacP['Top perf, ft'].astype('float')
inacP['Well ID'] = inacP['Well ID'].astype('str')
inacP = inacP.set_index('Well ID')

# Generate a mesh of points spanning the location of the wells. The values will be
# interpolated at these points.
latBnds = [inacP['Latitude'].min(), inacP['Latitude'].max()]
lonBnds = [inacP['Longitude'].min(), inacP['Longitude'].max()]
lonGrid, latGrid = np.meshgrid(np.arange(*lonBnds, step=1e-4),
							   np.arange(*latBnds, step=1e-4))

# Interpolate on the mesh
Pi = griddata((inacP['Longitude'], inacP['Latitude']),
			  inacP['Pressure @ datum, psi'], (lonGrid.flatten(),
											   latGrid.flatten()))

# Plot the interpolated pressure.
fig, ax = plt.subplots()

cont1 = ax.contourf(lonGrid, latGrid, Pi.reshape(latGrid.shape))
plt.colorbar(cont1)
ax.scatter(inacP['Longitude'], inacP['Latitude'], color='black')
ax.set_aspect('equal', adjustable='box')
ax.plot(leaseBoundary.loc[:, 'longitude'], leaseBoundary.loc[:, 'latitude'], '-k')

# Set title and axis' titles
ax.set_title('CRU Static reservoir pressure survey, psi (March 2020)')
ax.title.set_fontsize(16)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Annotate
ii = 0
for wellID in inacP.index:
	ax.annotate(wellID,
				(inacP.loc[wellID, 'Longitude'], inacP.loc[wellID, 'Latitude']))
	ii += 1
