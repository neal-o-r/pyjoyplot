import pyjoyplot as pjp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':

	df = pd.read_csv('sports.csv')
	df['Hours'] = df.time / 60

	pjp.plot(data=df, x='Hours', y='playing', hue='activity', smooth=10)


	iris = sns.load_dataset('iris')
	pjp.plot(data=iris, x='sepal_length', hue='species', bins=10, kind='hist')
	plt.show()
