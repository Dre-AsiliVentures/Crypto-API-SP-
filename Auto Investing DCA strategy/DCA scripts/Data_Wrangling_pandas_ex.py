import pandas as pd

# Creating DataFrames -conventional 
df1=pd.DataFrame(
    {
        "a" :[4,5,6],
        "b" :[7,8,9],
        "c" :[10,11,12]
    },
    index=[1,2,3]
)
print(df1)
# Creating DataFrames using Multi_Index
df2=pd.DataFrame(
    {
        "a" :[4,5,6],
        "b" :[7,8,9],
        "c": [10,11,12]
    },
    index=pd.MultiIndex.from_tuples
    (
        [('d',1),('d',2),
        ('e',3)],names=['n','v']
    )
)
print(df2)