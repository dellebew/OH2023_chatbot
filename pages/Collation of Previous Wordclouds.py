import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random as rand
import os
from PIL import Image


if st.session_state.api_key:
    col1, col2 = st.columns(2)  # 2 columns layout
    #  for display all previous wordclouds; draft
    all_clouds = []
    all_texts = []
    for files in os.listdir("clouds"):
        print(files)
        all_clouds.append("clouds/"+files)
    for f in os.listdir("texts"):
        # print(f)
        all_texts.append("texts/"+f)

    # zip for reference and clarity
    cloudAtexts = zip(all_clouds, all_texts)

    helper = list(cloudAtexts)
    with col1:
        for i in range(0, len(helper), 2):
            st.image(helper[i][0], width=500)
            with st.expander("See Poem"):
                poem = open(helper[i][1], "r")
                st.write(poem.read())
    with col2:
        for i in range(1, len(helper), 2):
            st.image(helper[i][0], width=500)
            with st.expander("See Poem"):
                poem = open(helper[i][1], "r")
                st.write(poem.read())
