from __future__ import annotations
import pandas as pd
import numpy as np


def _find(df, hints):
    for c in df.columns:
        if any(h in str(c).lower() for h in hints): return c
    return None


def deterministic_insights(df: pd.DataFrame, profile: dict) -> list[dict]:
    out=[]
    revenue=_find(df,["revenue","sales","amount","gmv"])
    profit=_find(df,["profit","income","earnings"])
    date=next((c for c,m in profile.items() if m["type"]=="Date"),None)
    cats=[c for c,m in profile.items() if m["type"] in {"Categorical","Geographic"}]
    if revenue:
        s=pd.to_numeric(df[revenue],errors="coerce")
        out.append({"title":"Revenue concentration","body":f"{revenue} totals {s.sum():,.0f} across {s.notna().sum():,} populated records.","priority":"info"})
        if cats:
            g=df.assign(_v=s).groupby(cats[0],dropna=False)['_v'].sum().sort_values(ascending=False)
            if not g.empty:
                share=(g.iloc[0]/g.sum()*100) if g.sum() else 0
                out.append({"title":f"Top {cats[0]}","body":f"{g.index[0]} leads with {g.iloc[0]:,.0f} ({share:.1f}% of total).","priority":"high"})
    if profit and revenue:
        rv=pd.to_numeric(df[revenue],errors="coerce").sum(); pv=pd.to_numeric(df[profit],errors="coerce").sum()
        if rv: out.append({"title":"Profitability","body":f"Overall profit margin is {(pv/rv*100):.1f}% based on the available revenue and profit columns.","priority":"medium" if pv>=0 else "critical"})
    if date and revenue:
        tmp=df[[date,revenue]].copy(); tmp[date]=pd.to_datetime(tmp[date],errors="coerce"); tmp[revenue]=pd.to_numeric(tmp[revenue],errors="coerce"); tmp=tmp.dropna()
        if len(tmp)>=6:
            monthly=tmp.groupby(pd.Grouper(key=date,freq="ME"))[revenue].sum().dropna()
            if len(monthly)>=4:
                change=(monthly.iloc[-1]-monthly.iloc[-2])/abs(monthly.iloc[-2])*100 if monthly.iloc[-2]!=0 else 0
                direction="increased" if change>=0 else "declined"
                out.append({"title":"Latest trend","body":f"{revenue} {direction} {abs(change):.1f}% versus the previous month in the current dataset.","priority":"high" if abs(change)>=15 else "info"})
    nums=[c for c,m in profile.items() if m["type"] in {"Numeric","Currency","Percentage"}]
    if len(nums)>=2:
        corr=df[nums].apply(pd.to_numeric,errors="coerce").corr().stack().dropna()
        corr=corr[corr<0.999]
        if not corr.empty:
            pair=corr.abs().sort_values(ascending=False).index[0]
            val=corr.loc[pair]
            out.append({"title":"Strong relationship","body":f"{pair[0]} and {pair[1]} have a correlation of {val:.2f}. Correlation is not proof of causation.","priority":"info"})
    return out[:6]


def ai_insights(df: pd.DataFrame, profile: dict) -> list[str]:
    """Optional OpenAI enhancement. Falls back to deterministic insights outside this function."""
    import os
    api_key=os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key: return []
    try:
        from openai import OpenAI
        client=OpenAI(api_key=api_key)
        sample=df.head(50).to_csv(index=False)
        prompt=("Analyze this dataset sample. Return 3 concise business insights. Only state facts that can be directly supported by the provided data. "
                "If a claim cannot be supported, omit it. No markdown headings.\n\n" + sample[:12000])
        response=client.responses.create(model=os.getenv("OPENAI_MODEL","gpt-4.1-mini"), input=prompt)
        text=getattr(response,"output_text","")
        return [line.strip("- ").strip() for line in text.splitlines() if line.strip()][:3]
    except Exception:
        return []
