import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import lsq_linear
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "plots"

# Převodní rovnice snímače:
# tlaková ztráta [Pa] = 24783 * proud [mA] - 109141
CALIBRATION_SLOPE = 24783
CALIBRATION_INTERCEPT = -109141

# Vlastnosti média a geometrie průtočného průřezu
# Voda při pokojové teplotě (~20 °C)
WATER_DENSITY_KG_M3 = 998.2
CHANNEL_WIDTH_M = 0.040
CHANNEL_HEIGHT_M = 0.015
FLOW_AREA_M2 = CHANNEL_WIDTH_M * CHANNEL_HEIGHT_M


# ============================================================================
# NAMĚŘENÁ DATA
#
# flow_kg_s = hmotnostní průtok [kg/s]
# current_mA = výstup snímače diferenčního tlaku [mA]
# ============================================================================

data = {
    "A1": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.4025,
            0.7782,
            1.1404,
            1.4758,
            1.5965,
            1.8783,
            2.0528,
            2.3077
        ],
        "current_mA": [
            4.0,
            4.5,
            5.0,
            5.6,
            6.1,
            6.4,
            7.0,
            7.5,
            8.2
        ]
    }),

    "A2": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.8318,
            1.3551,
            1.6771,
            1.8783,
            2.0259,
            2.2138,
            2.3479
        ],
        "current_mA": [
            4.0,
            4.8,
            5.3,
            5.7,
            6.0,
            6.0,
            6.3,
            6.4
        ]
    }),

    "A3": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.8989,
            1.2209,
            1.4892,
            1.7710,
            1.9722,
            2.2674,
            2.3345
        ],
        "current_mA": [
            4.0,
            4.7,
            4.9,
            5.1,
            5.5,
            5.6,
            5.9,
            6.0
        ]
    }),

    "B1": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            1.0331,
            1.3148,
            1.6637,
            1.8783,
            1.9991,
            2.2254,
            2.3345
        ],
        "current_mA": [
            4.0,
            4.9,
            5.3,
            5.8,
            6.2,
            6.4,
            6.6,
            6.7
        ]
    }),

    "B2": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.8184,
            1.1941,
            1.4624,
            1.8381,
            2.0662,
            2.3211
        ],
        "current_mA": [
            4.0,
            4.9,
            5.3,
            5.6,
            6.0,
            6.3,
            6.7
        ]
    }),

    "B3": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.9392,
            1.4892,
            1.8112,
            2.2540,
            2.3479
        ],
        "current_mA": [
            4.0,
            4.7,
            5.1,
            5.4,
            5.7,
            5.8
        ]
    }),

    "C1": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            1.2209,
            1.5697,
            2.0125,
            2.3613
        ],
        "current_mA": [
            4.0,
            4.5,
            4.6,
            5.0,
            5.2
        ]
    }),

    "C2": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            1.3551,
            1.9588,
            2.2406,
            2.3345
        ],
        "current_mA": [
            4.0,
            4.6,
            5.0,
            5.2,
            5.3
        ]
    }),

    "C3": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            1.2880,
            1.6771,
            2.0528,
            2.3211
        ],
        "current_mA": [
            4.0,
            4.6,
            4.7,
            5.0,
            5.2
        ]
    }),

    "D1": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.7379,
            1.3014,
            1.7576,
            2.0528,
            2.3345
        ],
        "current_mA": [
            4.0,
            4.5,
            4.8,
            5.1,
            5.4,
            5.6
        ]
    }),

    "D2": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.5903,
            0.9928,
            1.5966,
            1.8917,
            2.3077
        ],
        "current_mA": [
            4.0,
            4.4,
            4.6,
            4.9,
            5.1,
            5.5
        ]
    }),

    "D3": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.6306,
            1.4892,
            1.8917,
            2.2674,
            2.3379
        ],
        "current_mA": [
            4.0,
            4.4,
            4.9,
            5.2,
            5.5,
            5.5
        ]
    }),

    "E1": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.8050,
            1.2209,
            1.4356,
            2.0796,
            2.2808
        ],
        "current_mA": [
            4.0,
            4.6,
            5.0,
            5.3,
            6.1,
            6.2
        ]
    }),

    "E2": pd.DataFrame({
        "flow_kg_s": [
            0.0000,
            0.7782,
            1.3014,
            2.0259,
            2.3211
        ],
        "current_mA": [
            4.0,
            4.4,
            4.7,
            5.2,
            5.3
        ]
    })
}


# ============================================================================
# PŘEVOD mA NA TLAKOVOU ZTRÁTU
# ============================================================================

