# coding: utf-8
# # Woehler analyzing streamlit app

import copy
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pylife.materialdata.woehler as woehler
from pylife.materiallaws import WoehlerCurve
import streamlit as st


def make_SN_plot(fig, cycles, wc, name, color="black"):
    fig.add_scatter(
        x=cycles,
        y=wc.basquin_load(cycles),
        mode="lines",
        name=name + " 50%",
        line_color=color,
    )
    fig.add_scatter(
        x=cycles,
        y=wc.basquin_load(cycles, failure_probability=0.1),
        mode="lines",
        name=name + " 10%",
        line_color=color,
        line_dash="dash",
    )
    fig.add_scatter(
        x=cycles,
        y=wc.basquin_load(cycles, failure_probability=0.9),
        mode="lines",
        name=name + " 90%",
        line_color=color,
        line_dash="dash",
    )
    return fig


# %%
st.set_page_config("woehler", page_icon="../icon/pyLife_logo_no_elefant.png")
st.title("Woehler analyzing streamlit app")
st.markdown(
    r"""
    The SN analysis module takes fatigue data, i. e. values of the form `cycles` `load` `fracture` that have been measured by a fatigue testing lab and analyze it to return the parameters of a Wöhler curve. 
    """
)
# %%
# tab_inp, tab_eval = st.tabs(["Input", "Evaluation of Data"])
# In[2]:
with st.sidebar:
    st.header("Input of the SN data")
    target_upload = st.file_uploader("Select the target profile", type="csv")
if target_upload:
    df = pd.read_csv(target_upload, sep=",")
    df.columns = ["load", "cycles", "fracture"]
    fatigue_data = df.fatigue_data
    col_targ_1, col_targ_2 = st.columns(2)
    col_targ_1.dataframe(df)
    fig = px.scatter(
        df, x="cycles", y="load", log_x=True, log_y=True, symbol="fracture"
    )
    col_targ_2.plotly_chart(fig)
    # evaluation
    with st.sidebar:
        eval_methods = st.multiselect(
            "Select the SN evaluation methods", ["Probit", "ML full"]
        )
    probit_result = woehler.Probit(fatigue_data).analyze().rename("Probit")
    maxlike_full_result = woehler.MaxLikeFull(fatigue_data).analyze().rename("ML full")

    results = pd.concat((probit_result, maxlike_full_result), axis=1)
    cycles = np.logspace(np.log10(df.cycles.min()), np.log10(df.cycles.max()), 100)
    with st.sidebar:
        if eval_methods:
            st.dataframe(results[eval_methods])
            st.download_button(
                "download the SN data",
                data=results.to_csv().encode("utf-8"),
                file_name="SN_results.csv",
                mime="text/csv",
            )
            for method, color in zip(eval_methods, ["black", "blue"]):
                wc = results[method].woehler
                fig = make_SN_plot(fig, cycles, wc, method, color=color)
    if eval_methods:
        st.plotly_chart(fig)
