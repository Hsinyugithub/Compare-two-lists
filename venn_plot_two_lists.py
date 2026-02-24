import io
from typing import List, Set, Tuple

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2


# -----------------------------
# Utilities
# -----------------------------
def parse_list(
    text: str,
    delim_mode: str,
    custom_delim: str,
    case_sensitive: bool,
    strip_items: bool,
) -> Tuple[List[str], Set[str]]:

    text = text or ""

    # Choose splitting strategy
    if delim_mode == "newline":
        parts = text.splitlines()
    elif delim_mode == "comma":
        parts = text.split(",")
    elif delim_mode == "semicolon":
        parts = text.split(";")
    elif delim_mode == "whitespace":
        parts = text.split()
    elif delim_mode == "custom":
        parts = text.split(custom_delim) if custom_delim else [text]
    else:  # auto
        parts = text.splitlines()
        if len(parts) <= 1:
            parts = text.split(",")

    cleaned = []
    for p in parts:
        item = p.strip() if strip_items else p
        if item:
            cleaned.append(item)

    norm = cleaned if case_sensitive else [c.casefold() for c in cleaned]
    return cleaned, set(norm)


def normalize_list(lst: List[str], case_sensitive: bool):
    return lst if case_sensitive else [x.casefold() for x in lst]


def recover_items(original_list: List[str], normalized_set: Set[str], case_sensitive: bool):
    norm_list = normalize_list(original_list, case_sensitive)
    result, seen = [], set()

    for raw, norm in zip(original_list, norm_list):
        if norm in normalized_set and norm not in seen:
            result.append(raw)
            seen.add(norm)

    return result


def make_download(name: str, items: List[str]):
    buf = io.StringIO()
    buf.write("\n".join(items))

    st.download_button(
        label=f"Download {name} (TXT)",
        data=buf.getvalue(),
        file_name=f"{name}.txt",
        mime="text/plain",
        use_container_width=True
    )


# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(
    page_title="List Comparator",
    page_icon="🔍",
    layout="centered"
)

st.title("Compare Two Lists with a Venn Diagram")

# -----------------------------
# Sidebar Settings
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    label_a = st.text_input("Label for List A", "List A")
    label_b = st.text_input("Label for List B", "List B")

    delim_mode = st.selectbox(
        "Delimiter",
        ["auto", "newline", "comma", "semicolon", "whitespace", "custom"]
    )

    custom_delim = st.text_input("Custom delimiter") if delim_mode == "custom" else ""

    case_sensitive = st.checkbox("Case sensitive comparison", False)
    strip_items = st.checkbox("Trim whitespace", True)
    deduplicate = st.checkbox("Deduplicate results", True)


# -----------------------------
# Input Area
# -----------------------------
st.markdown("### Input Your Lists")

colA, colB = st.columns(2)

with colA:
    text_a = st.text_area(f"{label_a} items", height=250)

with colB:
    text_b = st.text_area(f"{label_b} items", height=250)


# -----------------------------
# Parse Lists
# -----------------------------
listA_raw, setA_norm = parse_list(
    text_a, delim_mode, custom_delim,
    case_sensitive, strip_items
)

listB_raw, setB_norm = parse_list(
    text_b, delim_mode, custom_delim,
    case_sensitive, strip_items
)

# -----------------------------
# Set Operations (efficient)
# -----------------------------
inter_norm = setA_norm & setB_norm
A_only_norm = setA_norm - setB_norm
B_only_norm = setB_norm - setA_norm

# Recover user-facing lists
A_only = recover_items(listA_raw, A_only_norm, case_sensitive)
B_only = recover_items(listB_raw, B_only_norm, case_sensitive)
intersect = recover_items(listA_raw, inter_norm, case_sensitive)

# Deduplicate display lists if requested
if deduplicate:
    A_only = list(dict.fromkeys(A_only))
    B_only = list(dict.fromkeys(B_only))
    intersect = list(dict.fromkeys(intersect))


# -----------------------------
# Summary Metrics
# -----------------------------
st.markdown("### 📊 Summary")

col1, col2, col3 = st.columns(3)
col1.metric(f"{label_a} only", len(A_only))
col2.metric("Intersection", len(intersect))
col3.metric(f"{label_b} only", len(B_only))


# -----------------------------
# Similarity Score
# -----------------------------
union_size = len(setA_norm | setB_norm)
jaccard = len(inter_norm) / union_size if union_size > 0 else 0

st.markdown(f"**Jaccard Similarity:** {jaccard:.3f}")


# -----------------------------
# Venn Diagram
# -----------------------------
st.markdown("### 🟣 Venn Diagram")

fig, ax = plt.subplots()

venn2(
    subsets=(len(A_only), len(B_only), len(intersect)),
    set_labels=(label_a, label_b),
    ax=ax
)

st.pyplot(fig)


# -----------------------------
# Interactive Region Selection
# -----------------------------
st.markdown("### 🔍 Explore Region")

region = st.radio(
    "Select region to inspect:",
    (
        f"{label_a} only",
        "Intersection",
        f"{label_b} only"
    ),
    horizontal=True
)

if region == f"{label_a} only":
    selected_items = A_only
elif region == "Intersection":
    selected_items = intersect
else:
    selected_items = B_only


# -----------------------------
# Display Table
# -----------------------------
st.markdown(f"### 📄 Items in: {region}")

if selected_items:
    df = pd.DataFrame({"Item": selected_items})
    st.dataframe(df, use_container_width=True)

    make_download(region.replace(" ", "_"), selected_items)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name=f"{region.replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.info("No items in this category.")