#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
df = pd.read_csv("insurance.csv")
df['age'] = np.random.permutation(df['age'].values)
df['DOB'] = np.random.permutation(df['DOB'].values)
df['name'] = np.random.permutation(df['name'].values)
df.describe()

