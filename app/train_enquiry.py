"""Interactive Route Enquiry Application (Level 6).

Sysslan IT Solutions Internship Project.
Enables fast, interactive search for DIRECT trains between any two stations across
the Indian Railways network using data/processed/dataset_verified.csv.

Features:
- In-memory train schedule indexing for sub-millisecond query latency.
- Flexible station resolution (Station Code or Station Name, case & whitespace insensitive).
- Strict DIRECT train filtering (Source SN/Distance < Destination SN/Distance on same Train_No).
- Midnight-safe duration calculation (reusing Task 2.2 logic).
- Comprehensive error handling for invalid stations, identical source/destination, and zero-result queries.
- Clean CLI interface and reusable Python API for testing and automation.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd

DEFAULT_DATASET_PATH = Path("data/processed/dataset_verified.csv")


def compute_segment_duration(start_time_str: str, end_time_str: str) -> Tuple[int, str]:
    """Compute segment journey duration in minutes with single-day midnight rollover.

    Reuses validated Task 2.2 logic using dummy base datetime objects.
    Returns (duration_minutes, formatted_string like '1h 15m' or '45m').
    """
    if pd.isna(start_time_str) or pd.isna(end_time_str):
        return 0, "N/A"

    t_start = datetime.strptime(str(start_time_str).strip(), "%H:%M:%S").time()
    t_end = datetime.strptime(str(end_time_str).strip(), "%H:%M:%S").time()

    base_date = datetime(2026, 1, 1)
    dt_start = datetime.combine(base_date, t_start)

    if t_end >= t_start:
        dt_end = datetime.combine(base_date, t_end)
    else:
        dt_end = datetime.combine(datetime(2026, 1, 2), t_end)

    mins = int((dt_end - dt_start).total_seconds() / 60)
    hrs = mins // 60
    rem_mins = mins % 60
    fmt = f"{hrs}h {rem_mins:02d}m" if hrs > 0 else f"{mins}m"
    return mins, fmt


class TrainRouteEnquiryEngine:
    """In-memory search engine for querying direct train routes."""

    def __init__(self, dataset_path: Optional[Path] = None):
        """Load verified dataset and initialize fast in-memory lookup indexes."""
        self.dataset_path = Path(dataset_path) if dataset_path else DEFAULT_DATASET_PATH
        if not self.dataset_path.is_file():
            raise FileNotFoundError(f"Verified dataset not found at: {self.dataset_path}")

        # Ingest dataset
        self.df = pd.read_csv(self.dataset_path, dtype=str, keep_default_na=False)

        # 1. Build Station Catalog (Code -> Canonical Name, Name -> Code)
        self.code_to_name: Dict[str, str] = {}
        self.name_to_code: Dict[str, str] = {}

        for _, row in self.df[["Station_Code", "Station_Name"]].drop_duplicates().iterrows():
            c = row["Station_Code"].strip().upper()
            n = row["Station_Name"].strip()
            self.code_to_name[c] = n
            self.name_to_code[n.upper()] = c

        # 2. Build Fast In-Memory Schedule Structure Grouped by Train_No
        self.train_schedules: Dict[str, List[dict]] = {}
        self.station_to_trains: Dict[str, set] = {code: set() for code in self.code_to_name}

        for train_no, group in self.df.groupby("Train_No", sort=False):
            t_str = str(train_no).strip()
            stops = []
            for _, row in group.iterrows():
                stn_code = row["Station_Code"].strip().upper()
                stops.append({
                    "SN": int(row["SN"]),
                    "Station_Code": stn_code,
                    "Station_Name": row["Station_Name"].strip(),
                    "Arrival_Time": row["Arrival_Time_Std"].strip(),
                    "Departure_Time": row["Departure_Time_Std"].strip(),
                    "Distance": int(row["Distance"])
                })
                self.station_to_trains[stn_code].add(t_str)
            self.train_schedules[t_str] = stops

    def resolve_station(self, query: str) -> Optional[Tuple[str, str]]:
        """Resolve user input to (Station_Code, Canonical_Name) flexibly and case-insensitively."""
        if not query or not str(query).strip():
            return None

        q = str(query).strip().upper()

        # 1. Direct code match (e.g. 'CSMT', 'BZA', 'MAS')
        if q in self.code_to_name:
            return q, self.code_to_name[q]

        # 2. Exact station name match (e.g. 'CST-MUMBAI', 'VIJAYWADA JN')
        if q in self.name_to_code:
            code = self.name_to_code[q]
            return code, self.code_to_name[code]

        # 3. Flexible match: Station name starts with query or query starts with station name
        matches = [c for name, c in self.name_to_code.items() if name.startswith(q) or q.startswith(name)]
        if len(matches) == 1:
            code = matches[0]
            return code, self.code_to_name[code]
        elif len(matches) > 1:
            # Prefer matching exact start
            pref_matches = [c for name, c in self.name_to_code.items() if name.startswith(q)]
            if len(pref_matches) == 1:
                code = pref_matches[0]
                return code, self.code_to_name[code]
            # Otherwise pick longest matching station name
            matches.sort(key=lambda c: len(self.code_to_name[c]), reverse=True)
            code = matches[0]
            return code, self.code_to_name[code]

        return None

    def search_direct_trains(self, source_input: str, dest_input: str) -> dict:
        """Search for all direct trains from source to destination.

        Returns a dictionary with 'status', 'message', 'count', and 'results'.
        """
        # Validate input strings
        if not source_input or not str(source_input).strip():
            return {"status": "ERROR", "message": "Source station cannot be empty.", "count": 0, "results": []}
        if not dest_input or not str(dest_input).strip():
            return {"status": "ERROR", "message": "Destination station cannot be empty.", "count": 0, "results": []}

        src_res = self.resolve_station(source_input)
        if not src_res:
            return {
                "status": "ERROR",
                "message": f"Unknown or invalid source station: '{source_input.strip()}'. Please verify station code or name.",
                "count": 0,
                "results": []
            }

        dst_res = self.resolve_station(dest_input)
        if not dst_res:
            return {
                "status": "ERROR",
                "message": f"Unknown or invalid destination station: '{dest_input.strip()}'. Please verify station code or name.",
                "count": 0,
                "results": []
            }

        src_code, src_name = src_res
        dst_code, dst_name = dst_res

        # Check same station
        if src_code == dst_code:
            return {
                "status": "ERROR",
                "message": f"Source and destination stations are identical: {src_name} ({src_code}). A journey requires distinct stations.",
                "count": 0,
                "results": []
            }

        # Fast set intersection for candidate trains
        candidate_trains = self.station_to_trains[src_code].intersection(self.station_to_trains[dst_code])
        if not candidate_trains:
            return {
                "status": "NO_DIRECT_TRAINS",
                "message": f"No direct trains found between {src_name} ({src_code}) and {dst_name} ({dst_code}).",
                "source": f"{src_name} ({src_code})",
                "destination": f"{dst_name} ({dst_code})",
                "count": 0,
                "results": []
            }

        # Filter candidates where source occurs strictly before destination
        results = []
        for train_no in candidate_trains:
            schedule = self.train_schedules[train_no]
            stn_codes = [s["Station_Code"] for s in schedule]

            src_idx = stn_codes.index(src_code)
            # Find destination index occurring after source (handles loop/circular routes correctly)
            dst_indices = [i for i, code in enumerate(stn_codes) if code == dst_code and i > src_idx]

            if dst_indices:
                dst_idx = dst_indices[0]
                src_stop = schedule[src_idx]
                dst_stop = schedule[dst_idx]

                dep_time = src_stop["Departure_Time"]
                arr_time = dst_stop["Arrival_Time"]
                dur_mins, dur_fmt = compute_segment_duration(dep_time, arr_time)
                dist_km = dst_stop["Distance"] - src_stop["Distance"]
                inter_stops = dst_idx - src_idx - 1

                results.append({
                    "Train_No": train_no,
                    "Source_Code": src_code,
                    "Source_Name": src_stop["Station_Name"],
                    "Dest_Code": dst_code,
                    "Dest_Name": dst_stop["Station_Name"],
                    "Departure_Time": dep_time,
                    "Arrival_Time": arr_time,
                    "Duration_Minutes": dur_mins,
                    "Duration_Formatted": dur_fmt,
                    "Distance_km": dist_km,
                    "Intermediate_Stops": inter_stops
                })

        if not results:
            return {
                "status": "NO_DIRECT_TRAINS",
                "message": f"No direct trains found from {src_name} ({src_code}) to {dst_name} ({dst_code}) in this direction of travel.",
                "source": f"{src_name} ({src_code})",
                "destination": f"{dst_name} ({dst_code})",
                "count": 0,
                "results": []
            }

        # Sort results chronologically by departure time
        results.sort(key=lambda x: (x["Departure_Time"], x["Train_No"]))

        return {
            "status": "SUCCESS",
            "message": f"Found {len(results)} direct train(s) from {src_name} ({src_code}) to {dst_name} ({dst_code}).",
            "source": f"{src_name} ({src_code})",
            "destination": f"{dst_name} ({dst_code})",
            "count": len(results),
            "results": results
        }

    def format_results_table(self, query_response: dict) -> str:
        """Render a clean ASCII table of search results."""
        status = query_response["status"]
        if status != "SUCCESS":
            return f"\n[!] {query_response['message']}\n"

        results = query_response["results"]
        src = query_response["source"]
        dst = query_response["destination"]
        count = query_response["count"]

        lines = [
            "\n" + "=" * 88,
            f"  DIRECT TRAIN SCHEDULE ENQUIRY: {src} -> {dst}",
            f"  Total Direct Trains Found: {count}",
            "=" * 88,
            f"{'#':<4} {'Train No':<10} {'Departure':<12} {'Arrival':<12} {'Est. Duration':<15} {'Distance':<12} {'Stops':<8}",
            "-" * 88
        ]

        for idx, t in enumerate(results, 1):
            lines.append(
                f"{idx:<4} {t['Train_No']:<10} {t['Departure_Time']:<12} {t['Arrival_Time']:<12} "
                f"{t['Duration_Formatted']:<15} {str(t['Distance_km']) + ' km':<12} {t['Intermediate_Stops']:<8}"
            )

        lines.append("=" * 88 + "\n")
        return "\n".join(lines)

    def interactive_cli(self):
        """Run interactive console session for user route enquiry."""
        print("\n" + "=" * 70)
        print("  INDIAN RAILWAYS INTERACTIVE ROUTE ENQUIRY SYSTEM")
        print("  Sysslan IT Solutions Internship Project (Level 6)")
        print(f"  Dataset: {len(self.code_to_name):,} Stations | {len(self.train_schedules):,} Unique Trains")
        print("=" * 70)
        print("  Type station code (e.g. 'CSMT', 'NDLS') or name (e.g. 'Kalyan Jn').")
        print("  Enter 'q' or 'exit' to quit.\n")

        while True:
            try:
                src_input = input("Enter SOURCE Station: ").strip()
                if src_input.lower() in ["q", "exit", "quit"]:
                    print("\nThank you for using the Train Route Enquiry System. Goodbye!")
                    break

                dst_input = input("Enter DESTINATION Station: ").strip()
                if dst_input.lower() in ["q", "exit", "quit"]:
                    print("\nThank you for using the Train Route Enquiry System. Goodbye!")
                    break

                response = self.search_direct_trains(src_input, dst_input)
                print(self.format_results_table(response))

            except (KeyboardInterrupt, EOFError):
                print("\n\nSession terminated by user. Goodbye!")
                break


def main():
    """CLI application entry point."""
    engine = TrainRouteEnquiryEngine()
    engine.interactive_cli()


if __name__ == "__main__":
    main()
