from __future__ import division
import os, sys
import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
import phylo_tools as pt
import scipy.stats as stats

import parse_file
import timecourse_utils

from scipy.special import gammaln

treatments = ['0','1','2']
replicates = ['1','2','3','4','5']


latex_dict = {  'B': r'$\mathit{Bacillus\, subtilis} \; \mathrm{NCIB \, 3610}$',
                'S': r'$\mathit{Bacillus\, subtilis} \; \mathrm{NCIB \, 3610} \, \Delta \mathrm{spo0A} $',
                'C': r'$\mathit{Caulobacter \, crescentus} \; \mathrm{NA1000}$',
                'D': r'$\mathit{Deinococcus \, radiodurans} \; \mathrm{BAA-816}$',
                'P': r'$\mathit{Pseudomonas \,} \; \mathrm{sp. \, KBS0710}$',
                'F': r'$\mathit{Pedobacter \,} \; \mathrm{sp. \, KBS0701}$',
                'J': r'$\mathit{Janthinobacterium \,} \; \mathrm{sp. \, KBS0711}$'
                }


def temporal_coverage():
    df = pd.read_csv(pt.get_path() + '/data/bacillus_coverage.txt', sep = '\t', header = 'infer')#, index_col = 0)
    df['cov_ratio'] = df['CP020103'] / df['CP020102']
    df = df.sort_values('Time')
    strains = ['B', 'S']
    treatments = [0,1,2]

    fig = plt.figure()
    count = 0
    #taxa_to_analyze = taxa_to_analyze[:2]
    fig.subplots_adjust(hspace=0.35, wspace=0.35)
    for treatment in treatments:
        col = pt.get_colors()[str(treatment)]
        for strain in strains:

            ax = fig.add_subplot(3, 2, count+1)
            count+=1

            if (count==1) :
                ax.title.set_text(r'$\mathit{B. \. subtilis} \; \mathrm{sp.} \, \mathrm{168}$')
            if (count==2) :
                ax.title.set_text(r'$\mathit{B. \. subtilis} \; \mathrm{sp.} \, \mathrm{168} \, \Delta \mathrm{spo0A}$')

            reps = list(set(df.Replicate.to_list()))
            for rep in reps:
                df_i = df.loc[(df['Strain'] == strain) & (df['Treatment'] == treatment) & (df['Replicate'] == rep)]
                ax.plot(df_i.Time, df_i.cov_ratio,  'o-', c=col)

            ax.set_ylim([-0.3, 3.5])

            ax.axhline(y=1, color='darkgrey', linestyle='--')

    fig.text(0.5, 0.02, 'Time (days)', ha='center', fontsize=16)
    fig.text(0.02, 0.5, 'Plasmid-chromosome coverage ratio', va='center', rotation='vertical', fontsize=14)

    fig_name = pt.get_path() + '/figs/plasmid_coverage_plot_new.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()



def plot_plasmid_coverage():
    df = pd.read_csv(pt.get_path() + '/data/bacillus_coverage.txt', sep = '\t', header = 'infer')#, index_col = 0)
    df['cov_ratio'] = df['CP020103'] / df['CP020102']
    df_group = df.groupby(['Strain', 'Treatment', 'Time'])[["cov_ratio"]].agg(['mean', 'std', 'count'])

    df_0B = df_group.loc[('B', 0), :]
    df_1B = df_group.loc[('B', 1), :]
    df_2B = df_group.loc[('B', 2), :]
    df_0S = df_group.loc[('S', 0), :]
    df_1S = df_group.loc[('S', 1), :]
    df_2S = df_group.loc[('S', 2), :]

    df_0B_time = df_0B.reset_index().Time.values
    df_0B_mean = df_0B.reset_index().cov_ratio['mean'].values
    df_0B_se = df_0B.reset_index().cov_ratio['std'].values / np.sqrt(df_0B.reset_index().cov_ratio['count'].values)

    df_1B_time = df_1B.reset_index().Time.values
    df_1B_mean = df_1B.reset_index().cov_ratio['mean'].values
    df_1B_se = df_1B.reset_index().cov_ratio['std'].values / np.sqrt(df_1B.reset_index().cov_ratio['count'].values)

    df_2B_time = df_2B.reset_index().Time.values
    df_2B_mean = df_2B.reset_index().cov_ratio['mean'].values
    df_2B_se = df_2B.reset_index().cov_ratio['std'].values / np.sqrt(df_2B.reset_index().cov_ratio['count'].values)

    df_0S_time = df_0S.reset_index().Time.values
    df_0S_mean = df_0S.reset_index().cov_ratio['mean'].values
    df_0S_se = df_0S.reset_index().cov_ratio['std'].values / np.sqrt(df_0S.reset_index().cov_ratio['count'].values)

    df_1S_time = df_1S.reset_index().Time.values
    df_1S_mean = df_1S.reset_index().cov_ratio['mean'].values
    df_1S_se = df_1S.reset_index().cov_ratio['std'].values / np.sqrt(df_1S.reset_index().cov_ratio['count'].values)

    df_2S_time = df_2S.reset_index().Time.values
    df_2S_mean = df_2S.reset_index().cov_ratio['mean'].values
    df_2S_se = df_2S.reset_index().cov_ratio['std'].values / np.sqrt(df_2S.reset_index().cov_ratio['count'].values)


    fig = plt.figure()

    plt.subplot(311)
    plt.text(575, 2, "1-day", fontsize=14)
    plt.axhline(y=1, color = 'dimgrey', lw = 2, ls = '--', zorder=1)
    plt.errorbar(df_0S_time, df_0S_mean, yerr=df_0S_se, fmt='o', label=r'$\Delta spo0A$', mfc='white', color=pt.get_colors()[str(0)], zorder=2)
    plt.errorbar(df_0B_time, df_0B_mean, yerr=df_0B_se, fmt='o', label=r'$wt$', color=pt.get_colors()[str(0)], zorder=3)
    plt.xlim([0,710])
    plt.ylim([0,2.5])
    plt.gca().axes.xaxis.set_ticklabels([])

    plt.subplot(312)
    plt.text(575, 2, "10-days", fontsize=14)
    plt.axhline(y=1, color = 'dimgrey', lw = 2, ls = '--', zorder=1)
    plt.errorbar(df_1S_time, df_1S_mean, yerr=df_1S_se, fmt='o', label=r'$\Delta spo0A$', mfc='white', color=pt.get_colors()[str(1)], zorder=2)
    plt.errorbar(df_1B_time, df_1B_mean, yerr=df_1B_se, fmt='o', label=r'$wt$', color=pt.get_colors()[str(1)], zorder=3)
    plt.xlim([0,710])
    plt.ylim([0,2.5])
    plt.gca().axes.xaxis.set_ticklabels([])

    plt.subplot(313)
    plt.text(575, 2, "100-days", fontsize=14)
    plt.axhline(y=1, color = 'dimgrey', lw = 2, ls = '--', zorder=1)
    plt.errorbar(df_2S_time, df_2S_mean, yerr=df_2S_se, fmt='o', label=r'$\Delta spo0A$', mfc='white', color=pt.get_colors()[str(2)], zorder=2)
    plt.errorbar(df_2B_time, df_2B_mean, yerr=df_2B_se, fmt='o', label=r'$wt$', color=pt.get_colors()[str(2)], zorder=3)
    plt.xlim([0,710])
    plt.ylim([0,2.5])

    # Set common labels
    fig.text(0.5, 0.04, 'Time (days)', ha='center', va='center', fontsize=18)
    fig.text(0.06, 0.5, 'Plasmid / chromosome coverage', ha='center', va='center', rotation='vertical', fontsize=16)

    fig_name = pt.get_path() + '/figs/plasmid_coverage.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()





