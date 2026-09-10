import pandas as pd
from core.column_detector import detect_columns
from core.kpi_engine import generate_kpis

def test_kpis():
    df=pd.DataFrame({"order_id":[1,2,3],"sales":[100,200,300],"profit":[20,40,60]})
    p=detect_columns(df); k=generate_kpis(df,p)
    labels=[x["label"] for x in k]
    assert any("Sales" in x for x in labels)
    assert any("Margin" in x for x in labels)
