import io
from typing import List, Set, Tuple

import pandas as pd
import streamlit as st


# -----------------------------
# Callbacks for Clearing State
# -----------------------------
def clear_a():
    st.session_state.text_a = ""

def clear_b():
    st.session_state.text_b = ""

def clear_all():
    st.session_state.text_a = ""
    st.session_state.text_b = ""


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
    """
    Parses the raw text into a cleaned list and a normalized set.
    """
    text = text or ""

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


def build_norm_map(original_list: List[str], case_sensitive: bool):
    """
    Builds a mapping from normalized value -> first-seen original value.
    """
    norm_list = original_list if case_sensitive else [x.casefold() for x in original_list]
    mapping = {}
    for raw, norm in zip(original_list, norm_list):
        mapping.setdefault(norm, raw)
    return mapping


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
# App Config
# -----------------------------
st.set_page_config(
    page_title="List Comparator Pro",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Compare Two Lists")

# Initialize session state keys
if "text_a" not in st.session_state:
    st.session_state.text_a = ""
if "text_b" not in st.session_state:
    st.session_state.text_b = ""


# -----------------------------
# Sidebar Settings
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    label_a = st.text_input("Label for List A", "List A")
    label_b = st.text_input("Label for List B", "List B")

    st.divider()

    delim_mode = st.selectbox(
        "Delimiter",
        ["auto", "newline", "comma", "semicolon", "whitespace", "custom"]
    )

    custom_delim = st.text_input("Custom delimiter") if delim_mode == "custom" else ""

    case_sensitive = st.checkbox("Case sensitive comparison", False)
    strip_items = st.checkbox("Trim whitespace", True)
    deduplicate = st.checkbox("Deduplicate results", True)
    sort_results = st.checkbox("Sort output alphabetically", False)

    st.divider()
    
    # Clear both button using callback
    st.button("🧹 Clear Both Lists", on_click=clear_all, use_container_width=True)


# -----------------------------
# Input Section
# -----------------------------
st.markdown("### 📥 Input Your Lists")

colA, colB = st.columns(2)

with colA:
    # Key links the widget directly to st.session_state.text_a
    st.text_area(
        label=f"{label_a} items",
        key="text_a",
        height=250,
        placeholder="Paste items here...",
    )
    st.button(f"Clear {label_a}", on_click=clear_a, use_container_width=True)

with colB:
    st.text_area(
        label=f"{label_b} items",
        key="text_b",
        height=250,
        placeholder="Paste items here...",
    )
    st.button(f"Clear {label_b}", on_click=clear_b, use_container_width=True)


# -----------------------------
# Processing logic
# -----------------------------
# We pull values directly from session state
listA_raw, setA_norm = parse_list(
    st.session_state.text_a, delim_mode, custom_delim, case_sensitive, strip_items
)

listB_raw, setB_norm = parse_list(
    st.session_state.text_b, delim_mode, custom_delim, case_sensitive, strip_items
)

norm_map_A = build_norm_map(listA_raw, case_sensitive)
norm_map_B = build_norm_map(listB_raw, case_sensitive)

# Set Operations
inter_norm = setA_norm & setB_norm
A_only_norm = setA_norm - setB_norm
B_only_norm = setB_norm - setA_norm

A_only = [norm_map_A[n] for n in A_only_norm]
B_only = [norm_map_B[n] for n in B_only_norm]
intersect = [norm_map_A[n] for n in inter_norm]

if deduplicate:
    A_only = list(dict.fromkeys(A_only))
    B_only = list(dict.fromkeys(B_only))
    intersect = list(dict.fromkeys(intersect))

if sort_results:
    A_only.sort()
    B_only.sort()
    intersect.sort()


# -----------------------------
# Results Section
# -----------------------------
st.divider()
st.markdown("### 📊 Summary")

m1, m2, m3 = st.columns(3)
m1.metric(f"{label_a} only", len(A_only_norm))
m2.metric("Common Items", len(inter_norm))
m3.metric(f"{label_b} only", len(B_only_norm))

# Similarity Scores
union_norm = setA_norm | setB_norm
jaccard = len(inter_norm) / len(union_norm) if union_norm else 0.0
overlap_coeff = (
    len(inter_norm) / min(len(setA_norm), len(setB_norm))
    if min(len(setA_norm), len(setB_norm)) > 0 else 0.0
)

st.info(f"**Jaccard Similarity:** {jaccard:.1%} | **Overlap Coefficient:** {overlap_coeff:.3f}")


# -----------------------------
# Explorer Section
# -----------------------------
st.markdown("### 🔍 Explorer")

region = st.radio(
    "Choose data to view:",
    (f"{label_a} only", "Intersection", f"{label_b} only"),
    horizontal=True
)

if region == f"{label_a} only":
    selected_items = A_only
elif region == "Intersection":
    selected_items = intersect
else:
    selected_items = B_only

if selected_items:
    df = pd.DataFrame({"Item": selected_items})
    st.dataframe(df, use_container_width=True, hide_index=True)

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        make_download(region.replace(" ", "_"), selected_items)
    with d_col2:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            csv_data,
            f"{region.replace(' ', '_')}.csv",
            "text/csv",
            use_container_width=True
        )
else:
    st.write("No items found in this category.")