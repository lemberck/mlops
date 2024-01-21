import pandas as pd

def analyze(data: pd.DataFrame):
    """Performs the analysis of sales data.

    Args:
        data (pd.DataFrame): Sales data.
    """
    # Calculate total sales for each product
    data["Total Sales"] = data["Sold Quantity"] * data["Unit Price"]

    # Calculate total sales of the company
    total_company = data["Total Sales"].sum()

    # Print the results
    print("Total sales per product:")
    print(data.groupby("Product")["Total Sales"].sum())
    print("\nTotal sales of the company:", total_company)

if __name__ == "__main__":
    # Read csv
    data = pd.read_csv("data/sales_data.csv")

    # Call function to analyze data
    analyze(data)

    