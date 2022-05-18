"""
eva.py: extreme value analysis with BM

Sandy H. S. Herho <herho@umd.edu> 
05/18/2022 
"""

# import libs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyextremes import EVA, get_extremes, get_return_periods

plt.style.use('ggplot')
plt.rcParams['figure.dpi'] = 1000

# data prep
df = pd.read_csv('../data/interpolated_kupang.csv', 
                 index_col='time', parse_dates=True)
ts = df['discharge']

# specify model
block_size = "365.2425D"
model = EVA(data=ts)
model.get_extremes(method="BM", extremes_type="high",
                   block_size=block_size, errors="ignore")

model.fit_model(model='Emcee', n_walkers=500, n_samples=2500)
print(model)

# plot BM
fig, ax = model.plot_extremes(figsize=(15,6))
ax.set_xlabel('time (month)', fontsize=14);
ax.set_ylabel('discharge(m$^3$/s)', fontsize=14);
fig.tight_layout();
fig.savefig('../figs/fig5.png')

# mcmc trace figs
fig, ax = model.plot_trace(figsize=(15, 8))
fig.axes[0].set_title('(a)', fontsize=20)
fig.tight_layout();
fig.savefig('../figs/fig6a.png');

fig, ax = model.plot_corner(figsize=(15, 15), levels=10);
fig.axes[0].set_title('(b)', fontsize=20);
fig.tight_layout();
fig.savefig('../figs/fig6b.png');

# BM & RP summary
summary_bm = model.get_summary(return_period=[2, 5, 10, 25, 50, 100], alpha=0.95)
summary_bm.to_csv('../data/bm_rp_sum.csv')

extremes = get_extremes(
    ts=ts,
    method="BM",
    block_size="365.2425D",
)
return_periods = get_return_periods(ts=ts, extremes=extremes, extremes_method="BM", 
                                    extremes_type="high", block_size="365.2425D",
                                    return_period_size="365.2425D",plotting_position="weibull")

rp =return_periods.sort_values("return period", ascending=False)
rp.to_csv('../data/high_return_periods.csv')


# plot return periods
fig,ax = model.plot_diagnostic(alpha=0.95, figsize=(18,12))

fig.axes[0].set_title('(a)', fontsize=20)
fig.axes[1].set_title('(b)', fontsize=20)
fig.axes[2].set_title('(c)', fontsize=20)
fig.axes[3].set_title('(d)', fontsize=20)

fig.axes[0].set_xlabel('return period (year)', fontsize=14)
fig.axes[0].set_ylabel('discharge (m$^3$/s)', fontsize=14)

fig.axes[1].set_xlabel('discharge (m$^3$/s)', fontsize=14)
fig.axes[1].set_ylabel('probability density', fontsize=14)

fig.axes[2].set_xlabel('theoretical', fontsize=14)
fig.axes[2].set_ylabel('observed', fontsize=14)

fig.axes[3].set_xlabel('theoretical', fontsize=14)
fig.axes[3].set_ylabel('observed', fontsize=14)

sns.despine(left=True)
fig.savefig('../figs/fig7.png')