# 🦠 COVID-19 ETL Pipeline — AWS S3

An end-to-end ETL (Extract, Transform, Load) data pipeline built with Python and AWS S3, processing real-world COVID-19 data.

---

## 📌 Project Overview

This pipeline automatically:
- **Extracts** COVID-19 country-wise data from a local CSV source (Kaggle)
- **Transforms** it by cleaning, filtering, and enriching with calculated metrics
- **Loads** the processed data into an AWS S3 bucket for cloud storage

---

## 🏗️ Architecture

```
Local CSV File
     │
     ▼
[EXTRACT] → Read raw data with pandas
     │
     ▼
[TRANSFORM] → Clean nulls, rename columns,
               calculate Death Rate & Recovery Rate,
               sort by confirmed cases
     │
     ▼
[LOAD] → Upload cleaned CSV to AWS S3
     │
     ▼
s3://covid-etl-vineeth/processed/covid_cleaned_<timestamp>.csv
```

---

## 📂 Project Structure

```
covid-etl-pipeline/
├── etl.py                    # Main ETL pipeline script
├── country_wise_latest.csv   # Raw COVID-19 data (Kaggle)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core scripting language |
| pandas | Data extraction and transformation |
| boto3 | AWS SDK — uploads data to S3 |
| AWS S3 | Cloud storage for processed data |
| AWS CLI | Local authentication with AWS |

---

## ⚙️ How It Works

### Extract
Reads `country_wise_latest.csv` containing COVID-19 statistics for 187 countries including confirmed cases, deaths, recoveries, and active cases.

### Transform
- Renames columns (removes spaces and special characters)
- Keeps only relevant columns
- Drops rows with missing or zero confirmed cases
- Fills remaining nulls with 0
- Calculates two new metrics:
  - `Death_Rate_%` = (Deaths / Confirmed) × 100
  - `Recovery_Rate_%` = (Recovered / Confirmed) × 100
- Sorts countries by confirmed cases (descending)

### Load
Converts the cleaned DataFrame to CSV in memory and uploads it to an AWS S3 bucket with a timestamp in the filename, ensuring each pipeline run produces a unique file.

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/covid-etl-pipeline.git
cd covid-etl-pipeline
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure AWS CLI
```bash
aws configure
```
Enter your AWS Access Key, Secret Key, region (`ap-southeast-2`), and output format (`json`).

### 4. Run the pipeline
```bash
python etl.py
```

---

## 📊 Sample Output

```
==================================================
   COVID ETL PIPELINE - by Vineeth M R
==================================================
🔵 EXTRACT: Reading COVID data from local file...
✅ Extracted 187 rows and 15 columns

🟡 TRANSFORM: Cleaning data...
✅ Transformed data: 187 rows remaining

   Top 5 countries by confirmed cases:
  Country_Region  Confirmed  Deaths  Death_Rate_%
0             US    4290259  148011          3.45
1         Brazil    2442375   87618          3.59
2          India    1480073   33408          2.26
3         Russia     816680   13334          1.63
4   South Africa     452529    7067          1.56

🟢 LOAD: Uploading to AWS S3...
✅ Uploaded to s3://covid-etl-vineeth/processed/covid_cleaned_20260503_103652.csv

==================================================
✅ PIPELINE COMPLETE
==================================================
```

---

## 📦 Requirements

```
pandas
boto3
```

---

## 👤 Author

**Vineeth M R**
- Background: Mechanical Engineering (B.Tech) + Data Science (M.S.)
- Upskilling in Data Engineering on AWS
- Email: vineethmravish@outlook.com
