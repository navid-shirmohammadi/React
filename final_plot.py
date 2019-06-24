import matplotlib.pyplot as plt
import numpy as np
from numpy import log, pi
# (robot, wave, freq, bias, amplitude, t2, std2, t3, std3, t4, std4, 'round' idx, wave idx , best time, best std)

data = np.array([(1, 'sin', 3, 15, 4.6, 10.0053, 18.6254, 7.7203, 27.1827, 7.8859, 21.1547, 0, 0, 7.7203, 18.6254),
                 (1, 'round', 3, 15, 4.6, 9.5557, 22.2594, 8.7984, 22.6076, 6.6861, 19.1196, 0, 1, 6.6861, 19.1196),
                 (1, 'square', 3, 15, 4.6, 8.5952, 25.2352, 8.0165, 27.7409, 10.1336, 26.7892, 0, 2, 8.0165, 25.2352),
                 (1, 'triangle', 3, 15, 4.6, 8.6979, 19.902, 8.8141, 22.6675, 8.272, 22.693, 0, 3, 8.272, 19.902),
                 (1, 'sin', 3, 5, 4.6, 7.6827, 18.8921, 7.4039, 15.1892, 7.2497, 12.6869, 1, 0, 7.2497, 12.6869),
                 (1, 'round', 3, 5, 4.6, 8.3431, 19.7993, 14.559, 15.7913, 13.1592, 23.1067, 1, 1, 8.3431, 15.7913),
                 (1, 'square', 3, 5, 4.6, 9.8539, 23.4695, 9.9174, 20.374, 10.7262, 16.6988, 1, 2, 9.8539, 16.6988),
                 (1, 'triangle', 3, 5, 4.6, 6.6266, 12.5812, 6.9368, 11.5328, 7.9218, 18.507, 1, 3, 6.6266, 11.5328),
                 (1, 'sin', 3, 25, 4.6, 5.9716, 19.1657, 6.2179, 20.7977, 6.3307, 16.6488, 2, 0, 5.9716, 16.6488),
                 (1, 'round', 3, 25, 4.6, 6.1574, 25.7655, 6.7568, 21.2444, 6.5247, 17.0463, 2, 1, 6.1574, 17.0463),
                 (1, 'square', 3, 25, 4.6, 6.6118419, 23.235866, 5.0789441, 18.97302053, 5.3843299, 24.50745281, 2, 2,
                  5.0789441, 18.97302053),
                 (1, 'triangle', 3, 25, 4.6, 6.1168782, 19.90912412, 12.4342877, 28.33401496, 8.1963978, 23.27854198, 2,
                  3, 6.1168782, 19.90912412),
                 (1, 'sin', 5, 15, 4.6, 7.434266, 36.30037062, 7.012834, 20.1030324, 6.0976219, 13.72398022, 3, 0,
                  6.0976219, 13.72398022),
                 (1, 'round', 5, 15, 4.6, 8.1505208, 23.79352756, 10.1252213, 28.99893165, 7.4674934, 26.39091761, 3, 1,
                  7.4674934, 23.79352756),
                 (1, 'square', 5, 15, 4.6, 6.1292031, 34.35729829, 6.9890936, 20.0639567, 6.163124, 22.18465496, 3, 2,
                  6.1292031, 20.0639567),
                 (1, 'triangle', 5, 15, 4.6, 5.2123197, 18.32803558, 7.1027641, 19.17476174, 6.4024807, 19.26408406, 3,
                  3, 5.2123197, 18.32803558),
                 (1, 'sin', 5, 5, 4.6, 8.0288885, 16.2281403, 8.5100602, 33.26579892, 6.7303139, 19.44898393, 4, 0,
                  6.7303139, 16.2281403),
                 (1, 'round', 5, 5, 4.6, 10.8109915, 27.875594, 8.2057245, 27.26394492, 8.7615062, 24.55560476, 4, 1,
                  8.2057245, 24.55560476),
                 (1, 'square', 5, 5, 4.6, 11.1937771, 25.89295064, 7.6549393, 18.76099492, 7.9109182, 16.85881674, 4, 2,
                  7.6549393, 16.85881674),
                 (1, 'triangle', 5, 5, 4.6, 8.4244851, 21.13667639, 8.0502962, 26.51432628, 10.6853647, 25.13985341, 4,
                  3, 8.0502962, 21.13667639),
                 (1, 'sin', 5, 25, 4.6, 5.975245, 19.76516985, 5.7356307, 28.8377475, 6.0292522, 20.02730001, 5, 0,
                  5.7356307, 19.76516985),
                 (1, 'round', 5, 25, 4.6, 6.8994215, 30.6299576, 12.4884219, 43.18995229, 13.0986097, 35.92281471, 5, 1,
                  6.8994215, 30.6299576),
                 (1, 'square', 5, 25, 4.6, 8.2675963, 33.78587317, 7.5216971, 29.51242716, 5.2821449, 22.01257384, 5, 2,
                  5.2821449, 22.01257384),
                 (1, 'triangle', 5, 25, 4.6, 8.7929295, 29.44203214, 7.4741487, 32.28000353, 8.3660568, 19.19377051, 5,
                  3, 7.4741487, 19.19377051),
                 (1, 'sin', 5, 15, 4, 6.8880546, 20.84049171, 7.2502685, 25.277552, 8.736422, 23.74718028, 6, 0,
                  6.8880546, 20.84049171),
                 (1, 'round', 5, 15, 4, 12.7640056, 36.96441588, 23.7582732, 21.36728787, 7.9190319, 18.54981282, 6, 1,
                  7.9190319, 18.54981282),
                 (1, 'square', 5, 15, 4, 7.8203663, 20.46835042, 6.7153028, 18.0655447, 15.0947102, 40.01790725, 6, 2,
                  6.7153028, 18.0655447),
                 (1, 'triangle', 5, 15, 4, 9.6252476, 28.43021651, 12.2152999, 34.49207116, 8.1706281, 21.6830313, 6, 3,
                  8.1706281, 21.6830313),
                 (1, 'sin', 5, 15, 3, 15.2253667, 28.99099077, 9.7380528, 18.43068607, 7.4184169, 14.70316156, 7, 0,
                  7.4184169, 14.70316156),
                 (1, 'round', 5, 15, 3, 7.148089, 13.1765081, 6.3538713, 13.74044124, 6.5174923, 12.93778589, 7, 1,
                  6.3538713, 12.93778589),
                 (1, 'square', 5, 15, 3, 7.2118475, 18.97439786, 18.3293218, 36.16224493, 9.8401689, 25.33520028, 7, 2,
                  7.2118475, 18.97439786),
                 (
                 1, 'triangle', 5, 15, 3, 7.2032228, 18.43911762, 16.3863327, 37.14174514, 5.6983889, 19.59092341, 7, 3,
                 5.6983889, 18.43911762),
                 (1, 'sin', 5, 15, 2, 14.3850782, 29.5265566, 7.1203119, 14.89468361, 8.7825001, 18.69574425, 8, 0,
                  7.1203119, 14.89468361),
                 (1, 'round', 5, 15, 2, 9.2193067, 34.91386789, 11.3285804, 27.88745055, 8.3638334, 20.04907754, 8, 1,
                  8.3638334, 20.04907754),
                 (1, 'square', 5, 15, 2, 11.1625107, 29.91334796, 16.3182116, 24.89155169, 7.1335908, 17.51919578, 8, 2,
                  7.1335908, 17.51919578),
                 (
                 1, 'triangle', 5, 15, 2, 7.4044977, 24.61686645, 14.9573215, 25.13832462, 6.9541862, 25.68422251, 8, 3,
                 6.9541862, 24.61686645),
                 (2, 'sin', 3, 15, 4.6, 7.5199759, 14.76563361, 7.1196146, 15.59881302, 8.7357142, 13.08097427, 9, 0,
                  7.1196146, 13.08097427),
                 (2, 'round', 3, 15, 4.6, 14.9046105, 39.07175357, 7.0178286, 14.91944806, 7.4432786, 12.65584383, 9, 1,
                  7.0178286, 12.65584383),
                 (2, 'square', 3, 15, 4.6, 6.4546482, 17.96255571, 6.3875961, 13.2707921, 11.6270714, 15.36238271, 9, 2,
                  6.3875961, 13.2707921),
                 (
                 2, 'triangle', 3, 15, 4.6, 13.4996212, 16.13408719, 8.4912428, 29.75656349, 12.1466598, 31.69882601, 9,
                 3, 8.4912428, 16.13408719),
                 (2, 'sin', 3, 5, 4.6, None, None, None, None, None, None, 10, 0, 0, 0),
                 (2, 'round', 3, 5, 4.6, None, None, None, None, None, None, 10, 1, 0, 0),
                 (2, 'square', 3, 5, 4.6, None, None, None, None, None, None, 10, 2, 0, 0),
                 (2, 'triangle', 3, 5, 4.6, None, None, None, None, None, None, 10, 3, 0, 0),
                 (2, 'sin', 3, 25, 4.6, 7.307607, 21.59470678, 7.3278103, 16.54123905, 6.4197378, 15.69400841, 11, 0,
                  6.4197378, 15.69400841),
                 (2, 'round', 3, 25, 4.6, 6.7976745, 17.4216733, 6.698238, 15.35022702, 6.7938841, 15.94994054, 11, 1,
                  6.698238, 15.35022702),
                 (
                 2, 'square', 3, 25, 4.6, 8.520278, 23.94574499, 9.4698876, 32.82476176, 17.2160284, 29.94655208, 11, 2,
                 8.520278, 23.94574499),
                 (2, 'triangle', 3, 25, 4.6, 6.8006833, 16.62937106, 6.1874197, 15.65712609, 7.1721875, 16.81207719, 11,
                  3, 6.1874197, 15.65712609),
                 (2, 'sin', 5, 15, 4.6, 6.4682587, 35.64919851, 7.4186801, 22.14355743, 5.5428332, 16.35597623, 12, 0,
                  5.5428332, 16.35597623),
                 (2, 'round', 5, 15, 4.6, 6.0287045, 17.93366588, 7.6328841, 19.64472173, 6.4995599, 19.39351901, 12, 1,
                  6.0287045, 17.93366588),
                 (2, 'square', 5, 15, 4.6, 7.0724821, 20.40150425, 15.6818359, 39.26270811, 5.8460637, 20.17220475, 12,
                  2, 5.8460637, 20.17220475),
                 (2, 'triangle', 5, 15, 4.6, 4.4919758, 16.67442744, 5.211105, 20.20086063, 6.7723766, 37.12027106, 12,
                  3, 4.4919758, 16.67442744),
                 (2, 'sin', 5, 5, 4.6, None, None, None, None, None, None, 13, 0, 0, 0),
                 (2, 'round', 5, 5, 4.6, None, None, None, None, None, None, 13, 1, 0, 0),
                 (2, 'square', 5, 5, 4.6, None, None, None, None, None, None, 13, 2, 0, 0),
                 (2, 'triangle', 5, 5, 4.6, None, None, None, None, None, None, 13, 3, 0, 0),
                 (2, 'sin', 5, 25, 4.6, 4.5433766, 16.76424678, 11.2704975, 19.33990849, 6.5343256, 17.16585102, 14, 0,
                  4.5433766, 16.76424678),
                 (2, 'round', 5, 25, 4.6, 5.7516032, 22.41637783, 5.5762853, 22.79377371, 4.9814375, 17.01554754, 14, 1,
                  4.9814375, 17.01554754),
                 (
                 2, 'square', 5, 25, 4.6, 5.2686448, 21.41383938, 4.5973744, 14.99262054, 5.0766973, 18.36538439, 14, 2,
                 4.5973744, 14.99262054),
                 (
                 2, 'triangle', 5, 25, 4.6, 5.0846662, 20.40438963, 5.560481, 19.0746292, 8.4121226, 17.95350616, 14, 3,
                 5.0846662, 17.95350616),
                 (2, 'sin', 5, 15, 4, 8.1346515, 13.92039726, 7.0770956, 13.46594212, 5.8187082, 12.49924373, 15, 0,
                  5.8187082, 12.49924373),
                 (2, 'round', 5, 15, 4, 7.711342, 14.57282368, 6.9207357, 15.14264347, 7.0308099, 15.5796583, 15, 1,
                  6.9207357, 14.57282368),
                 (2, 'square', 5, 15, 4, 8.4468552, 17.57102708, 7.6374398, 16.02974353, 7.9311425, 17.49022149, 15, 2,
                  7.6374398, 16.02974353),
                 (2, 'triangle', 5, 15, 4, 9.578588, 20.27179976, 8.1368541, 14.28405162, 7.3141057, 14.74693651, 15, 3,
                  7.3141057, 14.28405162),
                 (2, 'sin', 5, 15, 3, 10.5829051, 15.72108076, 7.6403047, 12.99780977, 12.3369105, 31.57515682, 16, 0,
                  7.6403047, 12.99780977),
                 (2, 'round', 5, 15, 3, 8.6840021, 14.58627501, 7.8210581, 14.99100493, 7.4341651, 11.94454385, 16, 1,
                  7.4341651, 11.94454385),
                 (2, 'square', 5, 15, 3, 8.8204958, 18.82924396, 8.0595064, 14.47729083, 8.0696088, 17.29609285, 16, 2,
                  8.0595064, 14.47729083),
                 (
                 2, 'triangle', 5, 15, 3, 6.9700127, 14.12266957, 7.7074288, 15.96998522, 7.0363721, 13.58974819, 16, 3,
                 6.9700127, 13.58974819),
                 (2, 'sin', 5, 15, 2, 8.8169952, 13.01129503, 7.5778338, 12.47939823, 8.4572714, 13.20174342, 17, 0,
                  7.5778338, 12.47939823),
                 (2, 'round', 5, 15, 2, 9.8893348, 17.00946302, 8.2819572, 17.33695227, 8.0097584, 15.56800897, 17, 1,
                  8.0097584, 15.56800897),
                 (2, 'square', 5, 15, 2, 8.0757312, 12.42671702, 8.0891539, 18.20989171, 7.2946794, 13.73694213, 17, 2,
                  7.2946794, 12.42671702),
                 (2, 'triangle', 5, 15, 2, 6.872565, 13.35461658, 7.2503627, 13.81986242, 6.7397183, 13.56984784, 17, 3,
                  6.7397183, 13.35461658)])

