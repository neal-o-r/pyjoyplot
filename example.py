import pyjoyplot as pjp
import pandas as pd

if __name__ == '__main__':

	df = pd.read_csv('sports.csv')
	df['Hours'] = df.time / 60

	pjp.plot(data=df, x='Hours', y='playing', hue='activity', smooth=10)

