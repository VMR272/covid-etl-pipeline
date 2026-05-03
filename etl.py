import pandas as pd
import boto3
import io
from datetime import datetime

# ================================================
# CONFIGURATION
# ================================================
BUCKET_NAME = "covid-etl-vineeth"
S3_FOLDER = "processed/"
LOCAL_FILE = "country_wise_latest.csv"

# ================================================
# STEP 1 - EXTRACT
# Read raw COVID data from local CSV file
# ================================================
def extract():
    print("🔵 EXTRACT: Reading COVID data from local file...")
    df = pd.read_csv(LOCAL_FILE)
    print(f"✅ Extracted {len(df)} rows and {len(df.columns)} columns")
    print(f"   Columns found: {list(df.columns)}")
    return df

# ================================================
# STEP 2 - TRANSFORM
# Clean and enrich the data
# ================================================
def transform(df):
    print("\n🟡 TRANSFORM: Cleaning data...")

    # Rename columns for cleanliness (remove spaces)
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("/", "_")

    # Keep only useful columns
    columns_to_keep = [
        "Country_Region",
        "Confirmed",
        "Deaths",
        "Recovered",
        "Active",
        "New_cases",
        "New_deaths",
        "New_recovered"
    ]

    # Only keep columns that exist in the file
    columns_to_keep = [col for col in columns_to_keep if col in df.columns]
    df = df[columns_to_keep]

    # Drop rows where Confirmed is null or zero
    df = df[df["Confirmed"].notna()]
    df = df[df["Confirmed"] > 0]

    # Fill nulls with 0
    df = df.fillna(0)

    # Add death rate column
    df["Death_Rate_%"] = (
        (df["Deaths"] / df["Confirmed"]) * 100
    ).round(2)

    # Add recovery rate column
    df["Recovery_Rate_%"] = (
        (df["Recovered"] / df["Confirmed"]) * 100
    ).round(2)

    # Sort by Confirmed cases descending
    df = df.sort_values("Confirmed", ascending=False).reset_index(drop=True)

    print(f"✅ Transformed data: {len(df)} rows remaining")
    print(f"   Columns: {list(df.columns)}")
    print(f"\n   Top 5 countries by confirmed cases:")
    print(df[["Country_Region", "Confirmed", "Deaths", "Death_Rate_%"]].head())
    return df

# ================================================
# STEP 3 - LOAD
# Upload cleaned data to AWS S3
# ================================================
def load(df):
    print("\n🟢 LOAD: Uploading to AWS S3...")

    # Convert dataframe to CSV in memory
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # Create S3 client
    s3_client = boto3.client("s3", region_name="ap-southeast-2")

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{S3_FOLDER}covid_cleaned_{timestamp}.csv"

    # Upload to S3
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=csv_buffer.getvalue()
    )

    print(f"✅ Uploaded to s3://{BUCKET_NAME}/{file_name}")
    return file_name

# ================================================
# MAIN - Run the pipeline
# ================================================
def run_pipeline():
    print("=" * 50)
    print("   COVID ETL PIPELINE - by Vineeth M R")
    print("=" * 50)

    raw_data = extract()
    clean_data = transform(raw_data)
    load(clean_data)

    print("\n" + "=" * 50)
    print("✅ PIPELINE COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()
