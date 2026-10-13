import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


# ============================================================
# DATA
# ============================================================

samples = np.array([
    "A1", "A2", "A3",
    "B1", "B2", "B3",
    "C1", "C2", "C3",
    "D1", "D2", "D3",
    "E1", "E2"
])

materials = np.array([
    "Cu", "Cu", "Cu",
    "Sn", "Sn", "Sn",
    "Al2O3", "Al2O3", "Al2O3",
    "ZrO2", "ZrO2", "ZrO2",
    "Polyurethane", "Polyurethane"
])

# Porozita [%]
porosity_percent = np.array([
    96.0, 97.0, 96.8,
    91.5, 89.3, 91.5,
    83.6, 86.0, 85.1,
    86.3, 87.3, 89.0,
    96.0, 95.8
], dtype=float)

# Porozita jako bezrozměrná hodnota 0–1
porosity = porosity_percent / 100.0

# Průměrný ekvivalentní průměr pórů [mm]
de_mm = np.array([
    0.36, 0.89, 1.26,
    0.41, 0.62, 1.30,
    1.12, 1.31, 1.98,
    1.21, 1.96, 2.71,
    1.62, 2.59
], dtype=float)

# Převod na metry
de_m = de_mm / 1000.0

# Koeficient A [Pa s m^-1]
A_coeff = np.array([
    4626.70,
    6090.63,
    2112.25,
    4095.22,
    6971.14,
    3272.14,
    0.00,
    0.00,
    0.00,
    109.12,
    0.00,
    0.00,
    1783.59,
    0.00
], dtype=float)

# Koeficient B [Pa s^2 m^-2]
B_coeff = np.array([
    5149.64,
    1765.38,
    2082.14,
    2905.23,
    1970.50,
    1438.34,
    1191.99,
    1403.90,
    1231.75,
    1976.04,
    1784.36,
    1866.42,
    2768.57,
    1556.36
], dtype=float)


# ============================================================
# ROZDĚLENÍ DO SKUPIN
# ============================================================

# Skupina A+B
group_AB = np.array([
    sample[0] in ["A", "B"]
    for sample in samples
])

# Skupina C+D+E
group_CDE = np.array([
    sample[0] in ["C", "D", "E"]
    for sample in samples
])

# Nenulové hodnoty A
valid_A = A_coeff > 0.0


# ============================================================
# FYZIKÁLNĚ MOTIVOVANÉ PARAMETRY
# ============================================================

# Laminární parametr podobný Kozeny-Carman / Ergun:
#
# (1 - epsilon)^2 / (epsilon^3 * d_e^2)

ergun_A_parameter = (
    (1.0 - porosity) ** 2
    / (porosity ** 3 * de_m ** 2)
)

# Inerciální parametr podle Ergunova typu:
#
# (1 - epsilon) / (epsilon^3 * d_e)

ergun_B_parameter = (
    (1.0 - porosity)
    / (porosity ** 3 * de_m)
)


# ============================================================
# FUNKCE PRO LINEÁRNÍ REGRESI
# ============================================================

