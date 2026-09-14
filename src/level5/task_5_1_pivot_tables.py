"""Task 5.1: Pivot Tables - Station-Level Analysis Across Route Types.

Analytical Question:
"Which stations across Indian Railways serve the highest volume of Long-route (>4h)
inter-state trains versus Short-route (<=80m) suburban/local trains, and how do major
metropolitan junctions differ in their traffic composition?"

Methodology:
Build a multi-dimensional pivot table indexing on Station_Code and canonical Station_Name,
column-grouped by Route_Type ('Short', 'Medium', 'Long'), aggregating unique Train_No counts.
Reconcile row totals against Task 2.4 station frequency table (outputs/tables/task_2_4_station_frequency.csv).
Highlight top stations per service category.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

VERIFIED_DATA_PATH = Path("data/processed/dataset_verified.csv")
STATION_FREQ_PATH = Path("outputs/tables/task_2_4_station_frequency.csv")
OUTPUT_TABLE_PATH = Path("outputs/tables/task_5_1_station_pivot.csv")
SCREENSHOT_PATH = Path("screenshots/level5/task_5_1.png")
DOCS_PATH = Path("documentation/level5/task_5_1.txt")


def generate_station_pivot_table():
    """Generate and validate station-by-route-type pivot table."""
    print("=" * 70)
    print("TASK 5.1: STATION PIVOT TABLE ANALYSIS (ROUTE TYPE COMPOSITION)")
    print("=" * 70)

    # 1. Load input datasets
    print("\nLoading input datasets...")
    df_ver = pd.read_csv(VERIFIED_DATA_PATH, dtype=str, keep_default_na=False)
    df_freq = pd.read_csv(STATION_FREQ_PATH)

    print(f"[DATA FACT] Total Stop Rows Loaded: {len(df_ver):,}")
    print(f"[DATA FACT] Total Canonical Stations Ingested: {len(df_freq):,}")

    # Build canonical Station_Name dictionary from Task 2.4
    canonical_names = df_freq.set_index("Station_Code")["Station_Name"].to_dict()

    # 2. Build Pivot Table: Station_Code x Route_Type -> nunique(Train_No)
    pivot = pd.pivot_table(
        df_ver,
        index="Station_Code",
        columns="Route_Type",
        values="Train_No",
        aggfunc="nunique",
        fill_value=0
    )[["Short", "Medium", "Long"]]

    # Map canonical name and compute total distinct trains
    pivot["Station_Name"] = pivot.index.map(canonical_names)
    pivot["Total_Distinct_Trains"] = pivot["Short"] + pivot["Medium"] + pivot["Long"]

    # Compute percentage composition
    pivot["Pct_Short"] = (pivot["Short"] / pivot["Total_Distinct_Trains"] * 100.0).round(1)
    pivot["Pct_Medium"] = (pivot["Medium"] / pivot["Total_Distinct_Trains"] * 100.0).round(1)
    pivot["Pct_Long"] = (pivot["Long"] / pivot["Total_Distinct_Trains"] * 100.0).round(1)

    # Sort descending by Total_Distinct_Trains
    pivot = pivot.sort_values(by="Total_Distinct_Trains", ascending=False).reset_index()

    # Column ordering
    ordered_cols = [
        "Station_Code", "Station_Name", "Short", "Medium", "Long",
        "Total_Distinct_Trains", "Pct_Short", "Pct_Medium", "Pct_Long"
    ]
    pivot = pivot[ordered_cols]

    # 3. Reconciliation Testing with Task 2.4
    print("\n--- RECONCILIATION AUDIT WITH TASK 2.4 ---")
    merged_audit = pd.merge(pivot, df_freq, on="Station_Code")
    assert len(merged_audit) == 8147, f"Station count mismatch: {len(merged_audit)}"

    diffs = (merged_audit["Total_Distinct_Trains"] != merged_audit["Train_Count"]).sum()
    print(f"[VALIDATION] Row total mismatches against Task 2.4 Train_Count: {diffs}")
    assert diffs == 0, f"Found {diffs} mismatches between pivot totals and Task 2.4 station frequencies!"
    print("[VALIDATION] 100% PERFECT RECONCILIATION: All 8,147 station totals match Task 2.4 exactly.")

    # 4. Spot-Checks
    print("\n--- SPOT CHECKS ---")
    # Spot-check CSMT (Short route dominance)
    csmt = pivot[pivot["Station_Code"] == "CSMT"].iloc[0]
    print(f"[VALIDATION] CSMT: Short={csmt['Short']}, Medium={csmt['Medium']}, Long={csmt['Long']} -> Total={csmt['Total_Distinct_Trains']}")
    assert csmt["Short"] == 804 and csmt["Medium"] == 138 and csmt["Long"] == 85

    # Spot-check BZA (Long route dominance)
    bza = pivot[pivot["Station_Code"] == "BZA"].iloc[0]
    print(f"[VALIDATION] BZA: Short={bza['Short']}, Medium={bza['Medium']}, Long={bza['Long']} -> Total={bza['Total_Distinct_Trains']}")
    assert bza["Long"] == 316 and bza["Short"] == 31 and bza["Medium"] == 69

    # Spot-check SDAH (Medium route dominance)
    sdah = pivot[pivot["Station_Code"] == "SDAH"].iloc[0]
    print(f"[VALIDATION] SDAH: Short={sdah['Short']}, Medium={sdah['Medium']}, Long={sdah['Long']} -> Total={sdah['Total_Distinct_Trains']}")
    assert sdah["Medium"] == 348 and sdah["Short"] == 339 and sdah["Long"] == 58

    # 5. Summary Highlights
    print("\n" + "=" * 70)
    print("TOP 10 STATIONS BY TOTAL TRAIN VOLUME & ROUTE COMPOSITION")
    print("=" * 70)
    print(pivot.head(10).to_string(index=False))

    print("\n" + "=" * 70)
    print("TOP 5 STATIONS BY LONG-ROUTE TRAINS (TRUNK CORRIDOR ARTERIES)")
    print("=" * 70)
    top_long = pivot.sort_values(by="Long", ascending=False).head(5)
    print(top_long[["Station_Code", "Station_Name", "Long", "Pct_Long", "Total_Distinct_Trains"]].to_string(index=False))

    print("\n" + "=" * 70)
    print("TOP 5 STATIONS BY SHORT-ROUTE TRAINS (SUBURBAN / COMMUTER HUBS)")
    print("=" * 70)
    top_short = pivot.sort_values(by="Short", ascending=False).head(5)
    print(top_short[["Station_Code", "Station_Name", "Short", "Pct_Short", "Total_Distinct_Trains"]].to_string(index=False))

    print("\n" + "=" * 70)
    print("TOP 5 STATIONS BY MEDIUM-ROUTE TRAINS (REGIONAL EXPRESS HUBS)")
    print("=" * 70)
    top_med = pivot.sort_values(by="Medium", ascending=False).head(5)
    print(top_med[["Station_Code", "Station_Name", "Medium", "Pct_Medium", "Total_Distinct_Trains"]].to_string(index=False))

    # 6. Save Output Table
    OUTPUT_TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    pivot.to_csv(OUTPUT_TABLE_PATH, index=False)
    print(f"\n[OUTPUT] Saved station pivot table: {OUTPUT_TABLE_PATH} ({len(pivot)} rows)")

    # 7. Generate Visual Evidence Screenshot
    create_evidence_screenshot(pivot)

    # 8. Generate Documentation Note
    write_documentation_note(pivot, top_long, top_short, top_med)

    print("\nTask 5.1 completed successfully.")
    return pivot


def create_evidence_screenshot(pivot: pd.DataFrame):
    """Render terminal / summary card visualization for screenshot artifact."""
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")
    ax.axis("off")

    # Title header
    fig.text(0.05, 0.93, "Sysslan IT Solutions Internship — Task 5.1 Evidence",
             color="#61afef", fontsize=16, fontweight="bold", fontfamily="monospace")
    fig.text(0.05, 0.88, "Pivot Table Analysis: Station-Level Route Type Composition & Hub Profiling",
             color="#abb2bf", fontsize=11, fontfamily="monospace")

    # Metrics summary banner
    banner_text = (
        "Analytical Question: 'Which stations serve the most Long-route vs. Short-route trains?'\n"
        "Input: data/processed/dataset_verified.csv (8,147 canonical stations, 11,113 unique trains)\n"
        "Long-Route Leaders: BZA (316), BRC (307), CNB (295) | Short-Route Leaders: CSMT (804), TNA (521), MSB (484)"
    )
    fig.text(0.05, 0.75, banner_text, color="#98c379", fontsize=9.5, fontfamily="monospace",
             bbox=dict(boxstyle="round,pad=0.6", facecolor="#282c34", edgecolor="#61afef", alpha=0.9))

    # Top 12 stations table
    top12 = pivot.head(12)[["Station_Code", "Station_Name", "Short", "Medium", "Long", "Total_Distinct_Trains", "Pct_Short", "Pct_Long"]]
    table_data = top12.values.tolist()

    table = ax.table(
        cellText=table_data,
        colLabels=["Code", "Station Name", "Short (<=80m)", "Medium (81-240m)", "Long (>240m)", "Total Trains", "Short %", "Long %"],
        loc="center",
        cellLoc="center",
        bbox=[0.05, 0.16, 0.90, 0.54]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8.5)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#3e4451")
        if row == 0:
            cell.set_facecolor("#21252b")
            cell.set_text_props(color="#e5c07b", fontweight="bold", fontfamily="monospace")
        else:
            cell.set_facecolor("#282c34" if row % 2 == 0 else "#21252b")
            if col in [2, 3, 4]:
                cell.set_text_props(color="#61afef", fontweight="bold", fontfamily="monospace")
            elif col == 5:
                cell.set_text_props(color="#98c379", fontweight="bold", fontfamily="monospace")
            else:
                cell.set_text_props(color="#abb2bf", fontfamily="monospace")

    footer_text = (
        "[QA CONCLUSION] Pivot table reconciled 100% with Task 2.4 totals across all 8,147 stations.\n"
        "Artifact saved: outputs/tables/task_5_1_station_pivot.csv"
    )
    fig.text(0.05, 0.06, footer_text, color="#e5c07b", fontsize=9.5, fontfamily="monospace",
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#21252b", edgecolor="#e5c07b", alpha=0.8))

    SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(SCREENSHOT_PATH, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"[EVIDENCE] Saved screenshot: {SCREENSHOT_PATH}")


def write_documentation_note(pivot: pd.DataFrame, top_long: pd.DataFrame, top_short: pd.DataFrame, top_med: pd.DataFrame):
    """Write documentation note following Requirement, Implementation, Output, Interpretation format."""
    top10_str = pivot.head(10).to_string(index=False)
    top_long_str = top_long[["Station_Code", "Station_Name", "Long", "Pct_Long", "Total_Distinct_Trains"]].to_string(index=False)
    top_short_str = top_short[["Station_Code", "Station_Name", "Short", "Pct_Short", "Total_Distinct_Trains"]].to_string(index=False)
    top_med_str = top_med[["Station_Code", "Station_Name", "Medium", "Pct_Medium", "Total_Distinct_Trains"]].to_string(index=False)

    doc_content = f"""================================================================================