nu = 4*pi*1e-7
N = 382
R = 1.7

robot = data[:, 0]
wave = data[:, 1]
freq = data[:, 2]
bias = data[:, 3]
amplitude = data[:, 4]
best_time = data[:, -2]
best_speed = best_time.copy()
for i in range(len(best_time)):
    if best_time[i]:
        best_speed[i] = 200 / best_time[i] # convert to speed

best_std = data[:, -1]

magnetic_field = (4/5)**1.5*nu*N/R*1000*amplitude

# wave_name = 'sin'
# wave_name = 'round'
wave_name = 'square'
# wave_name = 'triangle'

wave_data = np.where(wave == wave_name)
wave_name = 'sign'
r1 = np.intersect1d(wave_data, np.where(robot == 1))
r1_f3 = np.intersect1d(r1, np.where(freq == 3))
r1_f5 = np.intersect1d(r1, np.where(freq == 5))

r2 = np.intersect1d(wave_data, np.where(robot == 2))
r2_f3 = np.intersect1d(r2, np.where(freq == 3))
r2_f5 = np.intersect1d(r2, np.where(freq == 5))

# ============================================= std

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(bias[r1_f3], best_std[r1_f3], 'co', label='fish 1-frq: 3Hz')
plt.plot(bias[r1_f5], best_std[r1_f5], 'ro', label='fish 1-frq: 5Hz')
plt.plot(bias[r2_f3], best_std[r2_f3], 'cx', label='fish 2-frq: 3Hz')
plt.plot(bias[r2_f5], best_std[r2_f5], 'rx', label='fish 2-frq: 5Hz')

