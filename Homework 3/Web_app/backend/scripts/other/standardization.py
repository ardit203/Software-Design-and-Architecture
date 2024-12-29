import time
import os
import pandas as pd

normal = 'D:/Faculty/5th Semester/PYTHON/backend/database/normal'
standard = 'D:/Faculty/5th Semester/PYTHON/backend/database/standard'



def to_numbers(df: pd.DataFrame):
    try:
        # print(f"Processing {code}")
        def clean_column(col):
            return col.astype(str).str.replace(r'\.', '', regex=True).str.replace(r',', '.', regex=True)

        def clean_Volume(vol):
            std = []
            for number in vol:
                if number % 1 == 0:
                    std.append(int(number))
                else:
                    std.append(int(str(number).replace(r'.', '')))
            return std

        # df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')  # Handle invalid dates
        df['Last trade price'] = clean_column(df['Last trade price']).astype(float)
        df['Max'] = clean_column(df['Max']).astype(float)
        df['Min'] = clean_column(df['Min']).astype(float)
        df['Avg.Price'] = clean_column(df['Avg.Price']).astype(float)
        df['%chg.'] = df['%chg.'].replace(r',', '.', regex=True).astype(float)
        df['Volume'] = clean_Volume(df['Volume'])
        df['Turnover in BEST in denars'] = clean_column(df['Turnover in BEST in denars']).astype(float)
        df['Total turnover in denars'] = clean_column(df['Total turnover in denars']).astype(float)

        # print(f"File created: {code}")
    except Exception as e:
        print(f"Error processing: {e}")


def dates(df: pd.DataFrame):
    # df = content.copy()
    df['Date'] = pd.to_datetime(df['Date'])

    # Set the date as the index
    df.set_index('Date', inplace=True)

    # Create a complete date range from the min to the max date
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')

    # Reindex the DataFrame to include all dates
    df = df.reindex(full_date_range)

    # Reset the index and rename the columns
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)

    return df


def fill(df):
    if 'Last trade price' in df.columns:
        df['Last trade price'] = df['Last trade price'].ffill()

    if 'Max' in df.columns and 'Min' in df.columns:
        df['Max'] = df['Max'].fillna(df['Last trade price'])
        df['Min'] = df['Min'].fillna(df['Last trade price'])


def visual_standardization(df):
    # Make a copy to avoid modifying the original DataFrame
    copy = df.copy()

    to_numbers(copy)
    # Ensure the 'Date' column is in datetime format
    copy['Date'] = pd.to_datetime(copy['Date'], errors="coerce")

    # Drop rows with invalid dates (optional)
    copy = copy.dropna(subset=["Date"])

    # Sort by the 'Date' column
    copy = copy.sort_values(by="Date")

    # Format the 'Date' column
    copy["Date"] = copy["Date"].dt.strftime('%m/%d/%Y')

    # Print the formatted 'Date' column for debugging
    # print(copy["Date"])

    return copy


def standardization(df: pd.DataFrame):
    copy = df.copy()
    to_numbers(copy)
    copy = dates(copy)
    fill(copy)
    return copy


def format_number_manual(number):
    formatted = f"{number:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
    return formatted


def de_standardization(df: pd.DataFrame):
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    # Convert 'Last trade price' to string and replace '.' with ','
    df['LTP'] = df['Last trade price'].apply(format_number_manual)

    return df
