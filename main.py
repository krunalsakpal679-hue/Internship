"""Train Schedule Analysis and Interactive Route Enquiry System.

Master Pipeline Runner & Application Launcher.
Sysslan IT Solutions Internship Project
Author: Krunal Sakpal
Technology Stack: Python 3.14, Pandas, NumPy, Matplotlib, Seaborn, Pytest
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def print_banner():
    banner = """
================================================================================
  TRAIN SCHEDULE ANALYSIS AND INTERACTIVE ROUTE ENQUIRY SYSTEM USING PYTHON
  Sysslan IT Solutions Internship Project | Author: Krunal Sakpal
================================================================================
"""
    print(banner)


def run_command(cmd_args, desc):
    print(f"\n>>> [{desc}] Running: {' '.join(cmd_args)}")
    result = subprocess.run(cmd_args, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Failed during: {desc} (Exit code: {result.returncode})")
        return False
    return True


def run_full_pipeline():
    print_banner()
    print("Executing complete end-to-end data processing and analytics pipeline...\n")

    steps = [
        ([sys.executable, "src/level0/dataset_audit.py"], "Level 0: Master Dataset Cryptographic & Statistical Audit"),
        ([sys.executable, "src/level1/task_1_1_overview.py"], "Level 1 (Task 1.1): Dataset Overview"),
        ([sys.executable, "src/level1/task_1_2_start_end.py"], "Level 1 (Task 1.2): Starting and Ending Stations"),
        ([sys.executable, "src/level1/task_1_3_stops_per_train.py"], "Level 1 (Task 1.3): Stops per Train"),
        ([sys.executable, "src/level1/task_1_4_max_min_stops.py"], "Level 1 (Task 1.4): Trains with Max/Min Stops"),
        ([sys.executable, "src/level2/task_2_1_standardize_times.py"], "Level 2 (Task 2.1): Standardize Schedule Times"),
        ([sys.executable, "src/level2/task_2_2_journey_duration.py"], "Level 2 (Task 2.2): Journey Duration Calculation"),
        ([sys.executable, "src/level2/task_2_3_route_classification.py"], "Level 2 (Task 2.3): Route Classification Terciles"),
        ([sys.executable, "src/level2/task_2_4_station_frequency.py"], "Level 2 (Task 2.4): Station Train Frequencies"),
        ([sys.executable, "src/level3/task_3_1_missing_values.py"], "Level 3 (Task 3.1): Missing Value Handling"),
        ([sys.executable, "src/level3/task_3_2_duplicates.py"], "Level 3 (Task 3.2): Deduplication & Loop Route Protection"),
        ([sys.executable, "src/level3/task_3_3_station_order.py"], "Level 3 (Task 3.3): Station Order Monotonicity Validation"),
        ([sys.executable, "src/level3/task_3_4_save_verified.py"], "Level 3 (Task 3.4): Save Verified Analytical Dataset"),
        ([sys.executable, "src/level4/task_4_1_duration_comparison.py"], "Level 4 (Task 4.1): Duration Comparison by Route Type"),
        ([sys.executable, "src/level4/task_4_2_high_traffic_stations.py"], "Level 4 (Task 4.2): Identify High-Traffic Hubs"),
        ([sys.executable, "src/level4/task_4_3_visualizations.py"], "Level 4 (Task 4.3): Publication-Ready Visualizations"),
        ([sys.executable, "src/level4/task_4_4_summary_insights.py"], "Level 4 (Task 4.4): Summary Observations"),
        ([sys.executable, "src/level5/task_5_1_pivot_tables.py"], "Level 5 (Task 5.1): Station Route Pivot Tables"),
        ([sys.executable, "src/level5/task_5_2_crosstab.py"], "Level 5 (Task 5.2): Service Category Cross-tabulation"),
        ([sys.executable, "src/level5/task_5_3_comparative_charts.py"], "Level 5 (Task 5.3): Heatmap and Grouped Bar Charts"),
        ([sys.executable, "src/level5/task_5_4_advanced_insights.py"], "Level 5 (Task 5.4): Advanced Analytical Insights"),
        ([sys.executable, "src/level6/task_6_1_runner.py"], "Level 6 (Task 6.1): Automated CLI Enquiry Test Scenarios"),
        ([sys.executable, "src/validation/evidence_audit.py"], "Validation: 9-Part Evidence Chain Audit"),
        ([sys.executable, "-m", "pytest", "-v"], "Quality Assurance: Full Pytest Test Suite (83 Tests)"),
    ]

    for cmd, desc in steps:
        success = run_command(cmd, desc)
        if not success:
            print(f"\n[PIPELINE ABORTED] Pipeline execution stopped due to failure in: {desc}")
            sys.exit(1)

    print("\n" + "=" * 80)
    print("COMPLETE PIPELINE EXECUTED SUCCESSFULLY — ALL 21 TASKS & TESTS VERIFIED")
    print("=" * 80)


def launch_enquiry_cli():
    print_banner()
    print("Launching Interactive Route Enquiry CLI Application...\n")
    from app.train_enquiry import main as app_main
    app_main()


def main():
    parser = argparse.ArgumentParser(
        description="Train Schedule Analysis and Interactive Route Enquiry System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Execution Modes:
  python main.py             Launch Interactive Route Enquiry CLI application
  python main.py --app       Launch Interactive Route Enquiry CLI application
  python main.py --pipeline  Run complete end-to-end analytical pipeline (Levels 0–6)
  python main.py --test      Run automated pytest test suite (83 test cases)
  python main.py --audit     Run 9-part evidence chain audit across all tasks
        """
    )
    parser.add_argument("--pipeline", action="store_true", help="Execute complete analytical pipeline (Levels 0–6)")
    parser.add_argument("--app", action="store_true", help="Launch interactive route enquiry CLI application")
    parser.add_argument("--gui", action="store_true", help="Launch interactive route enquiry Desktop GUI application")
    parser.add_argument("--test", action="store_true", help="Execute automated test suite using pytest")
    parser.add_argument("--audit", action="store_true", help="Execute 9-part evidence chain audit")

    args = parser.parse_args()

    if args.pipeline:
        run_full_pipeline()
    elif args.gui:
        print_banner()
        print("Launching Desktop Graphical User Interface (GUI)...\n")
        from app.gui_enquiry import main as gui_main
        gui_main()
    elif args.test:
        print_banner()
        sys.exit(subprocess.run([sys.executable, "-m", "pytest", "-v"]).returncode)
    elif args.audit:
        print_banner()
        sys.exit(subprocess.run([sys.executable, "src/validation/evidence_audit.py"]).returncode)
    else:
        launch_enquiry_cli()


if __name__ == "__main__":
    main()
