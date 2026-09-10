from __future__ import annotations

def recommendations(report: dict) -> list[dict]:
    rec=[]
    if report["missing"]:
        pct=report["missing"] / max(1,report["rows"]*report["columns"])*100
        rec.append({"priority":"High" if pct>5 else "Medium","title":"Review missing values","body":f"{report['missing']:,} missing cells remain ({pct:.1f}% of all cells). Recheck upstream collection or field-level rules."})
    if report.get("duplicate_ids", 0):
        rec.append({"priority":"High","title":"Check duplicate identifiers","body":f"{report.get('duplicate_ids',0):,} repeated ID value(s) were detected. Confirm whether IDs should be unique before downstream joins."})
    if report["duplicates"]:
        rec.append({"priority":"High","title":"Investigate duplicate records","body":f"{report['duplicates']:,} duplicate row(s) were detected. Confirm whether they are true duplicates before removing them from production data."})
    if report["invalid"]:
        rec.append({"priority":"High","title":"Validate invalid values","body":f"{report['invalid']:,} invalid or rule-breaking value(s) were detected, including type/percentage/date checks where applicable."})
    if report["outliers"]:
        rec.append({"priority":"Medium","title":"Review extreme values","body":f"{report['outliers']:,} potential numeric outliers were detected using IQR. Review whether they are genuine business events before capping/removing them."})
    if report["inconsistencies"]:
        rec.append({"priority":"Medium","title":"Standardize categories","body":f"{report['inconsistencies']:,} case/label variants were detected. Normalizing dimension values can improve grouping and reporting."})
    if report["score"]>=90:
        rec.append({"priority":"Low","title":"Data is dashboard-ready","body":"The current quality score is high. Focus next on trend monitoring, anomaly alerts, and KPI ownership."})
    return rec[:8]
