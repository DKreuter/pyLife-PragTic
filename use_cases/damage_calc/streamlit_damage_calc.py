# %%
import numpy as np
import pandas as pd
import pylife.strength.fatigue
import plotly.express as px
import streamlit as st

# %%
st.set_page_config("damage", page_icon="../icon/pyLife_logo_no_elefant.png")
st.title("Damage Calculation")
st.markdown(
    r"""
    ## This app shows a general calculation stream for a nominal damage calculation.

    1. Define load cycles
    2. Define the material parameter
    3. Select the damage calculation method (Miner elementary, Miner-Haibach, ...)
    4. Calculate the damage for every load level and the damage sum
"""
)
# %% upload data
load_cycles = pd.DataFrame(
    {
        "amplitude": [100, 50, 75, 25],
        "cycles": [1e3, 5e3, 10e3, 25e3],
    }
)
st.table(load_cycles)
# %%
mat_init = {"k_1": 8.0, "ND": 1e6, "SD": 100.0, "TN": 12.0, "TS": 1.1}
mat_edit = pd.Series(mat_init)

with st.sidebar:
    st.markdown("## Define the material parameter")
    for k, v in mat_init.items():
        mat_edit[k] = st.number_input(k, value=v)
st.write("Defined material parameter")
st.table(mat_edit.to_frame().T)
st.markdown("## Evaluation method")
damage = {
    "miner_original": mat_edit.fatigue.damage(load_cycles),
    "miner_elementary": mat_edit.fatigue.miner_elementary().damage(load_cycles),
    "miner_haibach": mat_edit.fatigue.miner_haibach().damage(load_cycles),
}
methods = st.multiselect(
    "select your method",
    damage.keys(),
)

if st.button("start damage calc"):
    cyc = np.logspace(1, 12, 200)
    fig = px.bar(
        load_cycles, x="cycles", y="amplitude", orientation="h", log_x=True, log_y=True
    )
    for method, k_2 in zip(
        damage.keys(), [-np.inf, mat_edit.k_1, 2 * mat_edit.k_1 - 1]
    ):
        if method in methods:
            mat_act = mat_edit.copy()
            mat_act["k_2"] = k_2
            wc = mat_act.woehler
            sn_df = pd.DataFrame({"cycles": cyc, "amplitude": wc.basquin_load(cyc)})
            fig.add_scatter(x=sn_df.cycles, y=sn_df.amplitude, name=method)
            str_out = "total damage sum " + method + " :  %.2e" % damage[method].sum()
            st.markdown(str_out)
    st.plotly_chart(fig)