def plot_bPTR():
    df = pd.read_csv(pt.get_path() + '/data/bPTR_clean.txt', sep = '\t', header = 'infer')#, index_col = 0)
    df = df[np.isfinite(df['bPTR'])]

    df_mean = df.groupby(['Strain', 'Treatment', 'Time']).mean().reset_index()

    df_std = df.groupby(['Strain', 'Treatment', 'Time']).agg(stats.variation).reset_index()


    df_0B = df.loc[(df['Strain'] == 'B') & (df['Treatment'] == 0)]
    df_1B = df.loc[(df['Strain'] == 'B') & (df['Treatment'] == 1)]
    df_2B = df.loc[(df['Strain'] == 'B') & (df['Treatment'] == 2)]
    df_0S = df.loc[(df['Strain'] == 'S') & (df['Treatment'] == 0)]
    df_1S = df.loc[(df['Strain'] == 'S') & (df['Treatment'] == 1)]
    df_2S = df.loc[(df['Strain'] == 'S') & (df['Treatment'] == 2)]


    df_mean_0B = df_mean.loc[(df_mean['Strain'] == 'B') & (df_mean['Treatment'] == 0)]
    df_mean_1B = df_mean.loc[(df_mean['Strain'] == 'B') & (df_mean['Treatment'] == 1)]
    df_mean_2B = df_mean.loc[(df_mean['Strain'] == 'B') & (df_mean['Treatment'] == 2)]
    df_mean_0S = df_mean.loc[(df_mean['Strain'] == 'S') & (df_mean['Treatment'] == 0)]
    df_mean_1S = df_mean.loc[(df_mean['Strain'] == 'S') & (df_mean['Treatment'] == 1)]
    df_mean_2S = df_mean.loc[(df_mean['Strain'] == 'S') & (df_mean['Treatment'] == 2)]


    df_std_0B = df_std.loc[(df_std['Strain'] == 'B') & (df_std['Treatment'] == 0)]
    df_std_1B = df_std.loc[(df_std['Strain'] == 'B') & (df_std['Treatment'] == 1)]
    df_std_2B = df_std.loc[(df_std['Strain'] == 'B') & (df_std['Treatment'] == 2)]
    df_std_0S = df_std.loc[(df_std['Strain'] == 'S') & (df_std['Treatment'] == 0)]
    df_std_1S = df_std.loc[(df_std['Strain'] == 'S') & (df_std['Treatment'] == 1)]
    df_std_2S = df_std.loc[(df_std['Strain'] == 'S') & (df_std['Treatment'] == 2)]


    fig = plt.figure()

    plt.subplot(311)
    plt.axhline( y=np.mean(df_std_0B.bPTR.values), color=pt.get_colors()[str(0)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_std_0S.bPTR.values), color=pt.get_colors()[str(0)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_std_0B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_std_0S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 0.65, "1-day", fontsize=14)
    plt.scatter(df_std_0B.Time.values, df_std_0B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(0)], zorder=3)
    plt.scatter(df_std_0S.Time.values, df_std_0S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(0)], zorder=4)
    plt.xlim([0,710])
    plt.ylim([0,0.8])
    plt.gca().axes.xaxis.set_ticklabels([])

    plt.subplot(312)
    plt.axhline( y=np.mean(df_std_1B.bPTR.values), color=pt.get_colors()[str(1)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_std_1S.bPTR.values), color=pt.get_colors()[str(1)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_std_1B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_std_1S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 0.65, "10-days", fontsize=14)
    plt.scatter(df_std_1B.Time.values, df_std_1B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(1)], zorder=3)
    plt.scatter(df_std_1S.Time.values, df_std_1S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(1)], zorder=4)
    plt.xlim([0,710])
    plt.ylim([0,0.8])
    plt.gca().axes.xaxis.set_ticklabels([])

    plt.subplot(313)
    plt.axhline( y=np.mean(df_std_2B.bPTR.values), color=pt.get_colors()[str(2)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_std_2S.bPTR.values), color=pt.get_colors()[str(2)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_std_2B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_std_2S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 0.65, "100-days", fontsize=14)
    plt.scatter(df_std_2B.Time.values, df_std_2B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(2)])
    plt.scatter(df_std_2S.Time.values, df_std_2S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(2)])
    plt.xlim([0,710])
    plt.ylim([0,0.8])

    # Set common labels
    fig.text(0.5, 0.04, 'Time (days)', ha='center', va='center', fontsize=18)
    fig.text(0.06, 0.5, r'$\frac{\sigma}{\mu}$' + ' peak-to-trough ratio', ha='center', va='center', rotation='vertical', fontsize=18)

    fig_name = pt.get_path() + '/figs/bptr_cv_bacillus.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()




    fig = plt.figure()

    plt.subplot(311)
    plt.axhline( y=np.mean(df_mean_0B.bPTR.values), color=pt.get_colors()[str(0)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_mean_0S.bPTR.values), color=pt.get_colors()[str(0)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_mean_0B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_mean_0S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 1.65, "1-day", fontsize=14)
    plt.scatter(df_mean_0B.Time.values, df_mean_0B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(0)], zorder=3)
    plt.scatter(df_mean_0S.Time.values, df_mean_0S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(0)], zorder=4)
    plt.xlim([0,710])
    plt.ylim([0.2,2])
    plt.gca().axes.xaxis.set_ticklabels([])

    plt.subplot(312)
    plt.axhline( y=np.mean(df_mean_1B.bPTR.values), color=pt.get_colors()[str(1)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_mean_1S.bPTR.values), color=pt.get_colors()[str(1)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_mean_1B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_mean_1S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 1.65, "10-days", fontsize=14)
    plt.scatter(df_mean_1B.Time.values, df_mean_1B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(1)], zorder=3)
    plt.scatter(df_mean_1S.Time.values, df_mean_1S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(1)], zorder=4)
    plt.xlim([0,710])
    plt.ylim([0.4,2.5])
    plt.gca().axes.xaxis.set_ticklabels([])

    plt.subplot(313)
    plt.axhline( y=np.mean(df_mean_2B.bPTR.values), color=pt.get_colors()[str(2)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_mean_2S.bPTR.values), color=pt.get_colors()[str(2)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_mean_2B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_mean_2S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 1, "100-days", fontsize=14)
    plt.scatter(df_mean_2B.Time.values, df_mean_2B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(2)])
    plt.scatter(df_mean_2S.Time.values, df_mean_2S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(2)])
    plt.xlim([0,710])
    plt.ylim([0.5,1.2])

    # Set common labels
    fig.text(0.5, 0.04, 'Time (days)', ha='center', va='center', fontsize=18)
    fig.text(0.06, 0.5, 'Mean peak-to-trough ratio', ha='center', va='center', rotation='vertical', fontsize=18)

    fig_name = pt.get_path() + '/figs/bptr_mean_bacillus.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()




