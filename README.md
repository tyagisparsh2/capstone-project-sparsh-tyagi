E-Commerce Sales & Returns Analysis

This project analyzes e-commerce orders to identify revenue trends, return patterns, and high-risk customer segments. It combines MySQL, Python EDA, visualizations, and a GenAI narrative layer.

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

Run the SQL files in this order using MySQL:

SOURCE sql/schema.sql;
SOURCE sql/seed_data.sql;
SOURCE sql/reports.sql;

schema.sql creates the database tables, seed_data.sql loads the customer, product, and order data, and reports.sql runs the required reports and revenue calculations.

2. Python Analysis and Visualizations

From the repository root, run:

python analysis/clean_and_eda.py
python analysis/visualize.py

clean_and_eda.py loads the three CSV files, cleans the data, performs the required EDA, calculates revenue and return rates, and completes the Part 2 analysis.

Task 5 of Part 2 writes the verified analysis results to:

narrator/findings.json

visualize.py creates the following PNG files:

visualizations/return_rate_by_payment.png
visualizations/monthly_revenue_trend.png
3. GenAI Narrative

To use the Gemini API, set your API key as an environment variable before running the script.

Windows PowerShell
$env:GEMINI_API_KEY="your_api_key"
python narrator/generate_narrative.py
Linux / macOS
export GEMINI_API_KEY="your_api_key"
python narrator/generate_narrative.py

The script reads the verified values from narrator/findings.json and generates the narrative.

Offline Mode

No API key is required. Simply run:

python narrator/generate_narrative.py

If GEMINI_API_KEY is not available, the script automatically uses the offline deterministic narrative path. This allows the project to run without an external API.
