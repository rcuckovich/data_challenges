
import pytest
from Cuckovich_2_CAC import strawman_org_emissions
import pandas as pd

# columns for formula all have numeric, non-zero values
def test_clean_data():
    clean_data = pd.read_json(r'C:\Users\rcuck\YvesBlue\cac_clean_data.json')
    df_clean = strawman_org_emissions(clean_data)
    
    assert int(df_clean.iloc[0]['C02 Adjusted Total']) == int(81902.988458)
    
# columns for formula have one row with text values
def test_non_numeric_data():
    non_numeric_data = pd.read_json(r'C:\Users\rcuck\YvesBlue\cac_non_numeric_data.json')
    df_non_numeric = strawman_org_emissions(non_numeric_data)
    
    assert int(df_non_numeric.iloc[0]['C02 Adjusted Total']) == int(81902.988458)
    
# columns for formula have one row with values of zero
def test_zero_data():
    zero_data = pd.read_json(r'C:\Users\rcuck\YvesBlue\cac_zero_data.json')
    df_zero = strawman_org_emissions(zero_data)
    
    assert int(df_zero.iloc[0]['C02 Adjusted Total']) == int(81902.988458)
    