def plot_bPTR_all():
    df = pd.read_csv(pt.get_path() + '/data/bPTR_clean.txt', sep = '\t', header = 'infer')#, index_col = 0)
    df = df[np.isfinite(df['bPTR'])]

    df_mean = df.groupby(['Strain', 'Treatment', 'Time']).mean().reset_index()

    df_std = df.groupby(['Strain', 'Treatment', 'Time']).agg(stats.variation).reset_index()

    df_mean_0B = df_mean.loc[(df_mean['Strain'] == 'B') & (df_mean['Treatment'] == 0)]
    df_mean_1B = df_mean.loc[(df_mean['Strain'] == 'B') & (df_mean['Treatment'] == 1)]
    df_mean_2B = df_mean.loc[(df_mean['Strain'] == 'B') & (df_mean['Treatment'] == 2)]
    df_mean_0S = df_mean.loc[(df_mean['Strain'] == 'S') & (df_mean['Treatment'] == 0)]
    df_mean_1S = df_mean.loc[(df_mean['Strain'] == 'S') & (df_mean['Treatment'] == 1)]
    df_mean_2S = df_mean.loc[(df_mean['Strain'] == 'S') & (df_mean['Treatment'] == 2)]


    fig = plt.figure()

    plt.axhline( y=np.mean(df_mean_0B.bPTR.values), color=pt.get_colors()[str(0)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_mean_0S.bPTR.values), color=pt.get_colors()[str(0)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_mean_0B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_mean_0S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 1.65, "1-day", fontsize=14)
    plt.scatter(df_mean_0B.Time.values, df_mean_0B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(0)], zorder=3)
    plt.scatter(df_mean_0S.Time.values, df_mean_0S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(0)], zorder=4)

    plt.axhline( y=np.mean(df_mean_1B.bPTR.values), color=pt.get_colors()[str(1)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_mean_1S.bPTR.values), color=pt.get_colors()[str(1)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_mean_1B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_mean_1S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 1.65, "10-days", fontsize=14)
    plt.scatter(df_mean_1B.Time.values, df_mean_1B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(1)], zorder=3)
    plt.scatter(df_mean_1S.Time.values, df_mean_1S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(1)], zorder=4)

    plt.axhline( y=np.mean(df_mean_2B.bPTR.values), color=pt.get_colors()[str(2)], linestyle=':', alpha = 0.8, zorder=1)
    plt.axhline( y=np.mean(df_mean_2S.bPTR.values), color=pt.get_colors()[str(2)], linestyle=':', alpha = 0.8, zorder=2)
    plt.text(5, np.mean(df_mean_2B.bPTR.values), r'$\mathrm{wt}$')
    plt.text(5, np.mean(df_mean_2S.bPTR.values) + 0.05, r'$\Delta\mathrm{spo0A}$')
    plt.text(575, 1, "100-days", fontsize=14)
    plt.scatter(df_mean_2B.Time.values, df_mean_2B.bPTR.values, label=r'$wt$', color=pt.get_colors()[str(2)])
    plt.scatter(df_mean_2S.Time.values, df_mean_2S.bPTR.values, label=r'$\Delta spo0A$', facecolors='none', color=pt.get_colors()[str(2)])

    #plt.xlim([0,710])
    #plt.ylim([0.5,1.2])

    # Set common labels
    plt.xlabel( 'Time (days)', fontsize=18)
    plt.ylabel('Mean peak-to-trough ratio', fontsize=18)

    fig_name = pt.get_path() + '/figs/bptr_mean_bacillus_all.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()





def plot_allele_freqs():

    # only plot if they pass
    population = '1S3'
    annotated_timecourse_template = pt.get_path() + "/data/timecourse_final/%s_annotated_timecourse.txt"
    annotated_timecourse_file = open(annotated_timecourse_template % population,"r")

    first_line = annotated_timecourse_file.readline()
    first_line = first_line.strip()
    first_line_items = first_line.split(",")
    times = np.asarray([float(x.strip().split(':')[1]) for x in first_line_items[13::2]])
    times = np.insert(times, 0, 0, axis=0)
    # skip first line
    fig = plt.figure()
    for i, line in enumerate(annotated_timecourse_file):
        line = line.strip()
        items = line.split(",")
        pass_or_fail = items[12].strip()
        if pass_or_fail == 'FAIL':
            continue
        alt_cov = np.asarray([ float(x) for x in items[13::2]])
        total_cov = np.asarray([ float(x) for x in items[14::2]])
        # pseudocount to avoid divide by zero error
        alt_cov = alt_cov
        total_cov = total_cov + 1
        freqs = alt_cov / total_cov
        freqs = np.insert(freqs, 0, 0, axis=0)

        rgb = pt.mut_freq_colormap()
        rgb = pt.lighten_color(rgb, amount=0.5)
        #print(times)
        #print(total_cov)
        #if freqs[-1] > 0.9:

        plt.plot(times, freqs, '.-', c=rgb, alpha=0.7)


        #print(rgb)

    annotated_timecourse_file.close()

    plt.xlim([0,max(times)])
    plt.ylim([0, 1])

    plt.xlabel( 'Days, ' + r'$t$', fontsize=18)
    plt.ylabel('Allele frequency, ' + r'$f(t)$', fontsize=18)

    fig_name = pt.get_path() + '/figs/test_freq_trajectory.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()



