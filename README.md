

E-Commerce Sales & Returns Analysis MamaEarth Returns and  Growth intelligence pipeline

This project analyzes e-commerce orders to identify revenue trends, return patterns, and high-risk customer segments. The repository contains SQL analysis, Python EDA, visualizations, and a GenAI narrative layer.

Repository Structure
<repo>/
├── README.md
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
└── narrator/
    ├── findings.json
    └── generate_narrative.py
1. SQL Setup and Reports

Open MySQL and run the SQL files in this order:

SOURCE sql/schema.sql;
SOURCE sql/seed_data.sql;
SOURCE sql/reports.sql;

schema.sql creates the database tables, seed_data.sql loads the data, and reports.sql runs the required business reports and revenue calculations.

2. Python Analysis and Visualizations

From the repository root, run:

python analysis/clean_and_eda.py
python analysis/visualize.py

The first script loads and cleans the CSV files, performs EDA, calculates revenue and return rates, and completes the required analysis tasks. Task 5 of Part 2 writes the verified results to narrator/findings.json.

The visualization script creates:

visualizations/return_rate_by_payment.png
visualizations/monthly_revenue_trend.png
3. GenAI Narrative

Set your Gemini API key as an environment variable:

export GEMINI_API_KEY="your_api_key"
python narrator/generate_narrative.py

On Windows PowerShell:

$env:GEMINI_API_KEY="your_api_key"
python narrator/generate_narrative.py

Alternatively, run without an API key:

python narrator/generate_narrative.py

Without a key, the script automatically uses its offline deterministic narrative path based on narrator/findings.json.
