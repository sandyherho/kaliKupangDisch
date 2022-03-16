"""
eda.py: exploratory data analysis

Sandy H. S. Herho <herho@umd.edu> 
03/16/2022 
"""

# import libs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = [15, 6]
plt.rcParams['figure.dpi'] = 1000

# interpolation
df = pd.read_csv('kupang_raw_data.csv', 
                 index_col='time', parse_dates=True)

df_interp = df.interpolate(method='pchip')
df_interp.to_csv('interpolated_kupang.csv')

plt.plot(df, 'kx');
plt.plot(df_interp);
plt.ylabel('discharge (m$^{3}$)', fontsize=14);
plt.xlabel('time (month)', fontsize=14);
plt.tight_layout();
plt.savefig('../figs/fig2.png');

# annual cycle
fig, ax = plt.subplots()
df_interp.groupby(df_interp.index.month)["discharge"].mean().plot(kind='bar', 
                                                        color='#0f82d4', 
                                                        rot=0, ax=ax);
ax.set_xlabel('month', fontsize=14);
ax.set_ylabel('discharge (m$^{3}$)', fontsize=14);

labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']
ax.set_xticklabels(labels);
fig.tight_layout();
fig.savefig('../figs/fig3.png');

# normality test
fig, ax = plt.subplots()
sns.distplot(df_interp, ax=ax)
ax.set_xlabel('discharge (m$^3$)');
fig.tight_layout();
fig.savefig('../figs/fig4.png')

from scipy.stats import shapiro
data = df_interp['discharge']
stat, p = shapiro(data)
print('Statistics=%.3f, p=%.3f' % (stat, p))
alpha = 0.05
if p > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')