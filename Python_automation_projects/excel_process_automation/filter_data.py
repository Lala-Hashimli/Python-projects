
import pandas as pd


def filter_excel(input_excel, output_excel, filters_excel="filters.xlsx"):

    df = pd.read_excel(input_excel)

    print("Available columns:", list(df.columns))
    print("You can filter by Age, Country, Name")

    try:
        age_limit = int(input("Enter minimum age(or press Enter to skip): ") or 0)
    except ValueError:
        age_limit = 0

    country_filter = input("Enter country to filter (or press Enter to skip): ").strip()
    name_start = input("Enter starting letter(s) of name (or press Enter to skip): ").strip()

    filtered_df = df

    if age_limit > 0:
        filtered_df = filtered_df[filtered_df["Age"] > age_limit]

    if country_filter:
        filtered_df = filtered_df[filtered_df["Country"].str.contains(country_filter, case=False)]

    if name_start:
        filtered_df = filtered_df[filtered_df["Name"].str.startswith(name_start)]

    filtered_df.to_excel(output_excel, index=False)
    print(f"Filtered data saved to {output_excel}")