TASK 5.1 DOCUMENTATION: PIVOT TABLES - STATION-LEVEL ANALYSIS
================================================================================
Date / Timestamp: 2026-09-14T17:05:00+05:30
Task ID: 5.1
Level: 5 (Advanced Analytical Insights)
Phase: Phase 4 Advanced Analysis & Cross-tabulation (Checkpoint 4)

1. ANALYTICAL QUESTION & REQUIREMENT:
--------------------------------------------------------------------------------
- Analytical Question: "Which stations across Indian Railways serve the highest volume
  of Long-route (>4h) inter-state trains versus Short-route (<=80m) suburban/local
  trains, and how do major metropolitan junctions differ in their traffic composition?"
- Build pivot table: Station_Name x Route_Type -> nunique(Train_No).
- Sort and highlight top stations per service category.
- Reconcile row totals against Task 2.4 station frequency table.

2. IMPLEMENTATION:
--------------------------------------------------------------------------------
- Script: src/level5/task_5_1_pivot_tables.py
- Inputs:
  * data/processed/dataset_verified.csv (186,074 rows, 11,113 trains)
  * outputs/tables/task_2_4_station_frequency.csv (canonical station naming & frequency)
- Methodology:
  * Constructed pivot table aggregating distinct Train_No per Station_Code across
    Route_Type ('Short', 'Medium', 'Long').
  * Mapped canonical station names to eliminate clerical spelling variants.
  * Computed percentage shares (Pct_Short, Pct_Medium, Pct_Long) and total train volume.
  * Exported complete 8,147-row table to outputs/tables/task_5_1_station_pivot.csv.
  * Evidence: screenshots/level5/task_5_1.png, documentation/level5/task_5_1.txt.

