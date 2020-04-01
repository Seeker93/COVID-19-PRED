"""This file aims to create the input for the model
"""

import numpy as np
import pandas as pd

def expand_cases_to_vector(data):
  """Receives the cases dataframe and expands it, creating a row per each day
  time lapse.
  """

  dates_num = len(data.columns) - 1
  dates = data.columns[1:].tolist()
  countries = data["Country"].unique().tolist()

  #print(f"Total countries: {len(countries)}")
  #print(f"Total Dates: {dates_num}")

  # Empty template to fill with data
  rows = (dates_num-1) * len(countries)

  output = pd.DataFrame( \
                      columns=[
                      "Country",
                      "Date",
                      "Cases",
                      "Popden",
                      "Masks",
                      "Poprisk",
                      "Lockdown",
                      "Borders",
                      "NextDay"
                    ])

  for j in range(len(countries)):

    # Cases data from the country row
    country_data = data[ data["Country"] == countries[j] ].values.tolist()
    country_data = country_data[0][1:]

    for i in range(dates_num-1):

      output.loc[len(output)] = [countries[j],
                                 dates[i],
                                 country_data[i], 
                                 0, 0, 0, 0, 0, 
                                 country_data[i+1]]

  # print(f"Temp: {output}")

  return output

def fill_df_column_with_value(df, colname, source_df, source_col, default):
  """Takes the specified column from the source dataframe and inserts its data
  wisely in the specified column of the target dataframe. It admits a default
  value in case the value doesn't exist in the source.

  Wisely stands for based on the "Country" value of both dataframes.
  """

  countries = df["Country"].unique().tolist()

  for country in countries:

    #a, b, c = colname, country, source_df.loc[ source_df["Country"] == country, source_col].values
    #print(f"Feature {a} inserting country {b} value {c}")
    if country in source_df["Country"].tolist():
      df.loc[ df["Country"] == country, colname ] = \
            source_df.loc[ source_df["Country"] == country, source_col].values
    else:
      df.loc[ df["Country"] == country, colname ] = default

  # return df

def fill_df_column_date_based(df, colname, source_df, default):
  """Takes the specified column from the source dataframe and inserts its data
  wisely in the specified column of the target dataframe. It admits a default
  value in case the value doesn't exist in the source.

  Wisely stands for based on the "Country" value of both dataframes, and
  matching the dates in source and target.

  For those dates where no value is specified in the source, the latest value
  is kept.
  """

  countries = df["Country"].unique().tolist()

  for country in countries:

    if country in source_df["Country"].tolist():

      data = source_df.loc[ source_df["Country"] == country].T.values
      # Extend the latest value up to the lenght needed
      lenght_difference = len(df[df["Country"] == country]) - len(data)

      #from IPython import embed
      #embed()

      data = data.tolist() + [data[-1].tolist()] * (lenght_difference+1)
      
      # Remove the country name at the beginning
      data = data[1:]

      df.loc[ df["Country"] == country, colname ] = data
            
    else:

      df.loc[ df["Country"] == country, colname ] = default