# Superstore Executive Profit Optimization Analysis

An end-to-end data analytics case study designed to move past surface-level aggregate financial success to isolate, quantify, and mitigate hidden corporate profit leakage.

## 🔗 Project Deliverables
* **Interactive Dashboard:** [Live Tableau Public Dashboard](https://public.tableau.com/views/SuperstoreExecutiveProfitOptimizationDashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
* **Formal Business Report:** Available in Markdown format [here](./deliverables/executive_briefing_memo.md) or via [PDF](./deliverables/Report.pdf).

## 📌 Executive Core Insights
* **The Aggregate Trap:** The enterprise maintains an overall healthy margin of 12.5% ($286K profit on $2.30M sales), hiding massive value destruction in specific segments.
* **The 20% Discount Cliff:** Promotional discounts exceeding 20% completely invert the P&L, cascading to a catastrophic -119.2% margin at the 50%+ discount band, resulting in $135,376 of destroyed profit.
* **The Tactical Target:** 7.6% of historical order volume (Standard Class shipments intersecting with Furniture/Office Supplies carrying over 20% discounts) accounts for nearly half ($65,387) of all promotional value destruction.

## 📁 Repository Navigation
* `/charts`: Exported high-resolution data visualizations mapping out margin behavior.
* `/data`: Contains the historical transaction database.
* `/deliverables`: Holds the final executive briefing documentation, compiled PDFs, and interactive system screenshots.

## 🛠️ Tech Stack & Methodology
* **Data Engineering:** Python (Pandas) for multi-dimensional transaction auditing and custom financial band calculations.
* **Business Intelligence:** Tableau Public for dual-axis volume modeling, highlight matrix generation, and interactive dashboard deployment.

## 🌐 Data Source & Attribution
The dataset used in this analysis is a historical transaction log representing retail enterprise operations. 
* **Primary Source:** Publicly hosted via the [Salesforce Trailblazer Community](https://trailhead.salesforce.com/trailblazer-community/feed/0D5KX00000kQPXv0AO).
* **Curation Archive:** Sourced from the [Superstore Dataset Archive on Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final/).
* **Acknowledgements:** All credit belongs to the original creators and authors at Tableau/Salesforce. This project is structured strictly for educational and portfolio demonstration purposes under fair use.