def current_to_pressure_drop(current_mA):
    """
    Převod proudu snímače [mA] na tlakovou ztrátu [Pa].

    Použitá kalibrační rovnice:
        dp = 24783 * current_mA - 109141

    Záporné hodnoty jsou považovány za chybu měření nebo kalibrace
    a jsou nahrazeny nulou.
    """

    current_mA = np.asarray(current_mA, dtype=float)

    pressure_drop_pa = (
        CALIBRATION_SLOPE * current_mA
        + CALIBRATION_INTERCEPT
    )

    # Všechny záporné tlakové ztráty nastavíme na nulu
    pressure_drop_pa = np.maximum(pressure_drop_pa, 0.0)

    return pressure_drop_pa


# ============================================================================
# ZPRACOVÁNÍ DAT
# ============================================================================

def process_data(dataset):
    """
    Doplní do každého DataFrame tlakovou ztrátu v Pa.

    Současně:
    - nastaví dp = 0 Pa při nulovém průtoku,
    - odstraní případné záporné tlakové ztráty,
    - seřadí data podle průtoku.
    """

    processed_data = {}

    for sample_name, original_df in dataset.items():

        # Kopie, aby se neměnila původní data neočekávaným způsobem
        df = original_df.copy()

        # Kontrola délky sloupců
        if len(df["flow_kg_s"]) != len(df["current_mA"]):
            raise ValueError(
                f"Vzorek {sample_name}: počet hodnot průtoku a mA se neshoduje."
            )

        # Převod mA na Pa
        df["pressure_drop_pa"] = current_to_pressure_drop(
            df["current_mA"]
        )

        # Převod hmotnostního průtoku na střední rychlost proudění:
        # v = m_dot / (rho * S)
        df["velocity_m_s"] = (
            df["flow_kg_s"]
            / (WATER_DENSITY_KG_M3 * FLOW_AREA_M2)
        )

        # Při nulovém průtoku musí být tlaková ztráta přesně nula
        zero_flow_mask = np.isclose(
            df["flow_kg_s"],
            0.0,
            atol=1e-12
        )

        df.loc[zero_flow_mask, "pressure_drop_pa"] = 0.0

        # Dodatečná ochrana proti záporným hodnotám
        df["pressure_drop_pa"] = df["pressure_drop_pa"].clip(lower=0.0)

        # Seřazení podle průtoku
        df = df.sort_values("flow_kg_s").reset_index(drop=True)

        processed_data[sample_name] = df

    return processed_data


# ============================================================================
# ROZDĚLENÍ VZORKŮ DO SKUPIN
# ============================================================================

def create_sample_groups(dataset):
    """
    Automaticky rozdělí vzorky podle prvního písmene názvu.

    Například:
        A1, A2, A3 -> skupina A
        B1, B2, B3 -> skupina B
    """

    groups = {}

    for sample_name in dataset:
        group_name = sample_name[0].upper()

        if group_name not in groups:
            groups[group_name] = []

        groups[group_name].append(sample_name)

    # Seřazení názvů vzorků uvnitř každé skupiny
    for group_name in groups:
        groups[group_name] = sorted(groups[group_name])

    return groups


# ============================================================================
# TVORBA GRAFŮ
# ============================================================================

