# Presentation & Video Demonstration Script

**Project Title**: Train Schedule Analysis and Interactive Route Enquiry System Using Python  
**Internship Program**: Sysslan IT Solutions Internship Project  
**Author / Presenter**: Krunal Sakpal (Python Developer & QA Engineer)  
**Deliverable**: `documentation/presentation_script.md`  
**Estimated Video Duration**: 8–10 Minutes  

---

## 1. Introduction (0:00 – 0:45)
**[Visual: Title Slide — Project Title, Presenter Name, Sysslan IT Solutions Logo/Branding]**

> "Hello everyone! Welcome to the final project presentation for my Python data engineering and analytics internship. Today, I am excited to walk you through the design, implementation, and empirical insights of the **Train Schedule Analysis and Interactive Route Enquiry System**."

---

## 2. Internship & Host Organization (0:45 – 1:15)
**[Visual: Sysslan IT Solutions Internship Scope Slide & Tech Stack Icons: Python, Pandas, Matplotlib, Seaborn, Pytest]**

> "This project was conducted as part of the **Sysslan IT Solutions Internship Program**. Over the course of this internship, my objective was to apply defensive software engineering, exploratory data analysis, and test-driven quality assurance practices to real-world transportation timetable datasets using Python."

---

## 3. Project Title & Overview (1:15 – 1:45)
**[Visual: Project Architecture Flowchart from Raw Data -> Cleaning -> Analytics -> Interactive App]**

> "The project is titled **'Train Schedule Analysis and Interactive Route Enquiry System Using Python'**. It combines large-scale data cleansing, journey reconstruction across midnight rollovers, empirical traffic clustering, and an in-memory interactive command-line enquiry engine delivering direct train routes with sub-5 millisecond latency."

---

## 4. Problem Statement (1:45 – 2:30)
**[Visual: Diagram illustrating Stop-Level rows vs. Reconstructed Train Journeys]**

> "The core challenge lies in raw schedule complexity:
> 1. Timetable records are stored as individual station halts rather than complete train journeys.
> 2. Journey durations must be calculated across midnight rollovers without explicit calendar dates.
> 3. Data hygiene must protect circular loop routes and edge cases (such as the station code `'NAN'` for Nanogaon Road).
> 4. Passengers and operators need an instant, reliable enquiry tool to discover direct trains between any two stations in India."

---

## 5. Dataset Architecture & Raw Characteristics (2:30 – 3:15)
**[Visual: Dataset Schema Table and SHA-256 Checksum Badge]**

> "Our read-only source of truth is `data/raw/Dataset1.csv`, verified with SHA-256 checksum `8353639af562e88ceb8feb26454221d50fc97b38dc752e3fe6a7a0235f9ecd57`.
> • It contains **186,074 station-level halt rows** across **12 raw columns**.
> • It encompasses **11,113 unique trains** and **8,147 distinct stations**.
> • It has zero missing values in the raw state, and distances range from 0 to 4,260 kilometers."

---

## 6. Level 1: Basic Data Review (3:15 – 4:00)
**[Visual: Table 1.1 Overview and Table 1.4 Max/Min Stops preview]**

> "In Level 1, we reconstructed train journeys by grouping rows on `Train_No` and ordering them by track distance and sequence numbers (`SN`).
> • We mapped all 11,113 train origin-terminus pairs.
> • We evaluated stop distributions: the national average is 16.75 stops per train (median 13 stops).
> • We identified **Train 58141** (Tatanagar to Itwari Passenger) as holding the national record with **114 station halts** over an 887 km run, alongside 74 non-stop express shuttles with only 2 terminal stops."

---

## 7. Level 2: Simple Data Processing (4:00 – 4:45)
**[Visual: Formula for single-day rollover + Route Classification Tercile distribution]**

> "In Level 2, we converted timestamps to standard 24-hour formats and computed journey durations using single-day midnight rollover arithmetic.
> • 9,185 trains (82.65%) complete same-day runs, while 1,922 trains (17.29%) cross midnight.
> • We established empirical, data-driven tercile thresholds:
>   - **Short Routes** ($\le 80$ min): 3,860 trains (mean 49.5 min) — suburban EMUs.
>   - **Medium Routes** (81–240 min): 3,518 trains (mean 142.0 min) — intercity passenger shuttles.
>   - **Long Routes** ($> 240$ min): 3,735 trains (mean 637.3 min) — long-distance trunk expresses."

---

## 8. Level 3: Data Quality Checks & Monotonicity (4:45 – 5:30)
**[Visual: Data Quality Summary Table + Monotonicity Validation Graphs]**

