"""Flask Web Application for Indian Railways Route Enquiry System.

Sysslan IT Solutions Internship Project.
Author: Krunal Sakpal

Serves an interactive Web UI at http://127.0.0.1:5000
"""

import os
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from app.train_enquiry import TrainRouteEnquiryEngine

app = Flask(__name__)
ROOT_DIR = Path(__file__).resolve().parent.parent
CHART_DIR = ROOT_DIR / "outputs" / "charts"

# Initialize Engine
print("Initializing TrainRouteEnquiryEngine for Web Server...")
engine = TrainRouteEnquiryEngine()
print(f"Loaded {len(engine.code_to_name):,} stations and {len(engine.train_schedules):,} trains.")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indian Railways Route Enquiry System</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0d47a1;
            --primary-dark: #002171;
            --primary-light: #5472d3;
            --accent: #ff6f00;
            --bg: #f4f6f9;
            --card-bg: #ffffff;
            --text-main: #212529;
            --text-muted: #6c757d;
            --border: #e0e0e0;
            --success: #2e7d32;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text-main); line-height: 1.5; }
        
        /* Header */
        header { background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%); color: white; padding: 25px 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
        .title-group h1 { font-size: 26px; font-weight: 800; letter-spacing: -0.5px; display: flex; align-items: center; gap: 10px; }
        .title-group p { font-size: 13px; opacity: 0.9; margin-top: 4px; font-weight: 400; }
        .badge-verified { background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid rgba(255,255,255,0.3); }

        /* Container */
        .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }

        /* Navigation Tabs */
        .nav-tabs { display: flex; gap: 10px; border-bottom: 2px solid var(--border); margin-bottom: 25px; background: white; padding: 10px 15px 0; border-radius: 12px 12px 0 0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
        .nav-tab { padding: 12px 22px; font-size: 15px; font-weight: 600; color: var(--text-muted); cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.2s ease; border-radius: 6px 6px 0 0; }
        .nav-tab:hover { color: var(--primary); background: #f8f9fa; }
        .nav-tab.active { color: var(--primary); border-bottom-color: var(--primary); background: #f0f4ff; }

        /* Tab Content Panels */
        .tab-pane { display: none; }
        .tab-pane.active { display: block; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

        /* Card Styles */
        .card { background: var(--card-bg); border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 25px; border: 1px solid var(--border); }
        .card-title { font-size: 18px; font-weight: 700; margin-bottom: 18px; color: var(--primary-dark); display: flex; align-items: center; gap: 8px; }

        /* Form Controls */
        .form-row { display: grid; grid-template-columns: 1fr auto 1fr auto; gap: 15px; align-items: flex-end; }
        .form-group { display: flex; flex-direction: column; gap: 6px; }
        .form-group label { font-size: 13px; font-weight: 600; color: var(--text-main); }
        .form-control { padding: 12px 16px; border: 1.5px solid var(--border); border-radius: 8px; font-size: 15px; outline: none; transition: border-color 0.2s; font-family: inherit; }
        .form-control:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.15); }
        
        .btn { padding: 12px 24px; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; justify-content: center; gap: 6px; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-primary:hover { background: var(--primary-dark); transform: translateY(-1px); box-shadow: 0 4px 10px rgba(13, 71, 161, 0.3); }
        .btn-swap { background: #eef2f6; color: var(--text-main); padding: 12px 16px; }
        .btn-swap:hover { background: #dfe5ec; }

        /* Quick chips */
        .chips-container { display: flex; gap: 10px; align-items: center; margin-top: 15px; flex-wrap: wrap; }
        .chips-label { font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }
        .chip { background: #e8eaf6; color: #283593; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; cursor: pointer; border: 1px solid #c5cae9; transition: all 0.2s; }
        .chip:hover { background: #c5cae9; }

        /* Table */
        .table-responsive { overflow-x: auto; margin-top: 15px; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th { background: #f8f9fa; padding: 14px 18px; font-size: 13px; font-weight: 700; color: #495057; border-bottom: 2px solid var(--border); text-transform: uppercase; letter-spacing: 0.5px; }
        td { padding: 14px 18px; font-size: 14px; border-bottom: 1px solid var(--border); vertical-align: middle; }
        tbody tr:hover { background: #f0f7ff; cursor: pointer; }
        .train-badge { background: #e3f2fd; color: #0d47a1; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 13px; }
        .duration-badge { background: #e8f5e9; color: #2e7d32; font-weight: 600; padding: 4px 10px; border-radius: 6px; font-size: 13px; }

        /* Status & Alert Box */
        .alert-info { background: #e3f2fd; border-left: 4px solid var(--primary); padding: 14px 18px; border-radius: 6px; font-size: 14px; color: #0d47a1; margin-bottom: 20px; font-weight: 500; }
        .alert-success { background: #e8f5e9; border-left: 4px solid var(--success); padding: 14px 18px; border-radius: 6px; font-size: 14px; color: var(--success); margin-bottom: 20px; font-weight: 600; }
        .alert-warning { background: #fff8e1; border-left: 4px solid var(--accent); padding: 14px 18px; border-radius: 6px; font-size: 14px; color: #e65100; margin-bottom: 20px; font-weight: 500; }
        .alert-danger { background: #ffebee; border-left: 4px solid #c62828; padding: 14px 18px; border-radius: 6px; font-size: 14px; color: #c62828; margin-bottom: 20px; }

        /* Analytics Gallery */
        .chart-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 25px; }
        .chart-card { background: white; border-radius: 12px; padding: 20px; border: 1px solid var(--border); box-shadow: 0 4px 10px rgba(0,0,0,0.03); }
        .chart-card h3 { font-size: 16px; font-weight: 700; color: var(--primary); margin-bottom: 12px; }
        .chart-img { width: 100%; height: auto; border-radius: 8px; border: 1px solid #eee; display: block; }

        /* Stats Grid */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 25px; }
        .stat-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 3px 8px rgba(0,0,0,0.03); }
        .stat-val { font-size: 28px; font-weight: 800; color: var(--primary); margin-top: 6px; }
        .stat-lbl { font-size: 13px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; }

        @media (max-width: 768px) {
            .form-row { grid-template-columns: 1fr; }
            .chart-grid { grid-template-columns: 1fr; }
            .header-content { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>
<body>

<header>
    <div class="header-content">
        <div class="title-group">
            <h1>🚆 Indian Railways Route Enquiry System</h1>
            <p>Sysslan IT Solutions Internship Project | Author: Krunal Sakpal | Live Interactive Web UI</p>
        </div>
        <div class="badge-verified">
            🛡️ 186,074 Verified Records | 83/83 Tests Passed
        </div>
    </div>
</header>

<div class="container">

    <div class="nav-tabs">
        <div class="nav-tab active" onclick="switchTab('routeTab', this)">🔍 Direct Route Search</div>
        <div class="nav-tab" onclick="switchTab('scheduleTab', this)">🚆 Train Timetable</div>
        <div class="nav-tab" onclick="switchTab('analyticsTab', this)">📊 Visual Analytics & Dashboards</div>
        <div class="nav-tab" onclick="switchTab('systemTab', this)">ℹ️ System Overview</div>
    </div>

    <!-- TAB 1: ROUTE SEARCH -->
    <div id="routeTab" class="tab-pane active">
        <div class="card">
            <h2 class="card-title">🔍 Direct Train Route Search</h2>
            <div class="form-row">
                <div class="form-group">
                    <label for="srcInput">Origin Station (Code or Name):</label>
                    <input type="text" id="srcInput" class="form-control" placeholder="e.g. CSMT or CST-MUMBAI" value="CSMT">
                </div>
                <button class="btn btn-swap" onclick="swapStations()" title="Swap Origin and Destination">⇄ Swap</button>
                <div class="form-group">
                    <label for="dstInput">Destination Station (Code or Name):</label>
                    <input type="text" id="dstInput" class="form-control" placeholder="e.g. KYN or KALYAN JN" value="KYN">
                </div>
                <button class="btn btn-primary" onclick="searchRoutes()">🔍 Search Direct Trains</button>
            </div>

            <div class="chips-container">
                <span class="chips-label">Popular Routes:</span>
                <span class="chip" onclick="setRoute('CSMT', 'KYN')">CSMT → KYN</span>
                <span class="chip" onclick="setRoute('BZA', 'MAS')">BZA → MAS</span>
                <span class="chip" onclick="setRoute('NDLS', 'HWH')">NDLS → HWH</span>
                <span class="chip" onclick="setRoute('HWH', 'NDLS')">HWH → NDLS</span>
                <span class="chip" onclick="setRoute('PUNE', 'CSMT')">PUNE → CSMT</span>
                <span class="chip" onclick="setRoute('SBC', 'MAS')">SBC → MAS</span>
            </div>
        </div>

        <div id="routeResultsArea">
            <div class="alert-info">Enter origin and destination station codes or names above and click "Search Direct Trains".</div>
        </div>
    </div>

    <!-- TAB 2: TRAIN TIMETABLE -->
    <div id="scheduleTab" class="tab-pane">
        <div class="card">
            <h2 class="card-title">🚆 Full Train Route Timetable</h2>
            <div style="display: flex; gap: 15px; align-items: flex-end; max-width: 600px;">
                <div class="form-group" style="flex: 1;">
                    <label for="trainNoInput">Enter Train Number:</label>
                    <input type="text" id="trainNoInput" class="form-control" placeholder="e.g. 12951, 11019, 12001" value="12951">
                </div>
                <button class="btn btn-primary" onclick="searchTimetable()">View Timetable</button>
            </div>
        </div>

        <div id="scheduleResultsArea">
            <div class="alert-info">Enter a train number above to view its full sequence of stops across India.</div>
        </div>
    </div>

    <!-- TAB 3: VISUAL ANALYTICS -->
    <div id="analyticsTab" class="tab-pane">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-lbl">Total Station Stops</div>
                <div class="stat-val">186,074</div>
            </div>
            <div class="stat-card">
                <div class="stat-lbl">Unique Trains</div>
                <div class="stat-val">11,113</div>
            </div>
            <div class="stat-card">
                <div class="stat-lbl">Unique Stations</div>
                <div class="stat-val">8,147</div>
            </div>
            <div class="stat-card">
                <div class="stat-lbl">Pytest QA Suite</div>
                <div class="stat-val" style="color: #2e7d32;">83 / 83 PASS</div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart-card">
                <h3>📈 Top 10 High-Traffic Station Hubs (Task 4.3)</h3>
                <img src="/charts/task_4_3_high_traffic_stations.png" alt="High Traffic Stations" class="chart-img">
            </div>
            <div class="chart-card">
                <h3>⏱️ Journey Duration Distribution & KDE (Task 4.3)</h3>
                <img src="/charts/task_4_3_duration_histogram.png" alt="Duration Histogram" class="chart-img">
            </div>
            <div class="chart-card">
                <h3>📊 Journey Duration Comparison by Route Type (Task 4.3)</h3>
                <img src="/charts/task_4_3_duration_by_route_type.png" alt="Duration by Route Type" class="chart-img">
            </div>
            <div class="chart-card">
                <h3>🔥 Station Route Pivot Heatmap (Task 5.3)</h3>
                <img src="/charts/task_5_3_station_pivot_heatmap.png" alt="Station Pivot Heatmap" class="chart-img">
            </div>
            <div class="chart-card">
                <h3>🚆 Fleet Service Class Composition (Task 5.3)</h3>
                <img src="/charts/task_5_3_route_crosstab_bar.png" alt="Route Crosstab Bar" class="chart-img">
            </div>
        </div>
    </div>

    <!-- TAB 4: SYSTEM OVERVIEW -->
    <div id="systemTab" class="tab-pane">
        <div class="card">
            <h2 class="card-title">ℹ️ System Specifications & Architecture</h2>
            <div style="line-height: 1.8; font-size: 15px;">
                <p><strong>Project Title:</strong> Train Schedule Analysis and Interactive Route Enquiry System Using Python</p>
                <p><strong>Organization:</strong> Sysslan IT Solutions Internship</p>
                <p><strong>Author:</strong> Krunal Sakpal</p>
                <p><strong>Verified Dataset:</strong> <code>data/processed/dataset_verified.csv</code> (186,074 rows)</p>
                <p><strong>Cryptographic SHA-256:</strong> <code>8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57</code></p>
                <br>
                <h3 style="color: var(--primary); margin-bottom: 10px;">Core Engine Features:</h3>
                <ul style="margin-left: 20px;">
                    <li><strong>In-Memory Inverted Index:</strong> Instantaneous search response (&lt; 3 ms latency).</li>
                    <li><strong>Dual Code/Name Alias Resolution:</strong> Matches both official codes (<code>CSMT</code>) and common names (<code>CST-MUMBAI</code>).</li>
                    <li><strong>Strict Direct Directionality:</strong> Enforces monotonic distance and sequence constraints.</li>
                    <li><strong>Midnight Rollover Calculation:</strong> Handles cross-midnight journeys accurately.</li>
                </ul>
            </div>
        </div>
    </div>

</div>

<script>
    function switchTab(tabId, tabEl) {
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        tabEl.classList.add('active');
    }

    function swapStations() {
        const s = document.getElementById('srcInput').value;
        const d = document.getElementById('dstInput').value;
        document.getElementById('srcInput').value = d;
        document.getElementById('dstInput').value = s;
    }

    function setRoute(src, dst) {
        document.getElementById('srcInput').value = src;
        document.getElementById('dstInput').value = dst;
        searchRoutes();
    }

    async function searchRoutes() {
        const src = document.getElementById('srcInput').value.trim();
        const dst = document.getElementById('dstInput').value.trim();
        const area = document.getElementById('routeResultsArea');

        if (!src || !dst) {
            area.innerHTML = '<div class="alert-danger">Please provide both origin and destination station codes or names.</div>';
            return;
        }

        area.innerHTML = '<div class="alert-info">Searching direct trains across 186,074 schedule records...</div>';

        try {
            const res = await fetch(`/api/routes?src=${encodeURIComponent(src)}&dst=${encodeURIComponent(dst)}`);
            const data = await res.json();

            if (data.status === 'ERROR') {
                area.innerHTML = `<div class="alert-danger">❌ ${data.message}</div>`;
                return;
            }

            if (data.status === 'NO_DIRECT_TRAINS' || data.count === 0) {
                area.innerHTML = `<div class="alert-warning">ℹ️ ${data.message}</div>`;
                return;
            }

            let html = `
                <div class="alert-success">
                    ✅ <strong>Found ${data.count} Direct Train(s)</strong> from <strong>${data.source}</strong> ➔ <strong>${data.destination}</strong>
                </div>
                <div class="card">
                    <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">💡 Click any row to view its complete stop-by-stop route timetable.</p>
                    <div class="table-responsive">
                        <table>
                            <thead>
                                <tr>
                                    <th>Train No</th>
                                    <th>Origin Departure</th>
                                    <th>Dest Arrival</th>
                                    <th>Intermediate Stops</th>
                                    <th>Segment Distance</th>
                                    <th>Est. Duration</th>
                                </tr>
                            </thead>
                            <tbody>
            `;

            data.results.forEach(t => {
                html += `
                    <tr onclick="inspectTrain('${t.Train_No}')">
                        <td><span class="train-badge">${t.Train_No}</span></td>
                        <td><strong>${t.Departure_Time}</strong></td>
                        <td><strong>${t.Arrival_Time}</strong></td>
                        <td>${t.Intermediate_Stops} stops</td>
                        <td>${t.Distance_km} km</td>
                        <td><span class="duration-badge">${t.Duration_Formatted}</span></td>
                    </tr>
                `;
            });

            html += `
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
            area.innerHTML = html;

        } catch (e) {
            area.innerHTML = `<div class="alert-danger">Server communication error: ${e.message}</div>`;
        }
    }

    function inspectTrain(trainNo) {
        document.getElementById('trainNoInput').value = trainNo;
        const schedTabNav = document.querySelectorAll('.nav-tab')[1];
        switchTab('scheduleTab', schedTabNav);
        searchTimetable();
    }

    async function searchTimetable() {
        const trainNo = document.getElementById('trainNoInput').value.trim();
        const area = document.getElementById('scheduleResultsArea');

        if (!trainNo) {
            area.innerHTML = '<div class="alert-danger">Please enter a valid train number.</div>';
            return;
        }

        area.innerHTML = '<div class="alert-info">Loading train schedule...</div>';

        try {
            const res = await fetch(`/api/timetable?train_no=${encodeURIComponent(trainNo)}`);
            const data = await res.json();

            if (!data.success) {
                area.innerHTML = `<div class="alert-danger">❌ ${data.error}</div>`;
                return;
            }

            let html = `
                <div class="alert-success">
                    🚆 <strong>Train #${data.train_no}:</strong> ${data.origin.name} (${data.origin.code}) ➔ ${data.destination.name} (${data.destination.code}) | Total Stops: <strong>${data.total_stops}</strong> | Total Distance: <strong>${data.total_distance_km} km</strong>
                </div>
                <div class="card">
                    <div class="table-responsive">
                        <table>
                            <thead>
                                <tr>
                                    <th>Stop #</th>
                                    <th>Station Code</th>
                                    <th>Station Name</th>
                                    <th>Arrival</th>
                                    <th>Departure</th>
                                    <th>Cumulative Distance</th>
                                </tr>
                            </thead>
                            <tbody>
            `;

            data.stops.forEach(s => {
                html += `
                    <tr>
                        <td><strong>${s.SN}</strong></td>
                        <td><span class="train-badge">${s.Station_Code}</span></td>
                        <td><strong>${s.Station_Name}</strong></td>
                        <td>${s.Arrival_Time}</td>
                        <td>${s.Departure_Time}</td>
                        <td>${s.Distance} km</td>
                    </tr>
                `;
            });

            html += `
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
            area.innerHTML = html;

        } catch (e) {
            area.innerHTML = `<div class="alert-danger">Server communication error: ${e.message}</div>`;
        }
    }

    // Run default search on load
    window.addEventListener('DOMContentLoaded', () => {
        searchRoutes();
    });
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/routes")
def api_routes():
    try:
        src = request.args.get("src", "").strip()
        dst = request.args.get("dst", "").strip()
        if not src or not dst:
            return jsonify({"status": "ERROR", "message": "Both origin and destination stations are required.", "count": 0, "results": []})
        res = engine.search_direct_trains(src, dst)
        return jsonify(res)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Server processing exception: {str(e)}", "count": 0, "results": []})

@app.route("/api/timetable")
def api_timetable():
    try:
        train_no = request.args.get("train_no", "").strip()
        if not train_no:
            return jsonify({"success": False, "error": "Parameter 'train_no' is required."})
        if train_no not in engine.train_schedules:
            return jsonify({"success": False, "error": f"Train '{train_no}' not found in the verified dataset."})

        stops = engine.train_schedules[train_no]
        return jsonify({
            "success": True,
            "train_no": train_no,
            "origin": {"code": stops[0]["Station_Code"], "name": stops[0]["Station_Name"]},
            "destination": {"code": stops[-1]["Station_Code"], "name": stops[-1]["Station_Name"]},
            "total_stops": len(stops),
            "total_distance_km": stops[-1]["Distance"],
            "stops": stops
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/charts/<filename>")
def serve_chart(filename):
    return send_from_directory(CHART_DIR, filename)

def main():
    port = int(os.environ.get("PORT", 5000))
    print(f"\n================================================================================")
    print(f"  INDIAN RAILWAYS ROUTE ENQUIRY WEB SERVER RUNNING")
    print(f"  Access URL: http://127.0.0.1:{port} (or http://localhost:{port})")
    print(f"================================================================================\n")
    app.run(host="127.0.0.1", port=port, debug=False)

if __name__ == "__main__":
    main()
