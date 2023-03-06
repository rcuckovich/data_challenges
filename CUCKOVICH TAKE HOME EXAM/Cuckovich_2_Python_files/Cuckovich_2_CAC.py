#  This is how I get pytest to pick up the file during testing

import pandas as pd
import numpy as np

# Global variables to be updated between runs
curr_mu_purch = .5
curr_mu_max_purch = .8
curr_phi_prod = .05

# Import the data
df_cac = pd.read_json(r'C:\Users\rcuck\YvesBlue\cac_data.json')

# Look at the data
print(df_cac)
print(df_cac.head())
print(df_cac.info())
print(df_cac.describe())
print(df_cac.columns)


def strawman_org_emissions(df, mu_purch=.5, mu_max_purch=.8, phi_prod=.05):
    # Do data cleaning

    # Not sure if we want to clean everything with future data in mind or target only existing data
    # I have selected cleaning everything but am leaving this here commented out as an option
    # df.replace('Inconclusive', np.nan, inplace=True) 
    # df['Renewable Energy Purchased'] = pd.to_numeric(df['Renewable Energy Purchased'], errors='coerce')

    # Change objects to float -- am including CO2 Analytic even though not in formula
    # I would double check that the person asking for the data wants the output to be np.nan for rows that can't be computed
    cols_to_clean = df.columns.drop('ISIN') 
    df[cols_to_clean] = df[cols_to_clean].apply(pd.to_numeric, errors='coerce')
    
    # The above is the more elegant way to clean all columns
    #df['Total Energy Use'] = pd.to_numeric(df['Total Energy Use'], errors='coerce')
    #df['Total CO2 Equivalents Emissions'] = pd.to_numeric(df['Total CO2 Equivalents Emissions'], errors='coerce')
    #df['Renewable Energy Purchased'] = pd.to_numeric(df['Renewable Energy Purchased'], errors='coerce')
    #df['Renewable Energy Produced'] = pd.to_numeric(df['Renewable Energy Produced'], errors='coerce')
    #df['Carbon Credit Value'] = pd.to_numeric(df['Carbon Credit Value'], errors='coerce')
    #df['CO2 Analytic'] = pd.to_numeric(df['CO2 Analytic'], errors='coerce')
        
    # mask to identify any rows with non-numeric values or zero in a denominator
    mask1 = df['Total Energy Use'] > 0  # Notice zero not included because denominator value
    mask2 = df['Total CO2 Equivalents Emissions'] >= 0
    mask3 = df['Renewable Energy Purchased'] >= 0
    mask4 = df['Renewable Energy Produced'] >= 0
    mask5 = df['Carbon Credit Value'] >= 0
    mask = mask1 & mask2 & mask3 & mask4 & mask5

    
    df.loc[mask, 'C02 Adjusted Total'] = (df['Total CO2 Equivalents Emissions'] - df['Carbon Credit Value']) * (1 - np.minimum((mu_purch * df['Renewable Energy Purchased'] / df['Total Energy Use']), mu_max_purch)) - (phi_prod * df['Renewable Energy Produced'])
    
    return df