x31 = bias[r1_f3]
y31 = best_std[r1_f3]
a31 = amplitude[r1_f3]
b31 = magnetic_field[r1_f3]

x51 = bias[r1_f5]
y51 = best_std[r1_f5]
a51 = amplitude[r1_f5]
b51 = magnetic_field[r1_f5]

x32 = bias[r2_f3]
y32 = best_std[r2_f3]
a32 = amplitude[r2_f3]
b32 = magnetic_field[r2_f3]

x52 = bias[r2_f5]
y52 = best_std[r2_f5]
a52 = amplitude[r2_f5]
b52 = magnetic_field[r2_f5]

[ax.text(x31[i], y31[i] + 0, "B: %.2f mT" % b31[i], ha='left') for i in range(len(bias[r1_f3]))]
[ax.text(x51[i], y51[i] + 0, "B: %.2f mT" % b51[i], ha='left') for i in range(len(bias[r1_f5]))]
[ax.text(x32[i], y32[i] + 0, "B: %.2f mT" % b32[i], ha='left') for i in range(len(bias[r2_f3]))]
[ax.text(x52[i], y52[i] + 0, "B: %.2f mT" % b52[i], ha='left') for i in range(len(bias[r2_f5]))]

plt.ylim(10, 35)
plt.xlim(0, 30)
plt.legend(bbox_to_anchor=(0.35, 1))
plt.title(wave_name)
plt.xlabel('diversion [degree]')
plt.ylabel('std [mm]')
plt.show()

