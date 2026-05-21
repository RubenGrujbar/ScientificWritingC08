import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def get_colors(n):
    return [cm.gist_rainbow(i / max(n - 1, 1)) for i in range(n)]


def _plot_vz_into_ax(ax, df, y_target, x_start, x_end, x_step):
    col_x, col_y, col_z, col_w = 'x [mm]', 'y [mm]', 'z [mm]', 'Velocity w [m/s]'

    actual_y = df.iloc[(df[col_y] - y_target).abs().argsort()[:1]][col_y].values[0]
    df_y     = df[df[col_y] == actual_y]

    target_xs = np.arange(x_start, x_end + x_step * 0.1, x_step)
    colors    = get_colors(len(target_xs))

    for tx, color in zip(target_xs, colors):
        actual_x = df_y.iloc[(df_y[col_x] - tx).abs().argsort()[:1]][col_x].values[0]
        if abs(actual_x - tx) > 2.0:
            continue

        df_x = df_y[df_y[col_x] == actual_x].sort_values(col_z)
        z_vals, vz_vals = df_x[col_z].values, df_x[col_w].values

        integral_val = np.trapz(vz_vals, x=z_vals)
        ax.plot(vz_vals, z_vals,
                label=f"x ≈ {actual_x:.1f} mm  |  $I_{{VR}}$ = {integral_val:.2f}",
                color=color, linewidth=1.5)

    ax.set_title(f"Vertical Velocity ($v$) Profiles at $y \\approx 250$ mm", fontsize=13)
    ax.set_xlabel("Velocity $v$ (m/s)", fontsize=12)
    ax.set_ylabel("$z$ (mm)", fontsize=12)
    ax.axvline(0, color='black', linewidth=1, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10, title="Position & Integral", title_fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)


def _plot_ub_into_ax(ax, df, y_target, x_min, x_max, z_start, z_end, z_step):
    col_x, col_y, col_z, col_u = 'x [mm]', 'y [mm]', 'z [mm]', 'Velocity u [m/s]'

    actual_y = df.iloc[(df[col_y] - y_target).abs().argsort()[:1]][col_y].values[0]
    df_y     = df[df[col_y] == actual_y]

    target_zs = np.arange(z_start, z_end - z_step * 0.1, -z_step)
    colors    = get_colors(len(target_zs))

    for tz, color in zip(target_zs, colors):
        actual_z = df_y.iloc[(df_y[col_z] - tz).abs().argsort()[:1]][col_z].values[0]
        if abs(actual_z - tz) > z_step / 2:
            continue

        df_z = df_y[(df_y[col_z] == actual_z) &
                    df_y[col_x].between(x_min, x_max)].sort_values(col_x)
        x_vals, vx_vals = df_z[col_x].values, df_z[col_u].values

        if len(x_vals) < 2:
            continue

        integral_val = np.trapz(vx_vals, x=x_vals)
        ax.plot(vx_vals, x_vals,
                label=f"z ≈ {actual_z:.1f} mm  |  $I_{{HU}}$ = {integral_val:.1f}",
                color=color, linewidth=1.5)

    ax.set_title(f"Horizontal Velocity ($u$) Profiles at $y \\approx 250$ mm", fontsize=13)
    ax.set_xlabel("Velocity $u$ (m/s)", fontsize=12)
    ax.set_ylabel("Chordwise Position $x$ (mm)", fontsize=12)
    ax.axvline(0, color='black', linewidth=1, linestyle='--', alpha=0.7)
    ax.set_ylim(x_max, x_min)
    ax.set_xlim(6, 7.5)
    ax.legend(fontsize=10, title="Height ($z$) & Integral", title_fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)


def plot_combined(filename,
                  vz_y=300, vz_x_start=130, vz_x_end=175, vz_x_step=6,
                  ub_y=250, ub_x_min=0, ub_x_max=160,
                  ub_z_start=-25, ub_z_end=-60, ub_z_step=4.5):

    df = pd.read_csv(filename, skipinitialspace=True)
    df.columns = df.columns.str.strip()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    _plot_vz_into_ax(ax1, df, vz_y, vz_x_start, vz_x_end, vz_x_step)
    _plot_ub_into_ax(ax2, df, ub_y, ub_x_min, ub_x_max, ub_z_start, ub_z_end, ub_z_step)

    #fig.suptitle("Velocity Profiles — NACA 0015", fontsize=14, y=1.01)
    fig.tight_layout()

    out = "combined_velocity_profiles.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved → {out}")
    plt.show()


if __name__ == "__main__":
    plot_combined("Dataset NACA0015 Velocity and Standard deviation.csv")