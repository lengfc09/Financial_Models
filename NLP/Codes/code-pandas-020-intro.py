# This script gives a brief introduction on pandas in Python.

import pandas as pd
import numpy as np

df = \
    pd.DataFrame(
        np.random.randn(6, 4),  # 6x4 numpy array with random numbers.
        index=pd.date_range('2019-12-20', periods=6),
        columns=['A', 'B', 'C', 'D'])
df.head()                       # Top rows.
df.tail(3)                      # Bottom 3 rows.
df['A']                         # Look at column named 'A'.
df[0:3]                         # First three rows.
df.apply(lambda x: x.max() - x.min()) # Apply a function to the data.

# The key thing about a DataFrame is that its columns can hold data of
# different types.
df2 = \
    pd.DataFrame(
        { 'A' : 1.,
          'B' : pd.Timestamp('2019-12-20'),
          'C' : pd.Series(1, index=list(range(4)), dtype='float32'),
          'D' : np.array([3] * 4, dtype='int32'),
          'E' : pd.Categorical(["test", "train", "test", "train"]),
          'F' : 'foo' })
df2.dtypes                      # Look at data types.