def plot_sample_groups(dataset):
    """
    Vytvoří jeden graf pro každou skupinu vzorků.

    Naměřené hodnoty jsou zobrazené jako samostatné body.
    Každý vzorek je proložen křivkou:

        Δp = A*v + B*v²

    kde v je střední rychlost proudění v průřezu 40 × 15 mm.
    Fit je vynucený přes počátek, tedy Δp(0) = 0,
    a koeficienty jsou omezené podmínkami A >= 0 a B >= 0.

    Ke každému bodu je vykreslen svislý error bar ±5 % z Δp.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    groups = create_sample_groups(dataset)

    print("\n" + "=" * 96)
    print("KOEFICIENTY FITU: Δp = A*v + B*v²")
    print("=" * 96)
    print(
        f"{'Vzorek':<10}"
        f"{'A [Pa·s/m]':>22}"
        f"{'B [Pa·s²/m²]':>24}"
        f"{'R²':>12}"
    )
    print("-" * 96)

    for group_name, sample_names in sorted(groups.items()):
        fig, ax = plt.subplots(figsize=(8, 6))

        for sample_name in sample_names:
            df = dataset[sample_name]

            velocity = df["velocity_m_s"].to_numpy(dtype=float)
            pressure_drop = df["pressure_drop_pa"].to_numpy(dtype=float)

            # Fit Δp = A*v + B*v² bez konstantního členu.
            fit_matrix = np.column_stack((velocity, velocity**2))

            # Omezený fit: A >= 0, B >= 0.
            # Tím je zachováno Δp(0) = 0 a křivka je fyzikálně smysluplná.
            fit_result = lsq_linear(
                fit_matrix,
                pressure_drop,
                bounds=(0.0, np.inf),
                method="trf"
            )

            if not fit_result.success:
                raise RuntimeError(
                    f"Fit pro vzorek {sample_name} selhal: {fit_result.message}"
                )

            A, B = fit_result.x

            pressure_drop_predicted = (
                A * velocity
                + B * velocity**2
            )

            # R² počítané z naměřených bodů.
            ss_res = np.sum(
                (pressure_drop - pressure_drop_predicted)**2
            )
            ss_tot = np.sum(
                (pressure_drop - np.mean(pressure_drop))**2
            )

            if np.isclose(ss_tot, 0.0):
                r_squared = np.nan
            else:
                r_squared = 1.0 - ss_res / ss_tot

            print(
                f"{sample_name:<10}"
                f"{A:>22.6e}"
                f"{B:>24.6e}"
                f"{r_squared:>12.4f}"
            )

            # Relativní chyba měření tlakové ztráty: ±5 %.
            # Pro nulový bod je absolutní chyba rovna nule.
            pressure_drop_error = 0.05 * pressure_drop

            # Body se svislými error bary, bez spojnice mezi body.
            errorbar_container = ax.errorbar(
                velocity,
                pressure_drop,
                yerr=pressure_drop_error,
                fmt="o",
                linestyle="none",
                markersize=6,
                capsize=4,
                capthick=1.2,
                elinewidth=1.2,
                label=sample_name,
                zorder=3
            )

            # Stejná barva bodů, error barů a fitu pro daný vzorek.
            sample_color = errorbar_container.lines[0].get_color()

            # Hladká fitovací křivka.
            velocity_fit = np.linspace(
                0.0,
                velocity.max(),
                300
            )

            pressure_drop_fit = (
                A * velocity_fit
                + B * velocity_fit**2
            )

            # Numerická ochrana proti zanedbatelným záporným hodnotám.
            pressure_drop_fit = np.maximum(pressure_drop_fit, 0.0)

            ax.plot(
                velocity_fit,
                pressure_drop_fit,
                linewidth=2.0,
                color=sample_color,
                label="_nolegend_",
                zorder=2
            )

        ax.set_xlabel("Flow velocity [m/s]", fontsize=12)
        ax.set_ylabel("Pressure drop [Pa]", fontsize=12)
        ax.set_title(
            f"Pressure drop – sample group {group_name}",
            fontsize=13
        )

        ax.set_xlim(left=0.0)
        ax.set_ylim(bottom=0.0)

        ax.grid(
            visible=True,
            which="major",
            linestyle="--",
            linewidth=0.7,
            alpha=0.5
        )

        ax.legend(
            title="Sample",
            fontsize=10,
            title_fontsize=10
        )

        fig.tight_layout()

        output_file = (
            OUTPUT_DIR
            / f"group_{group_name}_pressure_drop_velocity.png"
        )

        fig.savefig(
            output_file,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close(fig)

        print(f"Graf uložen: {output_file}")


# ============================================================================
# VÝPIS ZPRACOVANÝCH DAT
# ============================================================================

def print_processed_data(dataset):
    """
    Vypíše zpracovaná data do terminálu pro kontrolu.
    """

    for sample_name, df in sorted(dataset.items()):
        print("\n" + "=" * 70)
        print(f"Vzorek: {sample_name}")
        print("=" * 70)

        print(
            df.to_string(
                index=False,
                formatters={
                    "flow_kg_s": lambda x: f"{x:.4f}",
                    "current_mA": lambda x: f"{x:.2f}",
                    "pressure_drop_pa": lambda x: f"{x:.1f}",
                    "velocity_m_s": lambda x: f"{x:.4f}"
                }
            )
        )


# ============================================================================
# HLAVNÍ ČÁST PROGRAMU
# ============================================================================

def main():

    # Převod a vyčištění dat
    processed_data = process_data(data)

    # Výpis tabulek do terminálu
    print_processed_data(processed_data)

    # Vytvoření grafů podle skupin A, B, C, D, E
    plot_sample_groups(processed_data)

    print("\nHotovo.")
    print(f"Grafy jsou uložené ve složce: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()