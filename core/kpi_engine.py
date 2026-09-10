from __future__ import annotations
import math
import pandas as pd

KEYWORDS = {
    "revenue": ["revenue","sales","turnover","gmv","amount"],
    "profit": ["profit","net_income","earnings"],
    "cost": ["cost","expense","spend","expenditure"],
    "quantity": ["quantity","qty","units","volume"],
    "orders": ["order","transaction","invoice","ticket"],
    "customer": ["customer","client","user","member"],
    "employee": ["employee","staff","worker"],
    "salary": ["salary","wage","compensation"],
}


def find_col(df: pd.DataFrame, terms: list[str]) -> str | None:
    for col in df.columns:
        low = str(col).lower()
        if any(term in low for term in terms):
            return str(col)
    return None


def fmt_number(v):
    if v is None or (isinstance(v,float) and math.isnan(v)): return "—"
    x=float(v)
    if abs(x)>=1_000_000_000: return f"{x/1_000_000_000:.1f}B"
    if abs(x)>=1_000_000: return f"{x/1_000_000:.1f}M"
    if abs(x)>=1_000: return f"{x/1_000:.1f}K"
    return f"{x:,.0f}" if float(x).is_integer() else f"{x:,.2f}"


def generate_kpis(df: pd.DataFrame, profile: dict) -> list[dict]:
    kpis=[]
    revenue=find_col(df,KEYWORDS["revenue"]); profit=find_col(df,KEYWORDS["profit"]); cost=find_col(df,KEYWORDS["cost"])
    qty=find_col(df,KEYWORDS["quantity"]); customer=find_col(df,KEYWORDS["customer"]); employee=find_col(df,KEYWORDS["employee"])
    order=find_col(df,KEYWORDS["orders"])
    kpis.append({"label":"Total Records","value":fmt_number(len(df)),"sub":"rows in current filter","raw":len(df)})
    if revenue:
        val=pd.to_numeric(df[revenue], errors="coerce").sum(); kpis.append({"label":revenue.replace('_',' ').title(),"value":fmt_number(val),"sub":"sum","raw":val})
        if order:
            orders=max(1,df[order].nunique(dropna=True)); aov=val/orders; kpis.append({"label":"Average Value / Order","value":fmt_number(aov),"sub":"derived metric","raw":aov})
    elif profit:
        val=pd.to_numeric(df[profit], errors="coerce").sum(); kpis.append({"label":profit.replace('_',' ').title(),"value":fmt_number(val),"sub":"sum","raw":val})
    if profit and revenue:
        rv=pd.to_numeric(df[revenue], errors="coerce").sum(); pv=pd.to_numeric(df[profit], errors="coerce").sum(); margin=(pv/rv*100) if rv else None
        kpis.append({"label":"Profit Margin","value":f"{margin:.1f}%" if margin is not None else "—","sub":"profit / revenue","raw":margin})
    if qty:
        val=pd.to_numeric(df[qty], errors="coerce").sum(); kpis.append({"label":"Units / Quantity","value":fmt_number(val),"sub":"sum","raw":val})
    if customer:
        val=df[customer].nunique(dropna=True); kpis.append({"label":"Unique Customers","value":fmt_number(val),"sub":"distinct IDs/names","raw":val})
    if employee:
        val=df[employee].nunique(dropna=True); kpis.append({"label":"Employees","value":fmt_number(val),"sub":"distinct employees","raw":val})
    if cost and not profit:
        val=pd.to_numeric(df[cost], errors="coerce").sum(); kpis.append({"label":cost.replace('_',' ').title(),"value":fmt_number(val),"sub":"sum","raw":val})
    # Add a useful generic metric when there is room.
    generic=[c for c,m in profile.items() if m["type"] in {"Numeric","Currency","Percentage"}]
    used={x["label"] for x in kpis}
    for col in generic:
        label=col.replace('_',' ').title()
        if label in used or len(kpis)>=6: continue
        val=pd.to_numeric(df[col], errors="coerce").mean()
        kpis.append({"label":f"Avg {label}","value":fmt_number(val),"sub":"average","raw":val})
        break
    return kpis[:6]