def plot_allele_freqs_all_treats(strain):

    fig = plt.figure(figsize = (12, 6))

    row_count = 0
    for treatment in treatments:

        column_count = 0

        for replicate in replicates:
            ax_i = plt.subplot2grid((3, 5), (row_count, column_count), colspan=1)

            population = treatment + strain + replicate
            print(population)
            annotated_timecourse_path = pt.get_path() + "/data/timecourse_final/%s_annotated_timecourse.txt" % population
            if os.path.exists(annotated_timecourse_path) == False:
                continue
            annotated_timecourse_file = open(annotated_timecourse_path ,"r")

            first_line = annotated_timecourse_file.readline()
            first_line = first_line.strip()
            first_line_items = first_line.split(",")
            times = np.asarray([float(x.strip().split(':')[1]) for x in first_line_items[13::2]])
            times = np.insert(times, 0, 0, axis=0)


            for i, line in enumerate(annotated_timecourse_file):
                line = line.strip()
                items = line.split(",")
                pass_or_fail = items[12].strip()
                if pass_or_fail == 'FAIL':
                    continue

                alt_cov = np.asarray([ float(x) for x in items[13::2]])
                total_cov = np.asarray([ float(x) for x in items[14::2]])
                # pseudocount to avoid divide by zero error
                alt_cov = alt_cov
                total_cov = total_cov + 1
                freqs = alt_cov / total_cov
                freqs = np.insert(freqs, 0, 0, axis=0)

                rgb = pt.mut_freq_colormap()
                rgb = pt.lighten_color(rgb, amount=0.5)


                if len(times) == len(freqs) + 1:
                    freqs = np.insert(freqs, 0, 0, axis=0)

                if population == '0D1':
                    print(times, freqs)

                ax_i.plot(times, freqs, '.-', c=rgb, alpha=0.4)


            ax_i.set_xlim([0,max(times)])
            ax_i.set_ylim([0, 1])

            if column_count == 0:
                ax_i.set_ylabel( str(10**int(treatment)) + '-day transfers', fontsize =12  )

            ax_i.tick_params(axis="x", labelsize=8)
            ax_i.tick_params(axis="y", labelsize=8)

            column_count += 1
        row_count +=1


    fig.text(0.5, 0.04, 'Days, ' + r'$t$', ha='center', va='center', fontsize=24)
    fig.text(0.05, 0.5, 'Allele frequency, ' + r'$f(t)$', ha='center', va='center', rotation='vertical',  fontsize=24)


    fig.suptitle(latex_dict[strain], fontsize=28, fontweight='bold')
    fig_name = pt.get_path() + '/figs/mut_trajectories_%s.png'
    fig.savefig(fig_name % strain, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()








# calculate_unnormalized_survival_from_vector function is modified from GitHub repo
# benjaminhgood/LTEE-metagenomic under GPL v2
def calculate_unnormalized_survival_from_vector(xs, min_x=None, max_x=None, min_p=1e-10):
    if min_x==None:
        min_x = xs.min()-1

    if max_x==None:
        max_x = xs.max()+1

    unique_xs = set(xs)
    unique_xs.add(min_x)
    unique_xs.add(max_x)

    xvalues = []
    num_observations = []

    for x in sorted(unique_xs):
        xvalues.append(x)
        num_observations.append( (xs>=x).sum() )

    # So that we can plot CDF, SF on log scale
    num_observations[0] -= min_p
    num_observations[1] -= min_p
    num_observations[-1] += min_p

    return np.array(xvalues), np.array(num_observations)






# NullGeneLogpSurvivalFunction class is modified from GitHub repo
# benjaminhgood/LTEE-metagenomic under GPL v2
class NullGeneLogpSurvivalFunction(object):
    # Null distribution of -log p for each gene

    def __init__(self, Ls, ntot,nmin=0):
        self.ntot = ntot
        self.Ls = np.array(Ls)*1.0
        self.Lavg = self.Ls.mean()
        self.ps = self.Ls/self.Ls.sum()
        self.expected_ns = self.ntot*self.ps
        self.nmin = nmin

    @classmethod
    def from_parallelism_statistics(cls, gene_parallelism_statistics,nmin=0):

        # calculate Ls
        Ls = []
        ntot = 0
        for gene_name in gene_parallelism_statistics.keys():
            Ls.append(gene_parallelism_statistics[gene_name]['length'])
            ntot += gene_parallelism_statistics[gene_name]['observed']

        return cls(Ls, ntot, nmin)

    def __call__(self, mlogps):

        # Do sum by hand
        ns = np.arange(0,400)*1.0

        logpvalues = calculate_poisson_log_survival(ns[None,:], self.expected_ns[:,None])

        logprobabilities = ns[None,:]*np.log(self.expected_ns)[:,None]-gammaln(ns+1)[None,:]-self.expected_ns[:,None]
        probabilities = np.exp(logprobabilities)
        survivals = np.array([ ((logpvalues>=mlogp)*(ns[None,:]>=self.nmin)*probabilities).sum() for mlogp in mlogps])
        return survivals




# calculate_poisson_log_survival function is modified from GitHub repo
# benjaminhgood/LTEE-metagenomic under GPL v2
def calculate_poisson_log_survival(ns, expected_ns):
    # change threshold from 1e-20 to 1e-60 so that genes w/ most mutations can pass

    survivals = stats.poisson.sf(ns-0.1, expected_ns)

    logsurvivals = np.zeros_like(survivals)
    logsurvivals[survivals>1e-60] = -np.log(survivals[survivals>1e-60])
    logsurvivals[survivals<=1e-60] = (-ns*np.log(ns/expected_ns+(ns==0))+ns-expected_ns)[survivals<=1e-60]

    return logsurvivals


# calculate_parallelism_logpvalues function is modified from GitHub repo
# benjaminhgood/LTEE-metagenomic under GPL v2
def calculate_parallelism_logpvalues(gene_statistics):

    gene_names = []
    Ls = []
    ns = []
    expected_ns = []

    for gene_name in gene_statistics.keys():
        gene_names.append(gene_name)
        ns.append(gene_statistics[gene_name]['observed'])
        expected_ns.append(gene_statistics[gene_name]['expected'])

    ns = np.array(ns)
    expected_ns = np.array(expected_ns)


    logpvalues = calculate_poisson_log_survival(ns, expected_ns)

    return {gene_name: logp for gene_name, logp in zip(gene_names, logpvalues)}







def get_sig_mult_genes(gene_parallelism_statistics, nmin=2):
    # Give each gene a p-value, get distribution
    gene_logpvalues = calculate_parallelism_logpvalues(gene_parallelism_statistics)
    #print(gene_logpvalues)
    pooled_pvalues = []
    for gene_name in gene_logpvalues.keys():
        if (gene_parallelism_statistics[gene_name]['observed']>= nmin) and (float(gene_logpvalues[gene_name]) >= 0):
            pooled_pvalues.append( gene_logpvalues[gene_name] )

    pooled_pvalues = np.array(pooled_pvalues)
    pooled_pvalues.sort()
    #if len(pooled_pvalues) == 0:
    #    continue
    null_pvalue_survival = NullGeneLogpSurvivalFunction.from_parallelism_statistics( gene_parallelism_statistics, nmin=nmin)
    observed_ps, observed_pvalue_survival = calculate_unnormalized_survival_from_vector(pooled_pvalues, min_x=-4)
    # Pvalue version
    # remove negative minus log p values.
    neg_p_idx = np.where(observed_ps>=0)
    observed_ps_copy = observed_ps[neg_p_idx]
    observed_pvalue_survival_copy = observed_pvalue_survival[neg_p_idx]
    pvalue_pass_threshold = np.nonzero(null_pvalue_survival(observed_ps_copy)*1.0/observed_pvalue_survival_copy<0.05)[0]

    if len(pvalue_pass_threshold) == 0:
        return []
    else:
        threshold_idx = pvalue_pass_threshold[0]
        pstar = observed_ps_copy[threshold_idx] # lowest value where this is true
        num_significant = observed_pvalue_survival[threshold_idx]

        list_genes = []

        for gene_name in sorted(gene_parallelism_statistics, key=lambda x: gene_parallelism_statistics.get(x)['observed'],reverse=True):
            if gene_logpvalues[gene_name] >= pstar and gene_parallelism_statistics[gene_name]['observed']>=nmin:
                #print(gene_name, gene_parallelism_statistics[gene_name])
                list_genes.append(gene_name)

        return list_genes



def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))



