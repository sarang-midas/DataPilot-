import pandas as pd
from core.data_cleaner import CleaningConfig, clean_dataframe

def test_cleaning_trim_fill_duplicate():
    df=pd.DataFrame({"name":[" Alice ",None,"Alice"],"sales":[10,None,10]})
    out,log,bq,aq=clean_dataframe(df,CleaningConfig())
    assert out["name"].iloc[0]=="Alice"
    assert out["sales"].isna().sum()==0
    assert len(out)==1
    assert aq["score"]>=bq["score"]
