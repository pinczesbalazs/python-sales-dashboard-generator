import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_files(folder_path):
    all_data = []

    csv_files = Path(folder_path).glob("*.csv")

    for file in csv_files:
        df = pd.read_csv(file)
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)


def clean_data(df):
    df = df.drop_duplicates()

    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].str.strip()

    df = df.fillna(0)

    return df


def calculate_kpis(df):
    total_revenue = df["Revenue"].sum()
    average_order = df["Revenue"].mean()

    top_product = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    return total_revenue, average_order, top_product


def create_monthly_chart(df):
    monthly_sales = (
        df.groupby("Month")["Revenue"]
        .sum()
    )

    monthly_sales.plot(kind="bar")

    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")

    plt.tight_layout()
    plt.savefig("monthly_revenue.png")
    plt.close()


def export_report(df, total_revenue, average_order, top_product):
    summary = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Average Order Value",
            "Top Product"
        ],
        "Value": [
            total_revenue,
            round(average_order, 2),
            top_product
        ]
    })

    with pd.ExcelWriter("sales_report.xlsx") as writer:
        df.to_excel(writer, sheet_name="Cleaned_Data", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)


def main():
    data = load_files("sales_files")

    cleaned_data = clean_data(data)

    total_revenue, average_order, top_product = calculate_kpis(cleaned_data)

    create_monthly_chart(cleaned_data)

    export_report(
        cleaned_data,
        total_revenue,
        average_order,
        top_product
    )

    print("Report created successfully.")


if __name__ == "__main__":
    main()
