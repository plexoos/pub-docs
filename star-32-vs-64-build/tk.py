import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import star.utils as stu


def ks_simple(d1, d2):
    data1 = np.sort(d1)
    data2 = np.sort(d2)

    data_all = np.concatenate([data1, data2])
    # using searchsorted solves equal data problem
    cdf1 = np.searchsorted(data1, data_all, side='right') / data1.size
    cdf2 = np.searchsorted(data2, data_all, side='right') / data2.size
    cddiffs = cdf1 - cdf2
    minS = -np.min(cddiffs)
    maxS = np.max(cddiffs)
    return max(minS, maxS), data_all, cdf1, cdf2, cddiffs


def wasserstein_simple(data1, data2):
    u_values = data1
    v_values = data2

    u_sorter = np.argsort(u_values)
    v_sorter = np.argsort(v_values)

    all_values = np.concatenate((u_values, v_values))
    all_values.sort(kind='mergesort')

    # Compute the differences between pairs of successive values of u and v.
    deltas = np.append(np.diff(all_values), 0)

    # Get the respective positions of the values of u and v among the values of
    # both distributions.
    u_cdf_indices = u_values[u_sorter].searchsorted(all_values, 'right')
    v_cdf_indices = v_values[v_sorter].searchsorted(all_values, 'right')

    # Calculate the CDFs of u and v using their weights, if specified.
    u_cdf = u_cdf_indices / u_values.size
    v_cdf = v_cdf_indices / v_values.size

    # Compute the value of the integral based on the CDFs.
    d = np.sum(np.multiply(np.abs(u_cdf - v_cdf), deltas))
    c = np.sum(np.abs(u_cdf - v_cdf))
    s = np.average(np.multiply( 1*(np.abs(u_cdf - v_cdf) > 0), deltas))
    return d, c, s, all_values, u_cdf, v_cdf


def match_closest(data1, data2):

    data_all = np.concatenate([data1, data2])
    data_idx = np.arange(len(data_all))

    data_all_argsort = data_all.argsort()

    data_all_srt = data_all[data_all_argsort]
    data_idx_srt = data_idx[data_all_argsort]

    len1 = len(data1)
    diff_all = np.diff(data_all_srt)
    diff_msk = np.array([ max(idx1, idx2) >= len1 and min(idx1, idx2) < len1 for idx1, idx2 in zip(data_idx_srt[:-1], data_idx_srt[1:])])

    # We would like to start matching pairs having the smallest difference
    # hence, sort by the distance between the values
    diff_all_masked_argsort = diff_all[diff_msk].argsort()

    diff_idx = np.arange(len(diff_all))
    diff_idx_msk_srt = diff_idx[diff_msk][diff_all_masked_argsort]

    # each interval with index idx corresponds to two end points with indices idx and idx+1
    mdiff_indices = []
    used_points = set()
    for idx in diff_idx_msk_srt:
        if idx not in used_points and idx+1 not in used_points:
            mdiff_indices.append( idx )
            used_points.update([idx, idx+1])

    mdiff_indices = np.array(mdiff_indices)

    left_idx, right_idx = data_all_argsort[mdiff_indices], data_all_argsort[mdiff_indices+1]

    m1, m2 = np.minimum(left_idx, right_idx), np.maximum(left_idx, right_idx)

    assert (data1[m1] == data_all[m1]).all()
    assert (data2[m2 - len1] == data_all[m2]).all()

    rms = np.sqrt(np.mean(np.square(data1[m1] - data2[m2 - len1])))

    return m1, m2-len1, rms, len1-len(m1), len(data2)-len(m1)


def plot_R_vs_S(R, S, spacing, label, axes):
    if label == 'C': 
        bins = np.logspace(-9, 0, 100)
    if label == 'U': 
        bins = np.logspace(-4, 1, 100)

        
    R_s = np.sort(R)
    S_o = {shuffle: s for shuffle, s in S.items() if shuffle != 0}
    S_s = {shuffle: np.sort(s) for shuffle, s in S.items() if shuffle != 0}
 
    # First row
    ax = axes[0,0]
    for shuffle, s in S_o.items():
        ax.plot(R, s, '.', ms=1, label=f'{label} {shuffle}')
    ax.legend(markerscale=10)
    ax.set_xlabel('R')
    ax.set_ylabel(f'{label}')
    ax.grid()
    
    ax = axes[0,1]
    for s in S_s.values():
        ax.plot(R_s, s, '.', ms=1)
    ax.set_xlabel(r'$R_s$, sorted')
    ax.set_ylabel(f'${label}_s$, sorted')
    ax.grid()

    # Second row
    ax = axes[1,0]
    for shuffle, s in S_o.items():
        ax.hist(np.abs(R - s), bins=bins, cumulative=True, density=True, label=f'{label} {shuffle}', histtype='step')
        ax.plot([spacing, spacing], [0,1], 'r--')
    ax.semilogx()
    ax.set_xlabel(r'$\left| R - ' + f'{label}' + r' \right|$')
    ax.set_ylabel('Cumulative')
    ax.legend(loc='upper left')
    ax.grid()

    ax = axes[1,1]
    for s in S_s.values():
        ax.hist(np.abs(R_s - s), bins=bins, cumulative=True, density=True, histtype='step')
        ax.plot([spacing, spacing], [0,1], 'r--')
    ax.semilogx()
    ax.set_xlabel(r'$\left| R_s - ' + f'{label}' + r'_s \right|$'),
    ax.set_ylabel('Cumulative')
    ax.grid()


