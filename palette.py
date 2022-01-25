from matplotlib import pyplot as plt
from skimage import io, color
from skimage.transform import rescale, resize, downscale_local_mean
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from matplotlib.colors import to_hex
from io import BytesIO

st.set_page_config(
    page_title = 'Color Palette Generator',
    page_icon = '✅',
    layout = 'wide'
)
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

number = st.slider('Max. Number of colors in the Palette', 0, 20, 5)
uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
if uploaded_file is not None:
    image = io.imread(uploaded_file)
    st.image(image)
    with st.spinner("Color Palette is being generated...."):
        img = resize(image, (200, 200))
        #st.write(img.shape)
        #img2 = img.reshape(-1, 3) # to reduce img in two dimensions
        #st.write(img2.shape)
        data = pd.DataFrame(img.reshape(-1, 3),
                        columns=['R', 'G', 'B']) #creating R, G B columns of dataframe named data
        kmeans = KMeans(n_clusters=number,
                    random_state=0)
        # Fit and assign clusters
        data['Cluster'] = kmeans.fit_predict(data) # adding 'Cluster' column in dataframe 'data' 
        palette = kmeans.cluster_centers_ # getting data table reduced to ceteroid clusters



        data1 = (data
            .groupby(['Cluster'])
            .agg({
            'Cluster': ['count'], 
            'R': ['mean'],
            'G': ['mean'],
            'B': ['mean'],
            }))
        #data1 


        def f(x):
            d = {}
            d['Cluster_count'] = x['Cluster'].count()
            d['R_mean'] = x['R'].mean()
            d['G_mean'] = x['G'].mean()
            d['B_mean'] = x['B'].mean()

            return pd.Series(d, index=['Cluster_count', 'R_mean', 'G_mean', 'B_mean'])

        data2 = data.groupby('Cluster').apply(f)
        data2 = data2.sort_values(["Cluster_count"], ascending=False)
        #data2
        data2["R_mean"] = 255 * data2["R_mean"]
        data2["G_mean"] = 255 * data2["G_mean"]
        data2["B_mean"] = 255 * data2["B_mean"]
        data2 = data2.astype({"R_mean": int})
        data2 = data2.astype({"G_mean": int})
        data2 = data2.astype({"B_mean": int})


        #data2
        z = zip(data2['R_mean'], data2['B_mean'], data2['G_mean'])
        data2["Hex"] = [f'#{R_mean:02X}{B_mean:02X}{G_mean:02X}' for R_mean, G_mean, B_mean in z]

        #data2["Hex"] = data2.apply(f'#{R_mean:02X}{G_mean:02X}{B_mean:02X}' for R_mean, G_mean, B_mean in z)
        #data2
        fig4 = plt.figure(figsize=(3, 3))

        plt.pie(data2["Cluster_count"], labels = data2["Hex"], colors=data2["Hex"], autopct='%1.1f%%')
        plt.show()
        st.pyplot(fig4)

        #st.write(palette) #write data table generated after taking kmeans of clusters

        # Convert data to format accepted by imshow
        palette_list = list()
        for color in palette:
            palette_list.append([[tuple(color)]])

        #st.write(color)
        # Show color palette
        for color in palette_list:
            fig = plt.figure(figsize=(6, 2))
            st.header(to_hex(color[0][0])) # to print color hex numbers


            def display_table(fig, figsize=(5,5)):
                "example of displaying a table in streamlit"
                fig, ax = plt.subplots(figsize=figsize)
                plt.axis('off')
                plt.imshow(color, aspect='auto')
                st.pyplot(fig)

            display_table(fig, figsize=(10,3))



            ###########