# ========================================== time

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(bias[r1_f3], best_speed[r1_f3], 'co', label='fish 1-frq: 3Hz')
plt.plot(bias[r1_f5], best_speed[r1_f5], 'ro', label='fish 1-frq: 5Hz')
plt.plot(bias[r2_f3], best_speed[r2_f3], 'cx', label='fish 2-frq: 3Hz')
plt.plot(bias[r2_f5], best_speed[r2_f5], 'rx', label='fish 2-frq: 5Hz')

x31 = bias[r1_f3]
y31 = best_speed[r1_f3]
a31 = amplitude[r1_f3]
b31 = magnetic_field[r1_f3]

x51 = bias[r1_f5]
y51 = best_speed[r1_f5]
a51 = amplitude[r1_f5]
b51 = magnetic_field[r1_f5]

x32 = bias[r2_f3]
y32 = best_speed[r2_f3]
a32 = amplitude[r2_f3]
b32 = magnetic_field[r2_f3]

x52 = bias[r2_f5]
y52 = best_speed[r2_f5]
a52 = amplitude[r2_f5]
b52 = magnetic_field[r2_f5]

[ax.text(x31[i], y31[i], "B: %.2f mT" % b31[i], ha='left') for i in range(len(bias[r1_f3]))]
[ax.text(x51[i], y51[i], "B: %.2f mT" % b51[i], ha='left') for i in range(len(bias[r1_f5]))]
[ax.text(x32[i], y32[i], "B: %.2f mT" % b32[i], ha='left') for i in range(len(bias[r2_f3]))]
[ax.text(x52[i], y52[i], "B: %.2f mT" % b52[i], ha='left') for i in range(len(bias[r2_f5]))]

