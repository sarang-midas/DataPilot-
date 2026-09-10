import io

import pandas as pd

from core.anomaly_engine import detect_anomalies, forecast_linear
from core.column_detector import detect_columns
from core.data_cleaner import CleaningConfig, clean_dataframe
from core.data_loader import read_excel_bytes
from core.visualization_engine import custom_chart


def test_cleaner_numeric_constant_and_duplicate_headers():
    df = pd.DataFrame([[1, None, " A ", 5], [2, 10, "B", 6]], columns=["id", "amount", " name ", " name "])
    out, log, _, _ = clean_dataframe(df, CleaningConfig(missing_numeric="Constant", missing_constant="99"))
    assert list(out.columns) == ["id", "amount", "name", "name_2"]
    assert out["amount"].isna().sum() == 0
    assert float(out.loc[0, "amount"]) == 99
    assert any("Handled" in item for item in log)


def test_excel_loader_reads_non_empty_sheets():
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        pd.DataFrame({"id": [1, 2], "sales": [10, 20]}).to_excel(writer, index=False, sheet_name="Sales")
        pd.DataFrame().to_excel(writer, index=False, sheet_name="Empty")
    result = read_excel_bytes(buf.getvalue())
    assert list(result) == ["Sales"]
    assert len(result["Sales"]) == 2


def test_anomaly_and_forecast_smoke():
    dates = pd.date_range("2026-01-01", periods=12, freq="D")
    df = pd.DataFrame({"date": dates, "sales": [10, 11, 10, 12, 11, 13, 12, 14, 100, 13, 14, 15]})
    profile = detect_columns(df)
    anomalies = detect_anomalies(df, profile, "IQR")
    forecast = forecast_linear(df, "date", "sales", 3)
    assert not anomalies.empty
    assert len(forecast) == 3


def test_custom_chart_handles_same_prn_column_for_category_and_metric():
    df = pd.DataFrame(
        {
            "prn": [1001, 1001, 1002],
            "student_name": ["Asha", "Bala", "Chen"],
            "attendance": [90, 80, 95],
        }
    )

    figure = custom_chart(df, "bar", "prn", "prn", "sum")

    assert len(figure.data) == 1
