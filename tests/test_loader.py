from core.data_loader import read_csv_bytes

def test_csv_loader():
    data=b"id,name,sales\n1,Alice,10\n2,Bob,20\n"
    df=read_csv_bytes(data)
    assert list(df.columns)==["id","name","sales"]
    assert len(df)==2
