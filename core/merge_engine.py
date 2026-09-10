from __future__ import annotations
import pandas as pd

def common_keys(left: pd.DataFrame, right: pd.DataFrame) -> list[str]:
    return [str(c) for c in left.columns if c in set(map(str,right.columns))]

def merge_frames(left: pd.DataFrame, right: pd.DataFrame, left_on: str, right_on: str, how: str) -> pd.DataFrame:
    return left.merge(right, left_on=left_on, right_on=right_on, how=how, suffixes=("_left","_right"))