plt.xlim(0, 30)
plt.ylim(15, 47)
plt.legend(bbox_to_anchor=(0.35, 1))
plt.title(wave_name)
plt.xlabel('diversion [degree]')
plt.ylabel('speed [mm/s]')
plt.show()

# ========================================== time-bias-amp=4.6

fig = plt.figure()
ax = fig.add_subplot(111)

amp46 = np.where(amplitude == 4.6)

r1_a46 = np.intersect1d(amp46, r1)
r2_a46 = np.intersect1d(amp46, r2)

r1_a46_f3 = np.intersect1d(r1_a46, r1_f3)
r1_a46_f5 = np.intersect1d(r1_a46, r1_f5)
r2_a46_f3 = np.intersect1d(r2_a46, r2_f3)
r2_a46_f5 = np.intersect1d(r2_a46, r2_f5)

plt.plot(bias[r1_a46_f3], best_speed[r1_a46_f3], 'co', label='fish 1-frq: 3Hz')
plt.plot(bias[r1_a46_f5], best_speed[r1_a46_f5], 'ro', label='fish 1-frq: 5Hz')
plt.plot(bias[r2_a46_f3], best_speed[r2_a46_f3], 'cx', label='fish 2-frq: 3Hz')
plt.plot(bias[r2_a46_f5], best_speed[r2_a46_f5], 'rx', label='fish 2-frq: 5Hz')

x31 = bias[r1_a46_f3]
y31 = best_speed[r1_a46_f3]
a31 = amplitude[r1_a46_f3]
b31 = magnetic_field[r1_a46_f3]

x51 = bias[r1_a46_f5]
y51 = best_speed[r1_a46_f5]
a51 = amplitude[r1_a46_f5]
b51 = magnetic_field[r1_a46_f5]

x32 = bias[r2_a46_f3]
y32 = best_speed[r2_a46_f3]
a32 = amplitude[r2_a46_f3]
b32 = magnetic_field[r2_a46_f3]

x52 = bias[r2_a46_f5]
y52 = best_speed[r2_a46_f5]
a52 = amplitude[r2_a46_f5]
b52 = magnetic_field[r2_a46_f5]

# [ax.text(x31[i], y31[i], "B: %.2f mT" % b31[i], ha='left') for i in range(len(bias[r1_a46_f3]))]
# [ax.text(x51[i], y51[i], "B: %.2f mT" % b51[i], ha='left') for i in range(len(bias[r1_a46_f5]))]
# [ax.text(x32[i], y32[i], "B: %.2f mT" % b32[i], ha='left') for i in range(len(bias[r2_a46_f3]))]
# [ax.text(x52[i], y52[i], "B: %.2f mT" % b52[i], ha='left') for i in range(len(bias[r2_a46_f5]))]

