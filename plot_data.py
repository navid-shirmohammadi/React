import pandas as pd
from ast import literal_eval
from matplotlib import pyplot as plt
import numpy as np


file_name = "clean.xlsx"
df = pd.read_excel(io=file_name)

start = 13*0
length = 3
fun_select = 2

sin_ = df.iloc[4:, start+fun_select*length:start+(1+fun_select)*length].dropna()

sin_position = sin_.values[:, 0]

sin_target = sin_.values[:, 1]

sin_t = sin_.values[:, 2]

sin_position = [literal_eval(x) for x in sin_position]

sin_position = np.array(sin_position)

sin_round_detect = np.where(sin_target == '(200, 400)')[0]

sin_round_detect_idx = [sin_round_detect[i] for i in range(len(sin_round_detect) - 1) if sin_round_detect[i] - sin_round_detect[i + 1] != -1]

sin_x = sin_position[:, 0]

sin_y = sin_position[:, 1]

sin_round2_x = sin_x[sin_round_detect_idx[0]:sin_round_detect_idx[1]]
sin_round3_x = sin_x[sin_round_detect_idx[1]:sin_round_detect_idx[2]]
sin_round4_x = sin_x[sin_round_detect_idx[2]:]

sin_round2_y = sin_y[sin_round_detect_idx[0]:sin_round_detect_idx[1]]
sin_round3_y = sin_y[sin_round_detect_idx[1]:sin_round_detect_idx[2]]
sin_round4_y = sin_y[sin_round_detect_idx[2]:]

sin_round2_t = sin_t[sin_round_detect_idx[0]:sin_round_detect_idx[1]]
sin_round3_t = sin_t[sin_round_detect_idx[1]:sin_round_detect_idx[2]]
sin_round4_t = sin_t[sin_round_detect_idx[2]:]

print(sin_round2_t[-1] - sin_round2_t[0])
print(sin_round3_t[-1] - sin_round3_t[0])
print(sin_round4_t[-1] - sin_round4_t[0])

plt.plot(sin_round2_x, sin_round2_y, '#f8b9ba')  # pink
plt.plot(sin_round3_x, sin_round3_y, '#9ecdba')  # green
plt.plot(sin_round4_x, sin_round4_y, '#ffc100')  # yellow
plt.plot([200, 450, 450, 200, 200], [150, 150, 400, 400, 150], 'r--')
plt.show()
