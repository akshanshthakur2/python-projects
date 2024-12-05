import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load the CSV file
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Strip extra spaces from column names
        print(f"Data loaded successfully from {file_path}")
        print("Columns in CSV:", df.columns)  # Print column names for debugging
        return df
    except Exception as e:
        print(f"Error loading file: {str(e)}")
        return None

# Function to display basic statistics
def display_basic_stats(df):
    if 'Data_value' not in df.columns:
        print("'Data_value' column not found in the data. Please check the column names.")
        return

    total_sales = df['Data_value'].sum()
    avg_sales = df['Data_value'].mean()
    total_transactions = len(df)

    print("\nBasic Statistics:")
    print(f"Total Sales: ${total_sales:,.2f}")
    print(f"Average Sales: ${avg_sales:,.2f}")
    print(f"Total Transactions: {total_transactions}")

# Function to plot the sales data
def plot_sales(df):
    # Ensure 'Period' is treated as a datetime object if it's not already
    df['Period'] = pd.to_datetime(df['Period'], errors='coerce')

    plt.figure(figsize=(8, 6))
    sns.lineplot(x='Period', y='Data_value', data=df, marker='o', color='b')
    plt.title("Sales Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to export data to CSV
def export_to_csv(df):
    export_file = "exported_sales_data.csv"
    df.to_csv(export_file, index=False)
    print(f"\nData exported successfully to {export_file}")

# Main function
def main():
    # Load CSV file
    file_path = input("Enter the CSV file path: ")
    df = load_data(file_path)

    if df is not None:
        # Display basic statistics
        display_basic_stats(df)

        # Plot sales data
        plot_sales(df)

        # Export data to CSV
        export_choice = input("\nDo you want to export the data to CSV? (y/n): ")
        if export_choice.lower() == 'y':
            export_to_csv(df)
        else:
            print("\nExport skipped.")

# Run the main function
if __name__ == "__main__":
    main()
