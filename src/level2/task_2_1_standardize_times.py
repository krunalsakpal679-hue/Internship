"""Task 2.1: Standardize Schedule Fields (Arrival_time, Departure_Time).

Parses arrival and departure times into standardized formats, establishes
the methodology distinguishing origin/terminus null-marker placeholders
(00:00:00) from genuine scheduled midnight halts, and creates boolean
validity flags for downstream journey duration calculations.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

RAW_DATA_PATH = Path("data/raw/Dataset1.csv")
OUTPUT_CSV_PATH = Path("outputs/tables/task_2_1_standardized_times.csv")
SCREENSHOT_PATH = Path("screenshots/level2/task_2_1.png")
DOCS_PATH = Path("documentation/level2/task_2_1.txt")
TRACKER_PATH = Path("documentation/task_tracker.csv")


def run_standardize_times():
    print("=" * 70)
    print("RUNNING TASK 2.1: STANDARDIZE SCHEDULE FIELDS & FLAG PLACEHOLDERS")
    print("=" * 70)

    # 1. Load dataset preserving strings for audit traceability
    df = pd.read_csv(
        RAW_DATA_PATH,
        dtype={
            "SN": str,
            "Train_No": str,
            "Station_Code": str,
            "1A": str,
            "2A": str,
            "3A": str,
            "SL": str,
            "Station_Name": str,
            "Route_Number": str,
            "Arrival_time": str,
            "Departure_Time": str,
            "Distance": str,
        },
    )
    total_rows = len(df)
    print(f"[DATA FACT] Total station-level records loaded: {total_rows:,}")

    # 2. Parse times using pandas.to_datetime with format='%H:%M:%S'
    arr_dt = pd.to_datetime(df["Arrival_time"], format="%H:%M:%S", errors="coerce")
    dep_dt = pd.to_datetime(df["Departure_Time"], format="%H:%M:%S", errors="coerce")

    # Assert no unparseable time formats exist in the raw dataset
    assert arr_dt.isna().sum() == 0, "[ERROR] Found unparseable Arrival_time values"
    assert dep_dt.isna().sum() == 0, "[ERROR] Found unparseable Departure_Time values"
    print("[DATA FACT] 100% of Arrival_time and Departure_Time values parse to %H:%M:%S without error (0 NaT).")

    # 3. Add standardized string representation
    df["Arrival_Time_Std"] = arr_dt.dt.strftime("%H:%M:%S")
    df["Departure_Time_Std"] = dep_dt.dt.strftime("%H:%M:%S")

    # 4. Determine origin (first) and terminus (last) stops per train
    # Note: Dataset1.csv rows are sequentially grouped per train in distance order.
    first_idx = df.groupby("Train_No", sort=False).head(1).index
    last_idx = df.groupby("Train_No", sort=False).tail(1).index

    df["is_first_stop"] = False
    df.loc[first_idx, "is_first_stop"] = True

    df["is_last_stop"] = False
    df.loc[last_idx, "is_last_stop"] = True

    # 5. Apply Placeholder vs. Scheduled Midnight Methodology
    # METHODOLOGY RULE:
    # - Origin Placeholder: If is_first_stop is True and Arrival_time == '00:00:00',
    #   the train originates here and has no incoming arrival; this is a null marker -> Arrival_Valid = False.
    # - Terminus Placeholder: If is_last_stop is True and Departure_Time == '00:00:00',
    #   the train terminates here and has no onward departure; this is a null marker -> Departure_Valid = False.
    # - Genuine Scheduled Midnight:
    #   * Intermediate stops with Arrival_time or Departure_Time == '00:00:00' are scheduled midnight halts -> Valid (True).
    #   * Terminus stops with Arrival_time == '00:00:00' arrived at midnight from prior halts (~23:50) -> Arrival_Valid = True.
    #   * Origin departures are always valid scheduled departures -> Departure_Valid = True.
    df["Arrival_Valid"] = ~(df["is_first_stop"] & (df["Arrival_time"] == "00:00:00")) & arr_dt.notna()
    df["Departure_Valid"] = ~(df["is_last_stop"] & (df["Departure_Time"] == "00:00:00")) & dep_dt.notna()

    # 6. Metrics & Counts
    arr_valid_count = int(df["Arrival_Valid"].sum())
    arr_invalid_count = int((~df["Arrival_Valid"]).sum())
    dep_valid_count = int(df["Departure_Valid"].sum())
    dep_invalid_count = int((~df["Departure_Valid"]).sum())

    print(f"[DATA FACT] Arrival_Valid: {arr_valid_count:,} True ({arr_valid_count/total_rows*100:.2f}%), "
          f"{arr_invalid_count:,} False ({arr_invalid_count/total_rows*100:.2f}%)")
    print(f"[DATA FACT] Departure_Valid: {dep_valid_count:,} True ({dep_valid_count/total_rows*100:.2f}%), "
          f"{dep_invalid_count:,} False ({dep_invalid_count/total_rows*100:.2f}%)")

    # Inspect intermediate midnight halts
    intermediate_arr_zeros = int((~df["is_first_stop"] & ~df["is_last_stop"] & (df["Arrival_time"] == "00:00:00")).sum())
    intermediate_dep_zeros = int((~df["is_first_stop"] & ~df["is_last_stop"] & (df["Departure_Time"] == "00:00:00")).sum())
    terminus_arr_zeros = int((df["is_last_stop"] & (df["Arrival_time"] == "00:00:00")).sum())

    print(f"[DATA FACT] Intermediate scheduled midnight arrivals (preserved as Valid): {intermediate_arr_zeros}")
    print(f"[DATA FACT] Intermediate scheduled midnight departures (preserved as Valid): {intermediate_dep_zeros}")
    print(f"[DATA FACT] Terminus scheduled midnight arrivals (preserved as Valid): {terminus_arr_zeros}")

    # 7. Assertions / Quality Gates
    assert df["Arrival_Valid"].dtype == bool, "Arrival_Valid must be boolean"
    assert df["Departure_Valid"].dtype == bool, "Departure_Valid must be boolean"
    assert arr_invalid_count == 1951, f"Expected 1,951 origin arrival placeholders, got {arr_invalid_count}"
    assert dep_invalid_count == 1955, f"Expected 1,955 terminus departure placeholders, got {dep_invalid_count}"

    # 8. Spot-check 5 sample trains
    spot_checks = ["107", "12626", "12951", "34752", "53041"]
    print("\n--- SPOT CHECK RESULTS FOR 5 TRAINS ---")
    spot_rows = []
    for t in spot_checks:
        sub = df[df["Train_No"] == t]
        first_r = sub.iloc[0]
        last_r = sub.iloc[-1]

        # First row checks
        print(f"Train {t} [Origin: {first_r['Station_Code']}]: Arr={first_r['Arrival_time']} "
              f"(Valid={first_r['Arrival_Valid']}), Dep={first_r['Departure_Time']} (Valid={first_r['Departure_Valid']})")
        spot_rows.append({
            "Train_No": t,
            "Position": "Origin",
            "Station": first_r["Station_Code"],
            "Arr_Time": first_r["Arrival_time"],
            "Arr_Valid": str(first_r["Arrival_Valid"]),
            "Dep_Time": first_r["Departure_Time"],
            "Dep_Valid": str(first_r["Departure_Valid"]),
        })

        # Last row checks
        print(f"Train {t} [Terminus: {last_r['Station_Code']}]: Arr={last_r['Arrival_time']} "
              f"(Valid={last_r['Arrival_Valid']}), Dep={last_r['Departure_Time']} (Valid={last_r['Departure_Valid']})")
        spot_rows.append({
            "Train_No": t,
            "Position": "Terminus",
            "Station": last_r["Station_Code"],
            "Arr_Time": last_r["Arrival_time"],
            "Arr_Valid": str(last_r["Arrival_Valid"]),
            "Dep_Time": last_r["Departure_Time"],
            "Dep_Valid": str(last_r["Departure_Valid"]),
        })

        # Train 107 specific assertion: Origin Arr is placeholder, Terminus Dep is placeholder
        if t == "107":
            assert not first_r["Arrival_Valid"] and first_r["Departure_Valid"]
            assert last_r["Arrival_Valid"] and not last_r["Departure_Valid"]

        # Train 34752 specific assertion: Terminus Arr is 00:00:00 but VALID, Terminus Dep is placeholder FALSE
        if t == "34752":
            assert last_r["Arrival_time"] == "00:00:00" and last_r["Arrival_Valid"]
            assert last_r["Departure_Time"] == "00:00:00" and not last_r["Departure_Valid"]

    # 9. Save table
    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"\nSaved standardized schedule table to: {OUTPUT_CSV_PATH} ({len(df):,} rows)")

    # 10. Generate Visual Evidence Screenshot
    SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig, (ax_bar, ax_table) = plt.subplots(1, 2, figsize=(16, 6), facecolor="#0f172a")

    # Left: Bar chart of validity breakdown
    ax_bar.set_facecolor("#1e293b")
    categories = ["Arrival Time", "Departure Time"]
    valid_counts = [arr_valid_count, dep_valid_count]
    placeholder_counts = [arr_invalid_count, dep_invalid_count]

    bar_width = 0.35
    x = [0, 1]
    b1 = ax_bar.bar([i - bar_width / 2 for i in x], valid_counts, width=bar_width, color="#10b981", label="Valid / Scheduled")
    b2 = ax_bar.bar([i + bar_width / 2 for i in x], placeholder_counts, width=bar_width, color="#ef4444", label="Flagged Placeholder (00:00:00)")

    ax_bar.set_title("Schedule Field Validity Breakdown (186,074 Stops)", color="white", fontsize=12, fontweight="bold")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(categories, color="white", fontsize=11, fontweight="bold")
    ax_bar.tick_params(colors="white")
    ax_bar.set_ylabel("Number of Records", color="white")
    ax_bar.legend(facecolor="#1e293b", edgecolor="#334155", labelcolor="white")

    # Value labels
    for bar in b1:
        yval = bar.get_height()
        ax_bar.text(bar.get_x() + bar.get_width() / 2.0, yval + 1500, f"{yval:,}", ha="center", va="bottom", color="#10b981", fontsize=9, fontweight="bold")
    for bar in b2:
        yval = bar.get_height()
        ax_bar.text(bar.get_x() + bar.get_width() / 2.0, yval + 1500, f"{yval:,}", ha="center", va="bottom", color="#ef4444", fontsize=9, fontweight="bold")
    ax_bar.set_ylim(0, 210000)

    # Right: Spot check table
    ax_table.set_facecolor("#1e293b")
    ax_table.axis("off")
    table_data = [[r["Train_No"], r["Position"], r["Station"], r["Arr_Time"], r["Arr_Valid"], r["Dep_Time"], r["Dep_Valid"]] for r in spot_rows]
    col_labels = ["Train", "Stop", "Stn", "Arrival", "Arr Valid", "Departure", "Dep Valid"]

    tbl = ax_table.table(
        cellText=table_data,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
        colWidths=[0.12, 0.14, 0.12, 0.16, 0.15, 0.16, 0.15],
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1.0, 1.4)

    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#334155")
        if r == 0:
            cell.set_facecolor("#2563eb")
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        else:
            is_even = (r % 2 == 0)
            cell.set_facecolor("#1e293b" if is_even else "#0f172a")
            # Highlight False in red, True in green
            val_text = cell.get_text().get_text()
            if val_text == "False":
                cell.get_text().set_color("#f87171")
                cell.get_text().set_weight("bold")
            elif val_text == "True":
                cell.get_text().set_color("#4ade80")
            else:
                cell.get_text().set_color("#f8fafc")

    ax_table.set_title("Manual Spot Check Validation (5 Trains)", color="white", fontsize=12, fontweight="bold")

    plt.suptitle("Task 2.1: Schedule Standardization & Placeholder Flagging", color="white", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(SCREENSHOT_PATH, dpi=180, facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved visual evidence screenshot to: {SCREENSHOT_PATH}")

    # 11. Write documentation
    DOCS_PATH.parent.mkdir(parents=True, exist_ok=True)
    docs_text = f"""TASK: Task 2.1: Standardize Schedule Fields (Arrival_time, Departure_Time)
