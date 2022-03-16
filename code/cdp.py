"""
cdp.py: change detection variance

Sandy H.S. Herho <herho@umd.edu>
03/16/2022
"""
# import libs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ruptures as rpt

plt.style.use('ggplot')

plt.rcParams['figure.figsize'] = [17, 8]
plt.rcParams['figure.dpi'] = 1000

# annual std. calc.
df = pd.read_csv('interpolated_kupang.csv', 
                 index_col='time', parse_dates=True)
discharge_std = df.resample('Y').std()
std = discharge_std.to_numpy().flatten()

# pelt detection
model="rbf"
algo = rpt.Pelt(model=model).fit(np.log(std))
result = algo.predict(pen=2)

print(discharge_std.iloc[result[0]:result[-1]]) # DETECT PERIOD

rpt.display(np.log(std), result);
plt.xlim([0, len(std + 1)]);
plt.ylabel('std. of annual discharge');
plt.xlabel('time (year)');
plt.xticks(np.arange(0, 36, 5), ['1975','1980','1985','1990','1995','2000','2005','2010'])
plt.tight_layout();
plt.savefig('../figs/fig5.png')