def get_mult_similarity():

    treatments = ['0','1','2']
    replicates = ['1','2','3','4','5']
    strains = ['B','S']

    strain_treat_dict = {}

    gene_data = parse_file.parse_gene_list('B')
    position_gene_map, effective_gene_lengths, substitution_specific_synonymous_fraction = parse_file.create_annotation_map(taxon='B', gene_data=gene_data)

    #print(effective_gene_lengths)


    for strain in strains:

        for treatment in treatments:

            print(treatment + strain )

            strain_treat_gene_parallelism_statistics = {}
            n_tot = 0

            for gene_i, length_i in effective_gene_lengths.items():
                if (gene_i == 'synonymous') or (gene_i == 'nonsynonymous') or (gene_i == 'noncoding'):
                    continue
                strain_treat_gene_parallelism_statistics[gene_i] = {}
                strain_treat_gene_parallelism_statistics[gene_i]['length'] = length_i
                strain_treat_gene_parallelism_statistics[gene_i]['observed'] = 0
                strain_treat_gene_parallelism_statistics[gene_i]['multiplicity'] = 0

            for replicate in replicates:


                population = treatment + strain + replicate
                annotated_timecourse_path = pt.get_path() + "/data/timecourse_final/%s_annotated_timecourse.txt" % population
                if os.path.exists(annotated_timecourse_path) == False:
                    continue
                annotated_timecourse_file = open(annotated_timecourse_path ,"r")

                first_line = annotated_timecourse_file.readline()
                first_line = first_line.strip()
                first_line_items = first_line.split(",")
                times = np.asarray([float(x.strip().split(':')[1]) for x in first_line_items[13::2]])
                times = np.insert(times, 0, 0, axis=0)

                for i, line in enumerate(annotated_timecourse_file):
                    line = line.strip()
                    items = line.split(",")
                    pass_or_fail = items[12].strip()
                    if pass_or_fail == 'FAIL':
                        continue

                    alt_cov = np.asarray([ float(x) for x in items[13::2]])
                    total_cov = np.asarray([ float(x) for x in items[14::2]])
                    # pseudocount to avoid divide by zero error
                    alt_cov = alt_cov
                    total_cov = total_cov
                    freqs = alt_cov / total_cov


                    if np.isnan(freqs[-1]) == True:

                        last_freq = freqs[-2]
                    else:
                        last_freq = freqs[-1]

                    if last_freq <= 0.3:
                        continue

                    gene = items[1].strip()

                    if gene in strain_treat_gene_parallelism_statistics:
                        strain_treat_gene_parallelism_statistics[gene]['observed'] += 1
                        n_tot += 1


            #print(strain_treat_gene_parallelism_statistics)
            L_mean = np.mean(list(effective_gene_lengths.values()))
            L_tot = sum(list(effective_gene_lengths.values()))
            # go back over and calculate multiplicity
            for locus_tag_i in strain_treat_gene_parallelism_statistics.keys():
                # double check the measurements from this
                strain_treat_gene_parallelism_statistics[locus_tag_i]['multiplicity'] = strain_treat_gene_parallelism_statistics[locus_tag_i]['observed'] *1.0/ strain_treat_gene_parallelism_statistics[locus_tag_i]['length'] * L_mean
                strain_treat_gene_parallelism_statistics[locus_tag_i]['expected'] = n_tot*strain_treat_gene_parallelism_statistics[locus_tag_i]['length']/L_tot


            sig_genes_all = get_sig_mult_genes(strain_treat_gene_parallelism_statistics)


            strain_treat_dict[treatment + strain] = sig_genes_all

    treat_sim_list = []

    for treatment in treatments:
        treat_sim = jaccard_similarity(strain_treat_dict[treatment + 'B'], strain_treat_dict[treatment + 'S'])

        treat_sim_list.append(treat_sim)

    fig = plt.figure()

    plt.plot([1, 10, 100], treat_sim_list, '.-', c = 'blue', alpha=0.9, markersize = 14)
    plt.xscale('log', basex=10)

    plt.xlabel('Transfer time', fontsize = 14)
    plt.ylabel("Jaccard similarity of significant\ngenes between " + r'$\mathrm{WT}$' + ' and ' + r'$\Delta \mathrm{spo0A}$', fontsize = 14)


    fig_name = pt.get_path() + '/figs/jaccard.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()







