import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class RetailSalesAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """Load CSV data using Pandas"""
        if not os.path.exists(self.file_path):
            print("File not found.")
            return False

        if not self.file_path.endswith(".csv"):
            print("Invalid file format. Please provide a CSV file.")
            return False

        self.data = pd.read_csv(self.file_path)
        print("Data loaded successfully.")
        return True

    def clean_data(self):
        """Handle missing values and create total sales column"""
        self.data.dropna(inplace=True)
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data["Total Sales"] = self.data["Price"] * self.data["Quantity Sold"]

    def calculate_metrics(self):
        """Calculate key metrics using NumPy"""
        total_revenue = np.sum(self.data["Total Sales"])
        average_sales = np.mean(self.data["Total Sales"])

        top_product = (
            self.data.groupby("Product")["Total Sales"]
            .sum()
            .idxmax()
        )

        print("\nKey Metrics")
        print(f"Total Revenue: ₹{total_revenue}")
        print(f"Average Sale Value: ₹{average_sales:.2f}")
        print(f"Top-Selling Product: {top_product}")

    def filter_data(self):
        """Filter data by category"""
        category = input("\nEnter category to filter (or press Enter to skip): ")
        if category:
            filtered = self.data[self.data["Category"] == category]
            if filtered.empty:
                print("No data found for this category.")
            else:
                print(filtered)

    def visualize_data(self):
        """Generate required visualizations"""
        sns.set(style="whitegrid")

        # Bar Chart: Sales by Category
        category_sales = self.data.groupby("Category")["Total Sales"].sum()
        category_sales.plot(kind="bar", title="Total Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Sales")
        plt.show()

        # Line Graph: Sales Trend Over Time
        daily_sales = self.data.groupby("Date")["Total Sales"].sum()
        daily_sales.plot(title="Sales Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Sales")
        plt.show()

        # Heatmap: Price vs Quantity
        pivot = pd.pivot_table(
            self.data,
            values="Total Sales",
            index="Price",
            columns="Quantity Sold",
            aggfunc=np.sum
        )

        sns.heatmap(pivot, cmap="coolwarm")
        plt.title("Heatmap: Price vs Quantity Sold")
        plt.show()


def main():
    file_path = input("Enter path to retail sales CSV file: ")

    analyzer = RetailSalesAnalyzer(file_path)

    if analyzer.load_data():
        analyzer.clean_data()
        analyzer.calculate_metrics()
        analyzer.filter_data()
        analyzer.visualize_data()


if __name__ == "__main__":
    main()