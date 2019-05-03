import pandas as pd
from math import pi
import matplotlib.pyplot as plt


def radar(acc, prev_acc):
	plt.xlim(0, 2*pi)
	plt.ylim(-20, 100)
	
	data = pd.DataFrame([acc, prev_acc], index=["acc", "prev_acc"])
	
	attributes = list(data)
	att_number = len(attributes)
	
	values = data.iloc[1].tolist()
	values += values[:1]
	
	angles = [n / float(att_number) * 2 * pi for n in range(att_number)]
	angles += angles[:1]
	
	values2 = data.iloc[0].tolist()
	values2 += values2[:1]
	
	angles2 = [n / float(att_number) * 2 * pi for n in range(att_number)]
	angles2 += angles2[:1]
	
	plt.xticks(angles[:-1], attributes)
	
	ax.plot(angles, values, 'teal')
	ax.fill(angles, values, 'teal', alpha=0.1)
	
	ax.plot(angles2, values2, 'red')
	ax.fill(angles2, values2, 'red', alpha=0.1)
	
	plt.figtext(0.1, 0.9, "acc", color="red")
	plt.figtext(0.1, 0.85, "vs.")
	plt.figtext(0.1, 0.8, "pre_acc", color="teal")
	plt.draw()
	
	plt.pause(0.15)
	
	# ax.lines[0].remove()
	ax.clear()


acc_array = [{'accuracy': 0.0, 'gain': 0, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0},
            {'accuracy': 0.0, 'gain': 10, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 0.0, 'gain': 20, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 5.0, 'gain': 30, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 38.0, 'gain': 40, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 100.0, 'gain': 50, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 100.0, 'gain': 60, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 73.0, 'gain': 70, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 51.0, 'gain': 60, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 84.0, 'gain': 70, 'contrast': 0, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 35.0, 'gain': 70, 'contrast': 10, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 13.0, 'gain': 70, 'contrast': 10, 'exposure': 0, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 26.0, 'gain': 70, 'contrast': 10, 'exposure': 10, 'brightness': 0, 'saturation': 0}, 
            {'accuracy': 80.0, 'gain': 70, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 0}, 
            {'accuracy': 46.0, 'gain': 70, 'contrast': 10, 'exposure': 10, 'brightness': 20, 'saturation': 0}, 
            {'accuracy': 100.0, 'gain': 70, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 0}, 
            {'accuracy': 38.0, 'gain': 70, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 0}, 
            {'accuracy': 0.0, 'gain': 70, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 10}, 
            {'accuracy': 0.0, 'gain': 60, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 10}, 
            {'accuracy': 0.0, 'gain': 50, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 10}, 
            {'accuracy': 41.0, 'gain': 40, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 10}, 
            {'accuracy': 100.0, 'gain': 30, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 10}, 
            {'accuracy': 15.0, 'gain': 20, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 10}, 
            {'accuracy': 33.0, 'gain': 30, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 10}, 
            {'accuracy': 0.0, 'gain': 30, 'contrast': 20, 'exposure': 10, 'brightness': 10, 'saturation': 10}, 
            {'accuracy': 0.0, 'gain': 30, 'contrast': 10, 'exposure': 10, 'brightness': 10, 'saturation': 10}]

ax = plt.axes(polar=True)

for i in range(len(acc_array)-1):
	acc = acc_array[i + 1]
	prev_acc = acc_array[i]
	radar(acc, prev_acc)