def get_mutation_fixation_trajectories(population):

    mutations, depth_tuple = parse_file.parse_annotated_timecourse(population)
    population_avg_depth_times, population_avg_depths, clone_avg_depth_times, clone_avg_depths = depth_tuple
    state_times, state_trajectories = parse_file.parse_well_mixed_state_timecourse(population)

    times = mutations[0][9]
    Ms = np.zeros_like(times)*1.0
    fixed_Ms = np.zeros_like(times)*1.0

    #transit_times[population] = []

    for mutation_idx in range(0,len(mutations)):

        location, gene_name, allele, var_type, test_statistic, pvalue, cutoff_idx, depth_fold_change, depth_change_pvalue, times, alts, depths, clone_times, clone_alts, clone_depths = mutations[mutation_idx]

        state_Ls = state_trajectories[mutation_idx]

        good_idxs, filtered_alts, filtered_depths = timecourse_utils.mask_timepoints(times, alts, depths, var_type, cutoff_idx, depth_fold_change, depth_change_pvalue)

        freqs = timecourse_utils.estimate_frequencies(filtered_alts, filtered_depths)

        masked_times = times[good_idxs]
        masked_freqs = freqs[good_idxs]
        masked_state_Ls = state_Ls[good_idxs]

        t0,tf,transit_time = timecourse_utils.calculate_appearance_fixation_time_from_hmm(masked_times, masked_freqs, masked_state_Ls)
        if t0==tf==transit_time==None:
            continue

        #transit_times[population].append(transit_time)

        interpolating_function = timecourse_utils.create_interpolation_function(masked_times, masked_freqs, tmax=100000)

        fs = interpolating_function(times)
        fs[fs<0]=0

        # Record
        Ms += fs
        if masked_state_Ls[-1] in parse_file.well_mixed_fixed_states:
            fixed_Ms += (times>=tf)


    return times, Ms, fixed_Ms





def plot_B_S_mutation_trajectory():
    sys.stderr.write("Loading mutation data...\n")

    mutation_trajectories = {}
    fixed_mutation_trajectories = {}
    #transit_times = {}
    taxa = ['B', 'S']

    for treatment in treatments:
        for taxon in taxa:
            for replicate in replicates:

                population = treatment + taxon + replicate
                sys.stderr.write("Processing %s...\t" % population)

                times, Ms, fixed_Ms = get_mutation_fixation_trajectories(population)

                fixed_mutation_trajectories[population] = (times, fixed_Ms)
                mutation_trajectories[population] = (times, Ms)

                sys.stderr.write("analyzed %d mutations!\n" % len(mutations))


    fig = plt.figure(figsize = (10, 6))

    column_count = 0

    for treatment in treatments:

        ax_t_vs_M = plt.subplot2grid((2, 3), (0, column_count), colspan=1)
        ax_M_vs_F = plt.subplot2grid((2, 3), (1, column_count), colspan=1)

        #ax_M_vs_F.plot([0,300],[0,300],'--',linewidth=1,color='k', zorder=1)

        for taxon_i, taxon in enumerate(taxa):

            treatment_taxon_populations = []


            for replicate in replicates:

                population = treatment + taxon + replicate

                Mts,Ms = mutation_trajectories[population]
                fixed_Mts, fixed_Ms = fixed_mutation_trajectories[population]

                ax_t_vs_M.plot(Mts, Ms, 'o-',color= pt.get_colors(treatment), marker=pt.plot_species_marker(taxon), fillstyle=pt.plot_species_fillstyle(taxon), alpha=1, markersize=7,linewidth=2, markeredgewidth=1.5, zorder=1)

                ax_M_vs_F.plot(fixed_Mts, fixed_Ms, 'o-', color= pt.get_colors(treatment), marker=pt.plot_species_marker(taxon), fillstyle=pt.plot_species_fillstyle(taxon), alpha=1, markersize=7,linewidth=2, markeredgewidth=1.5, zorder=1)
                #late_mut_axis.plot(Mts, Ms-intercept, linestyle, color=colorVal, alpha=1, markersize=1,linewidth=0.5,zorder=zorder, markeredgewidth=0)

                ax_t_vs_M.set_xlabel('Days, ' + r'$t$', fontsize = 11)
                ax_t_vs_M.tick_params(axis='x', labelsize=8)


                ax_M_vs_F.set_xlabel('Mutations, ' + r'$M(t)$', fontsize = 12)


                treatment_taxon_populations.append(population)

            avg_Mts, avg_Ms = timecourse_utils.average_trajectories([mutation_trajectories[population] for population in treatment_taxon_populations])

            if taxon == 'B':
                ls = '--'
            else:
                ls = ':'

            ax_t_vs_M.plot(avg_Mts, avg_Ms, ls,color='k', marker=" ", alpha=1, linewidth=2.5, zorder=2)


            if (taxon_i == 0) and (column_count==0):
                legend_elements = [Line2D([0], [0], ls='--', color='k', lw=1.5, label= r'$\overline{M}_{WT} (t)$'),
                                   Line2D([0], [0], ls=':', color='k', lw=1.5, label= r'$\overline{M}_{\Delta \mathrm{spo0A}} (t)$')]
                ax_t_vs_M.legend(handles=legend_elements, loc='upper left', fontsize=6.5)

        ax_t_vs_M.set_title( str(10**int(treatment))+ '-day transfers', fontsize=17)

        if treatment == '2':
            ax_M_vs_F.yaxis.set_major_locator(MaxNLocator(integer=True))

        if column_count == 0:

            ax_t_vs_M.set_ylabel('Mutations, ' + r'$M(t)$', fontsize = 14)
            ax_M_vs_F.set_ylabel('Fixed mutations', fontsize = 14)

        column_count += 1

    fig_name = pt.get_path() + '/figs/B_S_rate.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()



