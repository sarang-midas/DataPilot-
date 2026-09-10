import pandas as pd
import streamlit as st

from app import register_uploaded_files


class FakeUpload:
    def __init__(self, name: str, payload: bytes):
        self.name = name
        self._payload = payload
        self.size = len(payload)
        self.file_id = None

    def getvalue(self) -> bytes:
        return self._payload


def test_new_upload_replaces_old_dataset_state():
    st.session_state.clear()
    st.session_state["datasets"] = {
        "old_data": pd.DataFrame({"id": [1], "value": [99]})
    }
    st.session_state["processed_uploads"] = {"old-upload"}

    changed = register_uploaded_files(
        [FakeUpload("new_data.csv", b"customer,amount\nA,10\nB,20\n")]
    )

    assert changed is True
    assert list(st.session_state["datasets"]) == ["new_data"]
    assert st.session_state["active_dataset"] == "new_data"
    assert st.session_state["clean_df"].shape == (2, 2)
