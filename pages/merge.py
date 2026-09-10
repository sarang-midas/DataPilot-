import streamlit as st
from components.ui import section_title
from core.merge_engine import common_keys, merge_frames


def render_merge(datasets):
    section_title("Merge Datasets","Join customers, orders, products or any other uploaded tables with a preview before applying the merge.")
    names=list(datasets.keys())
    if len(names)<2:
        st.info("Upload at least two datasets to use the merge workspace.")
        return
    left_name=st.selectbox("Left dataset",names,index=0); right_name=st.selectbox("Right dataset",names,index=1)
    left,right=datasets[left_name],datasets[right_name]
    keys=common_keys(left,right)
    left_col=st.selectbox("Left join key",list(left.columns),index=list(left.columns).index(keys[0]) if keys else 0)
    right_col=st.selectbox("Right join key",list(right.columns),index=list(right.columns).index(keys[0]) if keys else 0)
    how=st.selectbox("Join type",["inner","left","right","outer"])
    if st.button("Preview merge",type="primary"):
        merged=merge_frames(left,right,left_col,right_col,how)
        st.session_state["merge_preview"]=merged
        st.dataframe(merged.head(200),width="stretch",hide_index=True)
        st.download_button("Download merged CSV",merged.to_csv(index=False).encode('utf-8-sig'),"merged_dataset.csv","text/csv",width="stretch")
    else:
        st.caption(f"Suggested common keys: {', '.join(keys[:8]) if keys else 'none detected'}")