def allele_survival():
    frequencies = np.linspace(0.1,0.9,201)
    df = 0.05
    fstar = 0.5

    #tstar = 20025

    null_num_in_bin = np.zeros_like(frequencies)
    null_avg_f = np.zeros_like(frequencies)

    origin_fixation_times = {}

    taxa = ['B', 'S']

    #fig = plt.figure()
    fig = plt.figure(figsize = (12, 6))

    for treatment in ['0']:
        for taxon_idx, taxon in enumerate(taxa):
            ax_i = plt.subplot2grid((1, 2), (0, taxon_idx), colspan=1)
            for replicate in ['1', '2', '3', '4', '5']:
                population = treatment + taxon + replicate

                num_runs = []

                num_in_bin = np.zeros_like(null_num_in_bin)
                avg_f = np.zeros_like(null_avg_f)

                origin_fixation_times[population] = ([],[],[])

                sys.stderr.write("Processing fixation probabilities for %s...\n" % population)

                # load mutations
                mutations, depth_tuple = parse_file.parse_annotated_timecourse(population)
                population_avg_depth_times, population_avg_depths, clone_avg_depth_times, clone_avg_depths = depth_tuple
                state_times, state_trajectories = parse_file.parse_well_mixed_state_timecourse(population)

                num_runs = []

                for mutation_idx in range(0,len(mutations)):

                    location, gene_name, allele, var_type, test_statistic, pvalue, cutoff_idx, depth_fold_change, depth_change_pvalue, times, alts, depths, clone_times, clone_alts, clone_depths = mutations[mutation_idx]

                    state_Ls = state_trajectories[mutation_idx]

                    good_idxs, filtered_alts, filtered_depths = timecourse_utils.mask_timepoints(times, alts, depths, var_type, cutoff_idx, depth_fold_change, depth_change_pvalue)

                    freqs = timecourse_utils.estimate_frequencies(filtered_alts, filtered_depths)

                    masked_times = times[good_idxs]
                    masked_freqs = freqs[good_idxs]
                    masked_depths = depths[good_idxs]
                    masked_state_Ls = state_Ls[good_idxs]

                    # Estimate appearance and fixation times
                    if masked_state_Ls[-1] in parse_file.well_mixed_fixed_states:
                        t0,tf,dt = timecourse_utils.calculate_appearance_fixation_time_from_hmm(masked_times, masked_freqs, masked_state_Ls)
                        origin_fixation_times[population][0].append(t0)
                        origin_fixation_times[population][1].append(tf)
                        origin_fixation_times[population][2].append(dt)

                    # Now split the trajectory into independent polymorphic runs
                    # each of which contains a single final state (unless end of experiment)
                    independent_runs = timecourse_utils.split_well_mixed_hmm(masked_times,masked_freqs, masked_state_Ls)
                    num_runs.append(len(independent_runs))

                    for run_idxs in independent_runs:

                        if len(run_idxs)<2:
                            # need at least one polymorphic state and one final state
                            continue
                        # initial time
                        t = masked_times[run_idxs[0]]

                        # get final state
                        final_state = masked_state_Ls[run_idxs[-1]]

                        # get frequency of parent clade during run
                        #if final_state == parse_file.well_mixed_hmm_states['F'] or final_state==parse_file.well_mixed_hmm_states['P']:
                        #    parent_freqs = masked_freqs
                        #else:
                        #parent_freqs = masked_freqs
                        #elif final_state == parse_file.clade_hmm_states['F'] or final_state == parse_file.well_mixed_hmm_states['P']:
                        #    parent_freqs = masked_fmajors
                        #elif final_state == parse_file.clade_hmm_states['F'] or final_state == parse_file.clade_hmm_states['Pm']:
                        #    parent_freqs = masked_fmajors
                        #else:
                        #    parent_freqs = masked_fextincts


                        # don't neet to renormalize the freqs because we have no population structure

                        #renormalized_freqs = np.clip(masked_freqs[run_idxs]/parent_freqs[run_idxs],0,1)

                        # get fixation weight
                        if final_state in parse_file.well_mixed_fixed_states:
                            fixation_weight = 1.0
                        elif final_state in parse_file.well_mixed_extinct_states:
                            fixation_weight = 0.0
                        else:
                            fixation_weight = masked_freqs[-1] > fstar

                        individual_bin_weights = np.exp(-np.power((masked_freqs[:,None]-frequencies[None,:])/df,2))
                        individual_bin_weights *= (individual_bin_weights>0.01)

                        bin_weights = individual_bin_weights.sum(axis=0)
                        fixation_weights = (individual_bin_weights*fixation_weight).sum(axis=0)

                        #num_in_bin += bin_weights
                        num_in_bin += bin_weights
                        avg_f += fixation_weights

                        null_num_in_bin += bin_weights
                        null_avg_f += fixation_weights


                avg_f = avg_f/(num_in_bin+(num_in_bin<1))

                ax_i.plot(frequencies[(num_in_bin>=1)], avg_f[(num_in_bin>=1)], '.-', color= pt.get_colors(treatment), marker=pt.plot_species_marker(taxon), fillstyle=pt.plot_species_fillstyle(taxon), alpha=0.9, linewidth=2.5, markersize = 8, zorder=2)
                ax_i.plot([0, 1], [0, 1], '--', c = 'black', alpha=0.9, markersize = 10, zorder=1)

                ax_i.set_xlim([0,1])
                ax_i.set_ylim([0,1])
                ax_i.set_xlabel('Allele frequency', fontsize = 14)
                ax_i.set_ylabel(r'$\mathrm{Pr}\left [ \mathrm{survival} \right ]$', fontsize = 14)

                ax_i.spines['top'].set_visible(False)

                line, = ax_i.plot([0,1],[1,1],'k:',linewidth=5)
                line.set_dashes((0.5, 0.5))

                ax_i.set_title( latex_dict[taxon], fontweight='bold', fontsize=17)

                #fig.suptitle(latex_dict[strain], fontsize=28, fontweight='bold')

            if (taxon_idx == 0):
                legend_elements = [Line2D([0], [0], ls='--', color='k', lw=1.5, label= 'Quasi-neutral'),
                                   Line2D([0], [0], ls=':', color='k', lw=1.5, label= 'Hitchhiking' )]
                ax_i.legend(handles=legend_elements, loc='upper left', fontsize=12)

    fig_name = pt.get_path() + '/figs/freq_vs_prob_fixation.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()