LEVEL: Level 2 — Simple Data Processing
IMPLEMENTATION FILE: src/level2/task_2_1_standardize_times.py
OUTPUT FILE: outputs/tables/task_2_1_standardized_times.csv
EVIDENCE SCREENSHOT: screenshots/level2/task_2_1.png
DOCUMENTATION: documentation/level2/task_2_1.txt
GIT CHECKPOINT: Checkpoint 2 (Level 2 + Level 3 bundle, Section 24)

1. REQUIREMENT:
Convert Arrival_time and Departure_Time to a consistent, parseable time type and flag placeholder/invalid values (e.g. 00:00:00 used as a null-marker at origin/terminus) while preserving raw strings for auditability.
Outputs:
- outputs/tables/task_2_1_standardized_times.csv
- screenshots/level2/task_2_1.png
- documentation/level2/task_2_1.txt

2. IMPLEMENTATION:
- Script developed at src/level2/task_2_1_standardize_times.py.
- Parsed Arrival_time and Departure_Time using pd.to_datetime(..., format='%H:%M:%S', errors='coerce').
- Verified 100% parse success (0 NaT values across 186,074 rows).
- Created Arrival_Time_Std and Departure_Time_Std standardized columns.
- Reconstructed train stop boundaries using groupby('Train_No') to tag is_first_stop and is_last_stop.
- Implemented methodological distinction between placeholder null-markers and scheduled midnight stops:
  * Origin Placeholder: is_first_stop & Arrival_time == '00:00:00' -> Arrival_Valid = False.
  * Terminus Placeholder: is_last_stop & Departure_Time == '00:00:00' -> Departure_Valid = False.
  * Intermediate halts at 00:00:00 and terminus arrivals at 00:00:00 are preserved as Valid (True).
