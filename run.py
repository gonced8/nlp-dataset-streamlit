# Standard Packages
import json
import os

# Custom Packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Modules
import dataset

st.title("NLP Dataset Streamlit")

# Select an existing/supported datasets
if dataset.supported[0]["id"] is not None:
    dataset.supported.insert(0, {"id": None, "name": ""})  # add a blank entry

selected_dataset = st.sidebar.selectbox(
    "Choose a file", dataset.supported, format_func=lambda x: x["name"]
)

# Read the dataset as a DataFrame
# Or upload a file
st.sidebar.write("or")

uploaded_file = st.sidebar.file_uploader("Upload a file")

if uploaded_file is not None:
    print(upload_file)

# Load dataset
data = []

if selected_dataset["id"] is not None:
    # List available files
    files = dataset.list_files(selected_dataset["directory"])
    selected_files = st.sidebar.multiselect(
        "Select set",
        files,
        default=None if len(files) > 1 else files[0],
        format_func=os.path.basename,
    )

    data_load_state = st.text("Loading data...")
    data = dataset.load_files(selected_files)
    data_load_state.text("Loading data... done!")

# Options
if data:
    # Raw data
    raw_data = st.sidebar.checkbox("Raw data", value=True)
    if raw_data:
        n_rows = st.sidebar.number_input("# of rows", min_value=1, value=10)

    # Sequence length
    sequence_length = st.sidebar.checkbox("Sequence length", value=True)
    if sequence_length:
        cols = zip(data[0]["df"].columns, data[0]["df"].dtypes)
        cols = [col[0] for col in cols if col[1] is np.dtype("O")]
        sequence_length_columns = st.sidebar.multiselect("Select columns", cols)
        n_bins = st.sidebar.number_input("# bins", min_value=1, value=20)

for entry in data:
    st.header(entry["name"])
    df = entry["df"]

    # Simple stats
    st.write(f"Number of elements: {len(df)}")

    # Display raw data
    if raw_data:
        st.subheader("Raw data")
        st.write(df.sample(min(n_rows, len(df))))

    # Histogram of sequence length
    if sequence_length:
        fig, ax = plt.subplots(1, 1)

        for col in sequence_length_columns:
            ax.hist(
                [
                    len(elem.split() if hasattr(elem, "split") else elem)
                    for elem in df[col]
                ],
                bins=n_bins,
                histtype="bar",
                alpha=0.5,
            )

        ax.set_xlabel("Length")
        ax.set_ylabel("Frequency")
        ax.grid()
        ax.legend(sequence_length_columns)

        st.pyplot(fig)
