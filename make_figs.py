import os

import matplotlib.gridspec
import matplotlib.pyplot as plt

import numpy as np

import behavior.fig
import behavior.data

import simulation.data
# from fit.compute import BackupFit  # Needed by pickle

import analysis.simulation
import analysis.batch.simulation
import analysis.dynamics.separate

import fit.exemplary_cases
import fit.data
import fit.fig


def xp_fig(force=False):

    fit_data = fit.data.get_customized(force=force)
    behavior_data = behavior.data.get(force=force)

    # --------- Clustered figure ------------------ #

    n_rows, n_cols = 2, 1

    fig = plt.figure(figsize=(10, 8), dpi=200)
    gs = matplotlib.gridspec.GridSpec(nrows=n_rows, ncols=n_cols, height_ratios=[2, 1.])

    # ------------------ BEHAVIOR ---------------------- #

    gs_behavior = matplotlib.gridspec.GridSpecFromSubplotSpec(subplot_spec=gs[0, 0], ncols=1, nrows=1)
    behavior.fig.plot(data=behavior_data, subplot_spec=gs_behavior[0, 0])

    # ------------------- FIT ------------------------------ #

    gs_fit = matplotlib.gridspec.GridSpecFromSubplotSpec(subplot_spec=gs[1, 0], ncols=2, nrows=1, width_ratios=[1.1, 1])
    # GridSpec(nrows=n_rows, ncols=n_cols, width_ratios=[1, 0.7])

    # --------- Score distribution ---------------- #

    fit.fig.scores_distribution(fit_data, subplot_spec=gs_fit[0, 0])

    # --------- Correlations --------------- #

    corr = [np.corrcoef(d) for d in fit_data]

    fit.fig.correlations(corr, subplot_spec=gs_fit[0, 1])

    # --------- Numbering ------------------ #

    plt.tight_layout()
    # gs.tight_layout(fig)

    ax = fig.add_subplot(gs[:, :], zorder=-10)

    plt.axis("off")
    ax.text(
        s="A", x=-0.06, y=0.4, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    ax.text(
        s="B", x=-0.06, y=-0.1, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    ax.text(
        s="C", x=0.55, y=-0.1, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    plt.savefig("fig/xp.pdf")
    plt.show()


def simulation_fig(force=False, span_pool=0.33, t_max_pool=100, t_max_xp=25,
                   random_params=False, force_params=False, fig_name="fig/simulation.pdf"):

    pool_bkp = simulation.data.pool(force=force, t_max=t_max_pool, random=random_params, force_params=force_params)
    batch_bkp = simulation.data.batch(force=force, t_max=t_max_xp, random=random_params, force_params=force_params)

    heuristics = simulation.data.get_heuristics()

    fig = plt.figure(figsize=(13.5, 7))

    gs = matplotlib.gridspec.GridSpec(nrows=len(heuristics), ncols=1)

    for i, h in enumerate(heuristics):

        gs_h = matplotlib.gridspec.GridSpecFromSubplotSpec(nrows=1, ncols=2, width_ratios=[1.5, 1],
                                                           subplot_spec=gs[i, 0])

        analysis.simulation.distance_price_and_profit(pool_backup=pool_bkp[h], subplot_spec=gs_h[0, 0], span=span_pool)
        analysis.batch.simulation.plot(batch_backup=batch_bkp[h], subplot_spec=gs_h[0, 1])

    plt.tight_layout()

    ax = fig.add_subplot(gs[:, :], zorder=-10)

    plt.axis("off")
    ax.text(
        s="A", x=-0.05, y=0.7, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)
    ax.text(
        s="B", x=0.58, y=0.7, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)
    ax.text(
        s="C", x=-0.05, y=0.3, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)
    ax.text(
        s="D", x=0.58, y=0.3, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)
    ax.text(
        s="E", x=-0.05, y=-0.05, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)
    ax.text(
        s="F", x=0.58, y=-0.05, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    plt.savefig(fig_name)
    plt.show()


def dynamics_fig(force=False):

    xp_examples = fit.exemplary_cases.get(force=force)
    sim_examples = simulation.data.individual(force=force)

    fig = plt.figure(figsize=(10, 10), dpi=200)
    gs = matplotlib.gridspec.GridSpec(
        nrows=6, ncols=5,
        width_ratios=[0.13, 1, 1, 1, 1],
        height_ratios=[0.13, 1.2, 0.02, 1.2, 0.02, 1.2])

    # First row

    analysis.dynamics.separate.eeg_like(
        backup=sim_examples["max_profit"]["25"], subplot_spec=gs[1, 1])

    analysis.dynamics.separate.eeg_like(
        backup=xp_examples["max_profit"]["25"], subplot_spec=gs[1, 2])

    analysis.dynamics.separate.eeg_like(
        backup=sim_examples["max_profit"]["50"], subplot_spec=gs[1, 3])

    analysis.dynamics.separate.eeg_like(
        backup=xp_examples["max_profit"]["50"], subplot_spec=gs[1, 4])

    # Second row

    analysis.dynamics.separate.eeg_like(
        backup=sim_examples["max_diff"]["25"], subplot_spec=gs[3, 1])

    analysis.dynamics.separate.eeg_like(
        backup=xp_examples["max_diff"]["25"], subplot_spec=gs[3, 2])

    analysis.dynamics.separate.eeg_like(
        backup=sim_examples["max_diff"]["50"], subplot_spec=gs[3, 3])

    analysis.dynamics.separate.eeg_like(
        backup=xp_examples["max_diff"]["50"], subplot_spec=gs[3, 4])

    # Third row

    analysis.dynamics.separate.eeg_like(
        backup=sim_examples["tacit_collusion"]["25"], subplot_spec=gs[5, 1])

    analysis.dynamics.separate.eeg_like(
        backup=xp_examples["tacit_collusion"]["25"], subplot_spec=gs[5, 2])

    analysis.dynamics.separate.eeg_like(
        backup=sim_examples["tacit_collusion"]["50"], subplot_spec=gs[5, 3])

    analysis.dynamics.separate.eeg_like(
        backup=xp_examples["tacit_collusion"]["50"], subplot_spec=gs[5, 4])

    ax = fig.add_subplot(gs[:, :], zorder=-10)

    plt.axis("off")

    L, R = 0.3, 0.8
    shift = 0.14

    # Top left
    ax.text(
        s="$r=0.25$", x=L, y=1, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes,
        fontsize=15)
    ax.text(
        s="Sim.", x=L-shift*0.9, y=0.97, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes,
        fontsize=13)
    ax.text(
        s="Exp.", x=L+shift, y=0.97, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes,
        fontsize=13)

    # Top right
    ax.text(
        s="$r=0.50$", x=R, y=1, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes,
        fontsize=15)

    ax.text(
        s="Sim.", x=R-shift*0.9, y=0.97, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes,
        fontsize=13)
    ax.text(
        s="Exp.", x=R+shift, y=0.97, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes,
        fontsize=13)

    # Side

    ax.text(
        s="Profit max.", x=0, y=0.8, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=15, rotation='vertical')
    ax.text(
        s="Diff max.", x=0, y=0.45, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=15, rotation='vertical')
    ax.text(
        s="Tacit collusion", x=0, y=0.1, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=15, rotation='vertical')

    # Letters

    left, right = 0.05, 0.54

    first_r, second_r, third_r = 0.64, 0.3, -0.04

    ax.text(
        s="A", x=left, y=first_r, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    ax.text(
        s="B", x=right, y=first_r, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    ax.text(
        s="C", x=left, y=second_r, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    ax.text(
        s="D", x=right, y=second_r, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    ax.text(
        s="E", x=left, y=third_r, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    ax.text(
        s="F", x=right, y=third_r, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        fontsize=20)

    plt.tight_layout(pad=1)
    plt.savefig("fig/dynamics.pdf")
    plt.show()


def main():

    os.makedirs('fig', exist_ok=True)
    dynamics_fig(force=False)
    simulation_fig(force=False)
    xp_fig(force=False)
    print('Done!')


if __name__ == "__main__":
    main()