3. OUTPUT:
--------------------------------------------------------------------------------
Top 10 Stations by Overall Volume and Route Composition:
{top10_str}

Top 5 Stations by Long-Route Trains (Trunk Line Arteries):
{top_long_str}

Top 5 Stations by Short-Route Trains (Suburban Commuter Hubs):
{top_short_str}

Top 5 Stations by Medium-Route Trains (Regional Express Hubs):
{top_med_str}

4. INTERPRETATION & KEY FINDINGS:
--------------------------------------------------------------------------------
- [DATA FACT] Long-Route Arterial Junctions:
  Vijayawada (BZA, 316 trains / 76.0%), Vadodara (BRC, 307 trains / 81.6%), Kanpur Central
  (CNB, 295 trains / 77.2%), Surat (ST, 272 trains / 86.1%), and Bhusaval (BSL, 253 trains / 84.9%)
  serve the highest volume of long-distance inter-state expresses in the nation.
  `[INTERPRETATION]` These stations function as primary confluence nodes on India's High-Density
  Trunk Corridors (Golden Quadrilateral and North-South/East-West diagonals).
- [DATA FACT] Suburban Commuter Dominance in Mumbai and Chennai:
  CST-Mumbai (CSMT) leads with 804 Short-route trains (78.3% of total), Thane (TNA) has 521 (65.5%),
  and Chennai Beach (MSB) has 484 (65.6% short, 0 long).
  `[INTERPRETATION]` Terminal stations in Mumbai and Chennai are specialized high-throughput commuter
  gateways designed specifically for local suburban EMU turnarounds.
- [DATA FACT] Kolkata's Regional Express Balance:
  Sealdah (SDAH, 348 trains / 46.7%) and Howrah (HWH, 327 trains / 46.8%) lead the nation in
  Medium-route (1.5 - 4 hour) services.
  `[INTERPRETATION]` The Kolkata rail complex maintains a unique operational balance between
  suburban local EMUs and dense regional intercity corridors connecting West Bengal districts.
- [QA VERIFICATION] All 8,147 row totals reconcile with Task 2.4 with 0 mismatches. Spot check
  cells for CSMT, BZA, and SDAH verified 100% against verified dataset.
================================================================================
"""
    DOCS_PATH.write_text(doc_content, encoding="utf-8")
    print(f"[DOCUMENTATION] Saved documentation note: {DOCS_PATH}")


if __name__ == "__main__":
    generate_station_pivot_table()
