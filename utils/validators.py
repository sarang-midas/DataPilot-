from __future__ import annotations
import pandas as pd


def validate_dataframe(df: pd.DataFrame) -> tuple[bool,str]:
    if not isinstance(df,pd.DataFrame): return False,"The loaded object is not a table."
    if df.empty: return False,"The dataset is empty. Please upload a file with at least one data row."
    if df.shape[1] == 0: return False,"The dataset contains no columns."
    return True,"OK"
