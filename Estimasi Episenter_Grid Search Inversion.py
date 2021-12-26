import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import scipy.interpolate

vp = 4      # km/s
t0 = 0      # origin time
x0 = 40     # episenter gempa
y0 = 30     # episenter gempa

# lokasi stasiun 1,2,3,4
xi = [20, 50, 40, 10]
yi = [10, 25, 50, 40]

t_observasi= []
# Forward Modelling
for j in range(len(xi)):
    tobs = t0 + (((x0 - xi[j])**2 + (y0 - yi[j])**2)**0.5/vp)
    t_observasi.append(tobs)
# print(t_observasi)

# Dibuat ukuran grid 5km dari panjang x dan y sebesar 60km
grid_size = 5
x_line = np.arange(0, 61, grid_size)
y_line = np.arange(0, 61, grid_size)


Mdata = []
RMSe = []
for m in range(len(y_line)):
    for k in range(len(x_line)):
        error = 0
        M = [x_line[k], y_line[m]]

        for l in range(len(xi)):
            tcal = t0 + (((M[0] - xi[l])**2 + (M[1] - yi[l])**2)**0.5/vp)           # Jumlahnya ada 676 (676/4=169)
            error += (tcal - t_observasi[l])**2                                     # ini masih kuadrat dari selisih tobs dan tcal

        RMS = 1/len(xi) * (error**0.5)
        RMSe.append(RMS)

        Mdata.append(M)

print(RMSe)
episenter = np.where(RMSe == np.min(RMSe))
print(episenter)
index = episenter[0][0]
print(index)

x0 = Mdata[index][0]
y0 = Mdata[index][1]
print("Estimasi Episenter:", x0, y0)
print("RMS error:", np.min(RMSe))

print(150*'=')

sumbux = []
sumbuy = []
for kk in range(len(Mdata)):
    DATA = Mdata[kk]
    sb_x = DATA[0]
    sb_y = DATA[1]
    sumbux.append(sb_x)
    sumbuy.append(sb_y)

# PLOTTING DATA HASIL RMS ERROR

# Membuat grid x dan y
x = np.linspace(0, 60, 1000)
y = np.linspace(0, 60, 1000)
xi, yi = np.meshgrid(x, y)

# Interpolasi harga X, Y, Z
rbf = scipy.interpolate.Rbf(sumbux, sumbuy, RMSe)
z = rbf(xi, yi)

# Tampilkan peta kontur
# peta = plt.contour(x, y, z, 15, cmap= "viridis")         #cmap="RdBu_r"
peta = plt.contour(x, y, z, 10, colors= "black")       #cmap="RdBu_r"
plt.clabel(peta, inline=True, fmt='%1.0f', fontsize=10)

plt.title("Peta Kontur Fungsi Objektif Estimasi Episenter (Grid Search Inversion)")
# plt.colorbar()

# Tampilkan titik data dan nilainya
# plt.scatter(sumbux, sumbuy)
# for i, txt in enumerate(RMSe):
#     plt.annotate(txt, (sumbux[i], sumbuy[i]), fontsize=10)
plt.show()
















