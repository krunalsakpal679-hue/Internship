# Train Schedule Analysis and Interactive Route Enquiry System

**Internship Project** | Sysslan IT Solutions  
**Author**: Krunal Sakpal  
**Technology Stack**: Python 3.14, Pandas, NumPy, Matplotlib, Seaborn, Pytest  

---

## Project Overview
This repository contains an end-to-end data analytics and route enquiry pipeline analyzing Indian Railways schedule data. The dataset comprises 186,074 station-level stop records across hundreds of train routes.

Each row in the dataset represents an individual station stop on a specific train route rather than a single train. Trains are reconstructed by grouping rows by `Train_No` (and `Route_Number` where applicable) and ordering them by `Distance` and sequence number (`SN`).

---

## Project Structure
```text
train-schedule-analysis/
├── data/
│   ├── raw/                # Read-only source of truth (Dataset1.csv)
│   └── processed/          # Cleaned, standardized, and validated datasets
├── notebooks/              # Exploratory and prototyping notebooks
├── src/
│   ├── level0/             # Dataset audit logic
│   ├── level1/             # Level 1: Basic data review scripts
│   ├── level2/             # Level 2: Simple data processing scripts
│   ├── level3/             # Level 3: Data quality & cleaning scripts
│   ├── level4/             # Level 4: Exploratory data analysis & visualizations
│   ├── level5/             # Level 5: Advanced analysis, pivot & cross-tabulations
│   ├── level6/             # Level 6: Application components
│   └── validation/         # Data integrity and evidence audit scripts
├── app/                    # Interactive Route Enquiry CLI application
├── outputs/
│   ├── charts/             # Generated visualizations (.png)
│   ├── tables/             # Tabular results and analytical metrics (.csv)
│   └── reports/            # Markdown reports and audits
├── screenshots/            # Verification screenshots (Levels 1–6)
├── documentation/          # Per-task documentation, session logs, trackers
├── tests/                  # Automated test suite (pytest)
├── requirements.txt        # Python dependency manifest
├── .gitignore              # Git ignore rules
├── README.md               # Repository documentation
└── main.py                 # Pipeline runner / main entry point
```

---

## Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/krunalsakpal679-hue/Internship.git
   cd Internship
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify test suite**:
   ```bash
   pytest
   ```

---

## Execution Phases & Checkpoints
- **Checkpoint 0**: Project Foundation & Workspace Setup
- **Checkpoint 1**: Dataset Audit & Level 1 Analysis (Tasks 1.1–1.4)
- **Checkpoint 2**: Data Processing & Quality Validation (Levels 2 & 3, Tasks 2.1–3.4)
- **Checkpoint 3**: Basic Analysis & Visualization (Level 4, Tasks 4.1–4.4)
- **Checkpoint 4**: Advanced Analysis & Visualization (Level 5, Tasks 5.1–5.4)
- **Checkpoint 5**: Interactive Route Enquiry System (Level 6, Task 6.1)
- **Checkpoint 6**: Full Automated Test Suite & Validation
- **Checkpoint 7**: Comprehensive Project Documentation
- **Checkpoint 8**: Final Release & Submission Package
