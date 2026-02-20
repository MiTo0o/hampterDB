import streamlit as st
import json
import os
import imagehash
from PIL import Image

st.set_page_config(page_title="Hamster Master Pruner", layout="wide")

# Floating Button CSS remains the same
st.markdown("""
    <style>
    div[data-testid="stFormSubmitButton"] {
        position: fixed; bottom: 2rem; right: 2rem; z-index: 999;
        background-color: white; padding: 10px; border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4); border: 3px solid #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "images"
MANIFEST = "manifest.json"

if not os.path.exists(MANIFEST):
    st.error("Run sync first!")
    st.stop()

with open(MANIFEST, "r") as f:
    photos = json.load(f)

# --- THE IMPROVED BRAIN ---
@st.cache_data
def get_visual_data(file_list):
    h_map = {}
    for f in file_list:
        try:
            with Image.open(os.path.join(IMG_DIR, f)) as img:
                # We use a combination of dhash and ahash
                # aHash is great for catching "shifted" or "compressed" twins
                h_map[f] = {
                    'd': imagehash.dhash(img),
                    'a': imagehash.average_hash(img)
                }
        except: pass
    return h_map

st.sidebar.title("Pruner Controls")
# Threshold 8-10 is usually the "sweet spot" for MS Paint
threshold = st.sidebar.slider("Similarity Sensitivity", 0, 30, 10)

with st.spinner("Analyzing hamsters..."):
    hashes = get_visual_data(photos)

to_delete = []
displayed = set()

with st.form("master_purge_form"):
    st.title("🐹 Hamster Duplicate Hunter")
    
    st.subheader("🔍 Potential Duplicates")
    for i, file_a in enumerate(photos):
        if file_a in displayed: continue
        h_a = hashes.get(file_a)
        cluster = [file_a]
        
        for file_b in photos[i+1:]:
            if file_b in displayed: continue
            h_b = hashes.get(file_b)
            
            if h_a and h_b:
                # If BOTH the structure (d) and average color (a) are close, it's a dupe
                d_diff = h_a['d'] - h_b['d']
                a_diff = h_a['a'] - h_b['a']
                
                # Using a combined score makes it much harder for "twins" to hide
                if (d_diff + a_diff) <= threshold:
                    cluster.append(file_b)
        
        if len(cluster) > 1:
            with st.container(border=True):
                cols = st.columns(6)
                for idx, img_file in enumerate(cluster):
                    with cols[idx % 6]:
                        st.image(os.path.join(IMG_DIR, img_file), use_container_width=True)
                        if st.checkbox("Delete", key=f"del_{img_file}"):
                            to_delete.append(img_file)
            displayed.update(cluster)

    st.divider()

    # Section 2: All the rest
    st.subheader("🐹 Lone Hamsters (Check these too!)")
    lone_hamsters = [p for p in photos if p not in displayed]
    
    # Simple grid for remaining
    for i in range(0, len(lone_hamsters), 6):
        batch = lone_hamsters[i:i + 6]
        cols = st.columns(6)
        for idx, img_file in enumerate(batch):
            with cols[idx]:
                st.image(os.path.join(IMG_DIR, img_file), use_container_width=True)
                if st.checkbox("Delete", key=f"del_lone_{img_file}"):
                    to_delete.append(img_file)
    
    submit = st.form_submit_button("🔥 PURGE SELECTED")

if submit and to_delete:
    for f in to_delete:
        path = os.path.join(IMG_DIR, f)
        if os.path.exists(path): os.remove(path)
        if f in photos: photos.remove(f)
    with open(MANIFEST, 'w') as f: json.dump(photos, f)
    st.success(f"Deleted {len(to_delete)} items!")
    st.rerun()