plt.text(25, 17, "B: 0.93mT")
plt.ylim(15, 47)
plt.xlim(0, 30)
plt.legend(bbox_to_anchor=(0.35, 1))
plt.title(wave_name)
plt.xlabel('diversion [degree]')
plt.ylabel('speed [mm/s]')
plt.show()

# ========================================== std-bias-amp=4.6

fig = plt.figure()
ax = fig.add_subplot(111)

amp46 = np.where(amplitude == 4.6)

r1_a46 = np.intersect1d(amp46, r1)
r2_a46 = np.intersect1d(amp46, r2)

r1_a46_f3 = np.intersect1d(r1_a46, r1_f3)
r1_a46_f5 = np.intersect1d(r1_a46, r1_f5)
r2_a46_f3 = np.intersect1d(r2_a46, r2_f3)
r2_a46_f5 = np.intersect1d(r2_a46, r2_f5)

plt.plot(bias[r1_a46_f3], best_std[r1_a46_f3], 'co', label='fish 1-frq: 3Hz')
plt.plot(bias[r1_a46_f5], best_std[r1_a46_f5], 'ro', label='fish 1-frq: 5Hz')
plt.plot(bias[r2_a46_f3], best_std[r2_a46_f3], 'cx', label='fish 2-frq: 3Hz')
plt.plot(bias[r2_a46_f5], best_std[r2_a46_f5], 'rx', label='fish 2-frq: 5Hz')

x31 = bias[r1_a46_f3]
y31 = best_std[r1_a46_f3]
a31 = amplitude[r1_a46_f3]
b31 = magnetic_field[r1_a46_f3]

x51 = bias[r1_a46_f5]
y51 = best_std[r1_a46_f5]
a51 = amplitude[r1_a46_f5]
b51 = magnetic_field[r1_a46_f5]

x32 = bias[r2_a46_f3]
y32 = best_std[r2_a46_f3]
a32 = amplitude[r2_a46_f3]
b32 = magnetic_field[r2_a46_f3]

x52 = bias[r2_a46_f5]
y52 = best_std[r2_a46_f5]
a52 = amplitude[r2_a46_f5]
b52 = magnetic_field[r2_a46_f5]

# [ax.text(x31[i], y31[i], "B: %.2f mT" % b31[i], ha='left') for i in range(len(bias[r1_a46_f3]))]
# [ax.text(x51[i], y51[i], "B: %.2f mT" % b51[i], ha='left') for i in range(len(bias[r1_a46_f5]))]
# [ax.text(x32[i], y32[i], "B: %.2f mT" % b32[i], ha='left') for i in range(len(bias[r2_a46_f3]))]
# [ax.text(x52[i], y52[i], "B: %.2f mT" % b52[i], ha='left') for i in range(len(bias[r2_a46_f5]))]
plt.text(25, 11, "B: 0.93mT")

plt.xlim(0, 30)
plt.ylim(10, 35)
plt.legend(bbox_to_anchor=(0.35, 1))
plt.title(wave_name)
plt.xlabel('diversion [degree]')
plt.ylabel('std [mm]')
plt.show()


# ========================================== time-amp-bias=15-freq=5

fig = plt.figure()
ax = fig.add_subplot(111)

b15 = np.where(bias == 15)
f5 = np.where(freq == 5)

b15_f5 = np.intersect1d(f5, b15)

r1_b15_f5 = np.intersect1d(b15_f5, r1)
r2_b15_f5 = np.intersect1d(b15_f5, r2)


plt.plot(magnetic_field[r1_b15_f5], best_speed[r1_b15_f5], 'co', label='fish 1-div: 15 degree')
plt.plot(magnetic_field[r2_b15_f5], best_speed[r2_b15_f5], 'rx', label='fish 2-div: 15 degree')

plt.ylim(15, 50)
plt.legend(bbox_to_anchor=(1, 1))
plt.title(wave_name)
plt.xlabel('magnetic field [mT]')
plt.ylabel('speed [mm/s]')
plt.show()

# ========================================== std-amp-bias=15-freq=5

fig = plt.figure()

plt.plot(magnetic_field[r1_b15_f5], best_std[r1_b15_f5], 'co', label='fish 1-div: 15 degree')
plt.plot(magnetic_field[r2_b15_f5], best_std[r2_b15_f5], 'rx', label='fish 2-div: 15 degree')

plt.ylim(10, 40)
plt.legend(bbox_to_anchor=(1, 1))
plt.title(wave_name)
plt.xlabel('magnetic field [mT]')
plt.ylabel('std [mm]')
plt.show()