- Performed spot-check validations across 5 sample trains (107, 12626, 12951, 34752, 53041).

3. OUTPUT:
- Table outputs/tables/task_2_1_standardized_times.csv generated with 186,074 rows and 16 columns.
- Standardized vs Placeholder Counts:
  * Total Records: 186,074
  * Arrival_Valid = True: 184,123 (98.95%)
  * Arrival_Valid = False (Origin Placeholders): 1,951 (1.05%)
  * Departure_Valid = True: 184,119 (98.95%)
  * Departure_Valid = False (Terminus Placeholders): 1,955 (1.05%)
  * Intermediate Scheduled Midnight Arrivals: 48 (100% Valid)
  * Intermediate Scheduled Midnight Departures: 15 (100% Valid)
  * Terminus Scheduled Midnight Arrivals: 4 (Trains 34752, 40153, 40572, 64483; 100% Valid)

4. INTERPRETATION:
- DATA FACT: 100% of timestamp strings in Dataset1.csv strictly adhere to %H:%M:%S format with zero parsing failures.
- METHODOLOGY: A timestamp of 00:00:00 cannot blindly be imputed or removed as 'bad data'. At the origin stop of 1,951 trains, 00:00:00 functions as a null-marker indicating 'no prior arrival'. At the terminus stop of 1,955 trains, 00:00:00 functions as a null-marker indicating 'no subsequent departure'.
- METHODOLOGY: Intermediate stops with 00:00:00 (48 arrivals, 15 departures) and terminus stops with 00:00:00 arrival (4 trains) represent genuine scheduled operations around midnight and must remain flagged as Valid so journey duration calculations in Task 2.2 remain strictly accurate.
"""
    with open(DOCS_PATH, "w", encoding="utf-8") as f:
        f.write(docs_text)
    print(f"Saved documentation findings to: {DOCS_PATH}")

    # 12. Update task tracker
    if TRACKER_PATH.is_file():
        tracker_df = pd.read_csv(TRACKER_PATH)
        mask = tracker_df["Task ID"].astype(str) == "2.1"
        if mask.any():
            tracker_df.loc[mask, "Status"] = "COMPLETED"
            tracker_df.to_csv(TRACKER_PATH, index=False)
            print("Updated documentation/task_tracker.csv for Task 2.1 -> COMPLETED")

    print("=" * 70)
    print("TASK 2.1 COMPLETE AND VERIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    run_standardize_times()
