# Custom Packages
import os
import pandas as pd
import streamlit as st

# List of supported datasets to load
supported = [
    {
        "id": "twcs",
        "name": "twcs (Customer Support on Twitter)",
        "directory": "datasets/twcs",
    },
    {
        "id": "multiwoz",
        "name": "MultiWOZ (Multi-Domain Wizard-of-Oz dataset)",
        "directory": "datasets/MultiWOZ",
    },
    {
        "id": "qrecc",
        "name": "QReCC (Question Rewriting in Conversational Context)",
        "directory": "datasets/ml-qrecc",
    },
]


@st.cache
def list_files(directory):
    files = []

    for (dirpath, _, filenames) in os.walk(directory):
        for filename in filenames:
            if ".json" in filename or ".csv" in filename:
                files.append(os.path.join(dirpath, filename))

    return files


@st.cache
def load_files(selected_files):
    data = []
    for filepath in selected_files:
        df = load(filepath)
        if df is not None:
            data.append({"name": os.path.basename(filepath), "df": df})

    return data


@st.cache
def load(filepath):
    filename = os.path.basename(filepath)
    df = None

    if ".json" in filename:
        df = pd.read_json(filepath)
    elif ".csv" in filename:
        df = pd.read_csv(filepath)

    return df
