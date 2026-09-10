import pandas as pd
from core.column_detector import detect_columns
from core.data_quality import quality_report

def test_quality_detects_missing_and_duplicates():
    df=pd.DataFrame({"id":[1,1,2],"sales":[10,None,30],"region":["West","west","West"]})
    p=detect_columns(df); q=quality_report(df,p)
    assert q["missing"]==1
    assert q["duplicates"]==0
    assert q["score"]<100
