import pandas as pd
import os

input_folder = "../data/nasdaq"
output_folder = "../cleaned_data/nasdaq"

os.makedirs(output_folder, exist_ok=True)

column_names = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)

        # Read CSV, skip first 3 rows, and assign column names
        df = pd.read_csv(file_path, skiprows=3, names=column_names)

        # Convert date column and set it as index
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        df.set_index('Date', inplace=True)

        # Ensure numeric types
        for col in ['Close', 'High', 'Low', 'Open', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Sort chronologically
        df.sort_index(inplace=True)

        # Save cleaned CSV
        output_path = os.path.join(output_folder, filename)
        df.to_csv(output_path)

        print(f"Cleaned and saved: {output_path}")