def plot_allele_corr_delta(min_trajectory_length=3):

    mutation_trajectories = {}
    fixed_mutation_trajectories = {}
    #transit_times = {}
    taxa = ['B', 'S']

    r2s_obs_dict = {}

    #r2s_null_dict = {}

    for treatment in ['0','1']:
        for taxon in taxa:
            r2s = []
            for replicate in replicates:

                population = treatment + taxon + replicate
                sys.stderr.write("Processing %s...\n" % population)

                mutations, depth_tuple = parse_file.parse_annotated_timecourse(population)
                population_avg_depth_times, population_avg_depths, clone_avg_depth_times, clone_avg_depths = depth_tuple
                state_times, state_trajectories = parse_file.parse_well_mixed_state_timecourse(population)

                times = mutations[0][9]
                Ms = np.zeros_like(times)*1.0
                fixed_Ms = np.zeros_like(times)*1.0

                for mutation_idx_i in range(0,len(mutations)):

                    location_i, gene_name_i, allele_i, var_type_i, test_statistic_i, pvalue_i, cutoff_idx_i, depth_fold_change_i, depth_change_pvalue_i, times_i, alts_i, depths_i, clone_times_i, clone_alts_i, clone_depths_i = mutations[mutation_idx_i]

                    state_Ls_i = state_trajectories[mutation_idx_i]
                    good_idx_i, filtered_alts_i, filtered_depths_i = timecourse_utils.mask_timepoints(times_i, alts_i, depths_i, var_type_i, cutoff_idx_i, depth_fold_change_i, depth_change_pvalue_i)
                    freqs_i = timecourse_utils.estimate_frequencies(filtered_alts_i, filtered_depths_i)

                    masked_times_i = times[good_idx_i]
                    masked_freqs_i = freqs_i[good_idx_i]
                    masked_state_Ls_i = state_Ls_i[good_idx_i]

                    P_idx_i = np.where(masked_state_Ls_i == 3)[0]
                    if len(P_idx_i) < min_trajectory_length:
                        continue
                    first_P_i = P_idx_i[0]
                    last_P_i = P_idx_i[-1]

                    masked_freqs_P_i = masked_freqs_i[first_P_i:last_P_i+1]
                    masked_times_P_i = masked_times_i[first_P_i:last_P_i+1]

                    delta_masked_freqs_P_i = masked_freqs_P_i[1:] - masked_freqs_P_i[:-1]
                    delta_masked_times_P_i = masked_times_P_i[:-1]


                    for mutation_idx_j in range(mutation_idx_i+1,len(mutations)):

                        location_j, gene_name_j, allele_j, var_type_j, test_statistic_j, pvalue_j, cutoff_jdx_j, depth_fold_change_j, depth_change_pvalue_j, times_j, alts_j, depths_j, clone_times_j, clone_alts_j, clone_depths_j = mutations[mutation_idx_j]

                        state_Ls_j = state_trajectories[mutation_idx_j]
                        good_idx_j, filtered_alts_j, filtered_depths_j = timecourse_utils.mask_timepoints(times_j, alts_j, depths_j, var_type_j, cutoff_jdx_j, depth_fold_change_j, depth_change_pvalue_j)
                        freqs_j = timecourse_utils.estimate_frequencies(filtered_alts_j, filtered_depths_j)

                        masked_times_j = times[good_idx_j]
                        masked_freqs_j = freqs_j[good_idx_j]
                        masked_state_Ls_j = state_Ls_j[good_idx_j]

                        P_jdx_j = np.where(masked_state_Ls_j == 3)[0]
                        if len(P_jdx_j) < min_trajectory_length:
                          continue
                        first_P_j = P_jdx_j[0]
                        last_P_j = P_jdx_j[-1]

                        masked_freqs_P_j = masked_freqs_j[first_P_j:last_P_j+1]
                        masked_times_P_j = masked_times_j[first_P_j:last_P_j+1]

                        delta_masked_freqs_P_j = masked_freqs_P_j[1:] - masked_freqs_P_j[:-1]
                        # delta_f = f_t_plus_1 - f_t
                        delta_masked_times_P_j = masked_times_P_j[:-1]

                        intersect_times = np.intersect1d(delta_masked_times_P_i, delta_masked_times_P_j)

                        if len(intersect_times)>=3:

                            intersect_idx_i = [np.where(delta_masked_times_P_i == intersect_time)[0][0] for intersect_time in intersect_times ]
                            intersect_delta_i = delta_masked_freqs_P_i[intersect_idx_i]

                            intersect_idx_j = [np.where(delta_masked_times_P_j == intersect_time)[0][0] for intersect_time in intersect_times ]
                            intersect_delta_j = delta_masked_freqs_P_j[intersect_idx_j]



                            if len(intersect_delta_i) != len(intersect_delta_j):
                                print(len(intersect_delta_j), len(intersect_delta_j))

                            r2 = stats.pearsonr(intersect_delta_i, intersect_delta_j)[0] ** 2
                            r2s.append(r2)

            r2s_obs_dict[treatment + taxon] = r2s

    fig = plt.figure(figsize = (12, 6))

    for i, taxon in enumerate(taxa):
            ax_i = plt.subplot2grid((1, 2), (0, i), colspan=1)

            for treatment in ['0','1']:
                r2_treatment_taxon = r2s_obs_dict[treatment+taxon]

                ax_i.hist(r2_treatment_taxon, label=pt.get_treatment_name(treatment), color= pt.get_colors(treatment), lw=5, histtype='step', bins = 30, alpha =1, weights=np.zeros_like(r2_treatment_taxon) + 1. / len(r2_treatment_taxon))
                ax_i.set_xlim([0,1] )
                ax_i.set_yscale('log', basey=10)
                ax_i.set_title(latex_dict[taxon], fontsize=18, fontweight='bold')
                ax_i.set_xlabel("Squared correlation between\nallele frequency trajectories, " + r'$\rho_{M_{\mathrm{P}}^{ (i) }, M_{\mathrm{P}}^{ (j) }  }^{2} $' , fontsize = 14)
                ax_i.set_ylabel('Frequency', fontsize = 20 )

                if i == 0:
                    ax_i.legend(loc='upper right', fontsize=12)


    fig_name = pt.get_path() + '/figs/r2_B_S.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()









#plot_allele_corr_delta()

#allele_survival()
#plot_B_S_mutation_trajectory()

#get_mult_similarity()

#plot_allele_freqs_all_treats('B')
#plot_allele_freqs_all_treats('S')
plot_allele_freqs_all_treats('D')



#plot_bPTR_all()
#temporal_coverage()
