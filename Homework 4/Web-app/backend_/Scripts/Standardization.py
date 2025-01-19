import pandas as pd
from babel.numbers import parse_decimal


# Used to convert strings from the macedonian format to number format without comma, dots and vice versa
# Used to sort data based on the data
class Standardization:

    def _safe_locale_conversion(self, val):
        if val in [None, "", 'nan']:
            return 'nan'
        return parse_decimal(str(val), locale='de')

    def _clean_Volume(self, vol):
        std = []
        for number in vol:
            if number in [None, "", 'nan']:
                std.append('nan')

            number = float(number)  # Ensure the number is float
            if number.is_integer():
                std.append(int(number))  # Append as integer
            else:
                # Replace decimal separator (if needed) and append as integer
                std.append(int(str(number).replace(".", "").replace(",", "")))
        return std

    def _convert_column(self, col):
        return col.apply(self._safe_locale_conversion)

    def _to_numbers(self, df: pd.DataFrame):
        # Converts strings in to numbers
        try:
            for col in df.columns:
                if col == 'Date':
                    continue

                if col == 'Volume':
                    df[col] = self._clean_Volume(df[col])
                    continue
                df[col] = self._convert_column(df[col])
            return df
        except Exception as e:
            print(e)

    def _dates(self, df: pd.DataFrame):
        # Sorts data based on the date
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by="Date", ascending=True)
        df["Date"] = df["Date"].dt.strftime('%m/%d/%Y')
        return df

    def standardization(self, df: pd.DataFrame):
        # Converts the strings to numbers and sorts the data
        copy = df.copy()
        copy = self._to_numbers(copy)
        copy = self._dates(copy)
        return copy

    def _format_number_manual(self, number): # Converts a number to a string number with dots and commas
        formatted = f"{number:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        return formatted

    def de_standardization(self, df: pd.DataFrame): # Converts a column from numbers to strings
        for column in df.columns:
            if column == 'Date':
                continue
            df[column] = df[column].apply(self._format_number_manual)

        return df
