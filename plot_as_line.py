import pandas as pd
from ast import literal_eval
from matplotlib import pyplot as plt
import numpy as np

file_name = "clean.xlsx"
df = pd.read_excel(io=file_name)

start = 13*0
fun_select = 1

length = 3

labels = ['sin', 'round', 'sign', 'triangle']

curve = df.iloc[4:, start + fun_select * length:start + (1 + fun_select) * length].dropna()

curve_position = curve.values[:, 0]

curve_target = curve.values[:, 1]

curve_t = curve.values[:, 2]

curve_position = [literal_eval(x) for x in curve_position]

curve_position = np.array(curve_position)

curve_round_detect = np.where(curve_target == '(200, 400)')[0]

curve_round_detect_idx = [curve_round_detect[i] for i in range(len(curve_round_detect) - 1) if curve_round_detect[i] - curve_round_detect[i + 1] != -1]

curve_x = 2*curve_position[:, 0]
curve_y = 2*curve_position[:, 1]

curve_round2_x = curve_x[curve_round_detect_idx[0]:curve_round_detect_idx[1]]
curve_round3_x = curve_x[curve_round_detect_idx[1]:curve_round_detect_idx[2]]
curve_round4_x = curve_x[curve_round_detect_idx[2]:]

curve_round2_y = curve_y[curve_round_detect_idx[0]:curve_round_detect_idx[1]]
curve_round3_y = curve_y[curve_round_detect_idx[1]:curve_round_detect_idx[2]]
curve_round4_y = curve_y[curve_round_detect_idx[2]:]

curve_round2_t = curve_t[curve_round_detect_idx[0]:curve_round_detect_idx[1]]
curve_round3_t = curve_t[curve_round_detect_idx[1]:curve_round_detect_idx[2]]
curve_round4_t = curve_t[curve_round_detect_idx[2]:]

label2 = 'round 2: ' + str(curve_round2_t[-1] - curve_round2_t[0])[:4] + ' sec'
label3 = 'round 3: ' + str(curve_round3_t[-1] - curve_round3_t[0])[:4] + ' sec'
label4 = 'round 4: ' + str(curve_round4_t[-1] - curve_round4_t[0])[:4] + ' sec'


plt.plot(curve_round2_x, curve_round2_y, '#f8b9ba', label=label2)  # pink
plt.plot(curve_round3_x, curve_round3_y, '#9ecdba', label=label3)  # green
plt.plot(curve_round4_x, curve_round4_y, '#ffc100', label=label4)  # yellow
plt.plot([400, 900, 900, 400, 400], [300, 300, 800, 800, 300], 'r--')

plt.legend(bbox_to_anchor=(0.65, 0.9))

plt.axis('equal')

plt.title(labels[fun_select])

plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')

plt.xticks(np.array(range(200,1600, 100)))
plt.yticks(np.array(range(200,1000, 100)))

plt.show()