def calculate_linear_regression(x, y):
    """
    Spočítá lineární regresi:

        y = slope * x + intercept
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if len(x) < 2:
        return None

    if np.allclose(x, x[0]):
        return None

    result = linregress(x, y)

    return {
        "slope": result.slope,
        "intercept": result.intercept,
        "r": result.rvalue,
        "r2": result.rvalue ** 2,
        "p": result.pvalue,
        "stderr": result.stderr
    }


# ============================================================
# VÝPIS REGRESE
# ============================================================

def print_regression_result(title, group_name, result, n_points):

    print("\n" + "=" * 80)
    print(title)
    print(group_name)
    print("=" * 80)

    if result is None:
        print("Regresi nebylo možné spočítat.")
        return

    print(f"Počet bodů: n = {n_points}")
    print(
        f"y = {result['slope']:.6e} x "
        f"+ {result['intercept']:.6e}"
    )
    print(f"Pearson r = {result['r']:.4f}")
    print(f"R² = {result['r2']:.4f}")
    print(f"p-value = {result['p']:.4e}")


# ============================================================
# OBECNÁ FUNKCE PRO VYKRESLENÍ KORELACE
# ============================================================

def plot_grouped_correlation(
    x,
    y,
    xlabel,
    ylabel,
    title,
    valid_mask=None,
    show_invalid_as_open=False,
    scientific_x=False
):

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if valid_mask is None:
        valid_mask = np.ones(len(y), dtype=bool)

    valid_mask = np.asarray(valid_mask, dtype=bool)

    fig, ax = plt.subplots(figsize=(9, 6.5))

    # --------------------------------------------------------
    # Masky pro platné body
    # --------------------------------------------------------

    mask_AB_valid = group_AB & valid_mask
    mask_CDE_valid = group_CDE & valid_mask

    # --------------------------------------------------------
    # Platné body A+B
    # --------------------------------------------------------

    ax.scatter(
        x[mask_AB_valid],
        y[mask_AB_valid],
        s=85,
        marker="o",
        color="tab:blue",
        label="Samples A and B",
        zorder=3
    )

    # --------------------------------------------------------
    # Platné body C+D+E
    # --------------------------------------------------------

    ax.scatter(
        x[mask_CDE_valid],
        y[mask_CDE_valid],
        s=85,
        marker="s",
        color="tab:red",
        label="Samples C, D and E",
        zorder=3
    )

    # --------------------------------------------------------
    # Neplatné body, například A = 0
    # --------------------------------------------------------

    invalid_mask = ~valid_mask

    if show_invalid_as_open and np.any(invalid_mask):

        invalid_AB = group_AB & invalid_mask
        invalid_CDE = group_CDE & invalid_mask

        if np.any(invalid_AB):
            ax.scatter(
                x[invalid_AB],
                y[invalid_AB],
                s=90,
                marker="o",
                facecolors="none",
                edgecolors="tab:blue",
                linewidths=1.8,
                label=r"$A=0$, excluded from regression",
                zorder=3
            )

        if np.any(invalid_CDE):
            ax.scatter(
                x[invalid_CDE],
                y[invalid_CDE],
                s=90,
                marker="s",
                facecolors="none",
                edgecolors="tab:red",
                linewidths=1.8,
                label=r"$A=0$, excluded from regression",
                zorder=3
            )

    # --------------------------------------------------------
    # Popisky bodů
    # --------------------------------------------------------

    for xi, yi, sample in zip(x, y, samples):
        ax.annotate(
            sample,
            xy=(xi, yi),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
            zorder=4
        )

    # --------------------------------------------------------
    # Regrese pro skupinu A+B
    # --------------------------------------------------------

    regression_AB = calculate_linear_regression(
        x[mask_AB_valid],
        y[mask_AB_valid]
    )

    if regression_AB is not None:

        x_fit_AB = np.linspace(
            np.min(x[mask_AB_valid]),
            np.max(x[mask_AB_valid]),
            300
        )

        y_fit_AB = (
            regression_AB["slope"] * x_fit_AB
            + regression_AB["intercept"]
        )

        ax.plot(
            x_fit_AB,
            y_fit_AB,
            linestyle="--",
            linewidth=2,
            color="tab:blue",
            label=(
                "Linear fit A+B: "
                f"$R^2={regression_AB['r2']:.3f}$, "
                f"$r={regression_AB['r']:.3f}$"
            ),
            zorder=2
        )

    # --------------------------------------------------------
    # Regrese pro skupinu C+D+E
    # --------------------------------------------------------

    regression_CDE = calculate_linear_regression(
        x[mask_CDE_valid],
        y[mask_CDE_valid]
    )

    if regression_CDE is not None:

        x_fit_CDE = np.linspace(
            np.min(x[mask_CDE_valid]),
            np.max(x[mask_CDE_valid]),
            300
        )

        y_fit_CDE = (
            regression_CDE["slope"] * x_fit_CDE
            + regression_CDE["intercept"]
        )

        ax.plot(
            x_fit_CDE,
            y_fit_CDE,
            linestyle="--",
            linewidth=2,
            color="tab:red",
            label=(
                "Linear fit C+D+E: "
                f"$R^2={regression_CDE['r2']:.3f}$, "
                f"$r={regression_CDE['r']:.3f}$"
            ),
            zorder=2
        )

    # --------------------------------------------------------
    # Formátování grafu
    # --------------------------------------------------------

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)

    ax.grid(
        True,
        linestyle=":",
        linewidth=0.8,
        alpha=0.75
    )

    if scientific_x:
        ax.ticklabel_format(
            axis="x",
            style="sci",
            scilimits=(0, 0)
        )

    # Odstranění duplicit v legendě
    handles, labels = ax.get_legend_handles_labels()

    unique_legend = {}

    for handle, label in zip(handles, labels):
        if label not in unique_legend:
            unique_legend[label] = handle

    ax.legend(
        unique_legend.values(),
        unique_legend.keys(),
        fontsize=9,
        loc="best"
    )

    plt.tight_layout()

    # --------------------------------------------------------
    # Výpis výsledků do terminálu
    # --------------------------------------------------------

    print_regression_result(
        title=title,
        group_name="Group A+B",
        result=regression_AB,
        n_points=np.sum(mask_AB_valid)
    )

    print_regression_result(
        title=title,
        group_name="Group C+D+E",
        result=regression_CDE,
        n_points=np.sum(mask_CDE_valid)
    )


# ============================================================
# GRAF 1: A VS POROZITA
# ============================================================

plot_grouped_correlation(
    x=porosity_percent,
    y=A_coeff,
    xlabel="Porosity [%]",
    ylabel=r"Coefficient $A$ [Pa s m$^{-1}$]",
    title=r"Dependence of coefficient $A$ on porosity",
    valid_mask=valid_A,
    show_invalid_as_open=True
)


# ============================================================
# GRAF 2: B VS POROZITA
# ============================================================

plot_grouped_correlation(
    x=porosity_percent,
    y=B_coeff,
    xlabel="Porosity [%]",
    ylabel=r"Coefficient $B$ [Pa s$^2$ m$^{-2}$]",
    title=r"Dependence of coefficient $B$ on porosity"
)


# ============================================================
# GRAF 3: A VS PRŮMĚR PÓRŮ
# ============================================================

plot_grouped_correlation(
    x=de_mm,
    y=A_coeff,
    xlabel=r"Average equivalent pore diameter $d_e$ [mm]",
    ylabel=r"Coefficient $A$ [Pa s m$^{-1}$]",
    title=r"Dependence of coefficient $A$ on $d_e$",
    valid_mask=valid_A,
    show_invalid_as_open=True
)


# ============================================================
# GRAF 4: B VS PRŮMĚR PÓRŮ
# ============================================================

plot_grouped_correlation(
    x=de_mm,
    y=B_coeff,
    xlabel=r"Average equivalent pore diameter $d_e$ [mm]",
    ylabel=r"Coefficient $B$ [Pa s$^2$ m$^{-2}$]",
    title=r"Dependence of coefficient $B$ on $d_e$"
)


# ============================================================
# GRAF 5: A VS LAMINÁRNÍ ERGUNŮV PARAMETR
# ============================================================

plot_grouped_correlation(
    x=ergun_A_parameter,
    y=A_coeff,
    xlabel=(
        r"Laminar structure parameter "
        r"$(1-\varepsilon)^2/(\varepsilon^3 d_e^2)$ [m$^{-2}$]"
    ),
    ylabel=r"Coefficient $A$ [Pa s m$^{-1}$]",
    title=r"Coefficient $A$ versus laminar structure parameter",
    valid_mask=valid_A,
    show_invalid_as_open=True,
    scientific_x=True
)


# ============================================================
# GRAF 6: B VS INERCIÁLNÍ ERGUNŮV PARAMETR
# ============================================================

plot_grouped_correlation(
    x=ergun_B_parameter,
    y=B_coeff,
    xlabel=(
        r"Inertial structure parameter "
        r"$(1-\varepsilon)/(\varepsilon^3 d_e)$ [m$^{-1}$]"
    ),
    ylabel=r"Coefficient $B$ [Pa s$^2$ m$^{-2}$]",
    title=r"Coefficient $B$ versus inertial structure parameter",
    scientific_x=True
)


# ============================================================
# ZOBRAZENÍ VŠECH ŠESTI GRAFŮ
# ============================================================

plt.show()