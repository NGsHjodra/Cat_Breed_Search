import streamlit as st
from model.func import query, boot

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

boot()

st.title('Cat Breed Search')

title = st.text_input("Cat Breed", "Siamese")

if st.button("Find Image"):
    st.write(f"Finding image for {title}...")
    results = query(title)
    for i, result in enumerate(results):
        st.image(result, caption=f"Result {i+1}")