def plot_cumpdf(d1, d2, ax, axdiff=None):
    data1 = np.sort(d1)
    data2 = np.sort(d2)

    data_all = np.concatenate([data1, data2])
    # using searchsorted solves equal data problem
    cdf1 = np.searchsorted(data1, data_all, side='right') / data1.size
    cdf2 = np.searchsorted(data2, data_all, side='right') / data2.size

    sorter = data_all.argsort()
    ax.step(data_all[sorter], cdf1[sorter], where='post', alpha=0.7)
    ax.step(data_all[sorter], cdf2[sorter], where='post', alpha=0.7)
    ax.set_ylabel('CDF1, CDF2')
    ax.grid()

    ax2 = ax.twinx()
    ax2.set_ylim([-1,1])
    ax2.axis('off')
    ax2.plot([np.min(data_all), np.max(data_all)], [0, 0], 'k-')
    ax2.plot(data_all, np.full_like(data_all, 0), 'k|', ms=5)
    ax2.plot(data1, np.full_like(data1,  0.06), 'v')
    ax2.plot(data2, np.full_like(data2, -0.06), '^')

    if axdiff:
        from matplotlib.ticker import MaxNLocator

        cddiffs = cdf1[sorter] - cdf2[sorter]
        #axdiff.step(data_all, np.abs(cddiffs), where='post', color='r')
        #axdiff.plot(data_all, np.abs(cddiffs), 'rs', ms=5)

        axdiff.step(data_all[sorter], cddiffs, where='post', color='g')
        axdiff.plot(data_all[sorter], cddiffs, 'gs', ms=5)
        axdiff.plot([np.min(data_all), np.max(data_all)], [0, 0], 'k-')

        axdiff.yaxis.set_major_locator(MaxNLocator(integer=True))
        axdiff.set_ylabel('CDF1 - CDF2')
        axdiff.grid()


def plot_match(data1, data2):
    fig, ax = plt.subplots(2, 2, figsize=(10,8))
    ax[0,0].hist2d(data_all[m1], data_all[m2], bins=50)
    ax[0,1].plot(data1[mmask1], data2[mmask2], 'o')
    ax[1,0].hist(data1[mmask1] - data2[mmask2], bins=np.linspace(-1e-3, 1e-3, 100))
    ax[1,1].plot(data1[~mmask1], 'o', data2[~mmask2], '+')
    plt.show()


def plot_compare(df_pairs, colname, figsize, **hist_kwargs):
    for df_pair in df_pairs:
        fig = plt.figure(figsize=figsize)
        df1, df2 = df_pair
        plot_compare_pair(fig, df1, df2, colname, **hist_kwargs)


def plot_compare_pair(fig, df1, df2, colname, **hist_kwargs):
    assert (df1.columns == df2.columns).all()

    from matplotlib.gridspec import GridSpec
    gs = GridSpec(1, 2, width_ratios=[2,1], figure=fig)
    ax_up = fig.add_subplot(gs[0])
    ax_dn = ax_up.twinx()
    ax_pj = fig.add_subplot(gs[1], sharey=ax_dn)

    plt.setp(ax_dn.get_yticklabels(), visible=False)
    #plt.setp(ax_pj.get_yticks(), visible=False)

    s1, s2 = df1[colname], df2[colname]
    if 'bins' in hist_kwargs.keys():
        bins = hist_kwargs['bins']
        h1, h2, ratio, errors, edges = stu.divide_histograms(s1, s2, bins=bins)
    else:
        h1, h2, ratio, errors, edges = stu.divide_histograms(s1, s2)

    centers = (edges[1:] + edges[:-1]) / 2
    ax_up.hist(centers, weights=h1, label='32', **hist_kwargs)
    ax_up.hist(centers, weights=h2, label='64', **hist_kwargs)
    ax_up.semilogy()
    #ax_up.legend(loc='upper left')
    ax_up.legend()
    ax_up.grid()

    #ax_dn.errorbar(centers, ratio, yerr=errors, marker='.', ms=3, ls='', lw=1, color='C2')
    ax_dn.plot(centers, ratio, marker='.', ms=5, ls='', lw=1, color='C2')
    ax_dn.plot([centers[0], centers[-1]], [1,1], 'C2-', lw=1)
    ax_dn.tick_params(axis='y',labelcolor='C2')
    
    ax_pj.hist(ratio[~np.isnan(ratio)], bins=50, orientation='horizontal', color='C2')
    ax_pj.semilogx()
    ax_pj.grid()
    ax_pj.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax_pj.tick_params(axis='y', labelcolor='C2')
