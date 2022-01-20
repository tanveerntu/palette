from matplotlib import pyplot as plt
from skimage import io, color
from skimage.transform import rescale, resize, downscale_local_mean
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from matplotlib.colors import to_hex

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Color Palette Generator")
st.header("Load any Image to Generate its Color Palette")
st.write("Palette Generation may take a few seconds after loading the image")
number = st.slider('Max. Number of shades in the Palette', 0, 20, 5)

uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
if uploaded_file is not None:
    image = io.imread(uploaded_file)
    st.image(image)

    img = resize(image, (200, 200))
    #st.image(img)
    data = pd.DataFrame(img.reshape(-1, 3),
                    columns=['R', 'G', 'B'])

    kmeans = KMeans(n_clusters=number,
                random_state=0)
    # Fit and assign clusters
    data['Cluster'] = kmeans.fit_predict(data)
    palette = kmeans.cluster_centers_

    # Convert data to format accepted by imshow
    palette_list = list()
    for color in palette:
        palette_list.append([[tuple(color)]])

    # Show color palette
    for color in palette_list:
        fig = plt.figure(figsize=(6, 2))
        st.header(to_hex(color[0][0]))
        def display_table(fig, figsize=(5,5)):
            "example of displaying a table in streamlit"
            fig, ax = plt.subplots(figsize=figsize)
            plt.axis('off')
            plt.imshow(color, aspect='auto')
            st.pyplot(fig)

        display_table(fig, figsize=(10,5))
