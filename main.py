import numpy as np
import pandas as pd

data = pd.read_csv('btd-2014-2024.csv')

print(data.head())

# We're interested in data["Close"]