> "Level 3 ensured total dataset integrity before advanced modeling:
> • **Zero-Null Invariant**: Isolated 3,906 origin arrival and terminus departure 00:00:00 null-markers using boolean validity flags.
> • **Edge-Case Protection**: Preserved `'NAN'` (Nanogaon Road) from accidental parser NaN coercion.
> • **Deduplication Defense**: Preserved all 60 legitimate repeat visits on 20 circular/loop routes (e.g. Darjeeling Joyrides and Delhi Ring Railway).
> • **Monotonicity**: Verified 100% distance monotonicity along station sequence (0 negative diffs across all 11,113 trains).
> • Exported the finalized `data/processed/dataset_verified.csv` with 21 enriched columns and 100% row retention."

---

## 9. Level 4: Exploratory Analysis & Visualizations (5:30 – 6:15)
**[Visual: Duration Comparison Bar Chart (`task_4_3_duration_by_route_type.png`) and Top 15 Busiest Stations Chart (`task_4_3_high_traffic_stations.png`)]**

> "In Level 4, we visualized duration hierarchies and station traffic:
> • As seen in Figure 4.1, Long routes exhibit an 82.3-minute positive skew between mean (637.3 min) and median (555.0 min) due to trans-continental trunk runs reaching up to 23.9 hours.
> • Using the statistically defensible 90th percentile threshold ($\ge 48$ trains), we isolated **830 high-traffic stations** (10.19% of network) handling the vast majority of passenger transit.
> • Top national hubs: **CSMT (1,027 trains)**, **Kalyan (828 trains)**, and **Thane (796 trains)** in Mumbai, alongside **Sealdah (745)** and **Howrah (699)** in Kolkata, and **Chennai Beach (738)** in Chennai."

---

## 10. Level 5: Advanced Cross-tabulations & Heatmaps (6:15 – 7:00)
**[Visual: Station Pivot Heatmap (`task_5_3_station_pivot_heatmap.png`) and Fleet Composition Bar Chart (`task_5_3_route_crosstab_bar.png`)]**

> "Level 5 explored structural relationships across railway services:
> • Our station heatmap reveals tripartite operational specialization: commuter terminals (CSMT: 804 Short trains), regional transit hubs (Sealdah: 348 Medium trains), and arterial express junctions (Vijayawada BZA: 316 Long trains, Vadodara BRC: 307 Long trains).
> • Cross-tabulating train series prefixes confirmed that Mail/Express (`1xxxx`) provides 53.49% of all Long routes nationwide (1,998 trains), while Mumbai Suburban (`9xxxx`) supplies 40.88% of all Short routes nationwide (1,578 trains)."

---

## 11. Level 6: Interactive Route Enquiry System (Live Demo) (7:00 – 8:00)
**[Visual: Terminal Recording / Live Screen Share running `python app/train_enquiry.py` and searching `CSMT` -> `KYN` and `BZA` -> `MAS`]\**

> "Now, let's look at the interactive application: `app/train_enquiry.py`.
> • On launch, the engine builds an in-memory inverted station-to-train index, allowing instant route queries in under 5 milliseconds.
> • Let's query from **CSMT** to **KYN**: The system immediately finds **144 direct trains**, sorted by departure time, displaying intermediate stop counts, segment distance (53 km), and elapsed travel duration.
> • It accepts station codes, full names (e.g. `CST-MUMBAI`), or aliases like `CHENNAI CENTRAL`.
> • It includes complete defensive error handling: searching for disconnected city pairs (e.g. `KOTA JN` to `DIBRUGARH`) gracefully reports zero direct trains, and invalid inputs are clearly rejected."

---

## 12. Key Findings Summary & QA Verification (8:00 – 8:45)
**[Visual: Summary Matrix of Key Findings & Pytest 83/83 Passed Banner]**

> "To recap our core project outcomes:
> 1. **Verified Empirical Metrics**: Every single finding is 100% cited and reproducible from `outputs/`.
> 2. **Automated Testing Suite**: We constructed a modular test suite of **83 automated pytest test cases** spanning data loading, time parsing, deduplication, pivot reconciliation, and CLI integration — passing with **100% compliance in 39.24s**.
> 3. **9-Part Evidence Chain**: An automated audit script confirmed that all 21 tasks possess their complete implementation, output data, visual screenshots, documentation notes, session logs, and Git checkpoint commits."

---

## 13. Challenges, Limitations, Future Scope & Conclusion (8:45 – 9:30)
**[Visual: Conclusion Slide with GitHub Repository Link & Acknowledgements]**

> "In conclusion, this project demonstrates end-to-end data pipeline design, rigorous data validation, and clean application architecture.
> • **Known Limitations**: The raw timetable does not include calendar day masks, meaning multi-day journeys are modeled with single-day rollovers.
> • **Future Scope**: Future enhancements will include multi-hop graph routing (Dijkstra's algorithm for connecting trains) and a Streamlit interactive web map.
> • **Acknowledgements**: Sincere thanks to **Sysslan IT Solutions** for the guidance, mentorship, and opportunity to build this project.
> 
> Thank you! All code, datasets, visual charts, and documentation are available on our GitHub repository."

---
