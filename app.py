import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import matplotlib.pyplot as plt

update = st.button('Save')

st.text('1) Draw your markers')

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=3,
    stroke_color="k",
    background_color="#eee",
    update_streamlit=update,
    height=150,
    drawing_mode="freedraw",
    key="canvas",
)
name_input = st.text_area('2) Name your markers seperated by a comma')

st.text('3) Save your markers by Clicking Save Above')


# Process the drawn data
if canvas_result.json_data is not None:
    marker_paths = []
    marker_names = name_input.split(',')
    for d, name in zip(canvas_result.json_data["objects"], marker_names):
        path = d["path"]
        codes = [p[0] for p in path]
        vertices = np.array([p[-2:] for p in path])
        #normed = (vertices - vertices.mean(0)) / vertices.max(0)
        pt_ranges = vertices.max(0) - vertices.min(0)
        normed = (vertices - vertices.min(0) - 0.5*pt_ranges) / pt_ranges
        # flip vertically
        normed[:, 1] = normed[:, 1] * -1

        marker_paths.append(normed)
        np.savetxt(f'saved_paths/{name}.gz', normed)


# Example Plots of the drawn markers
if canvas_result.image_data is not None:
    n_markers = len(name_input.split(','))

    np.random.seed(442)
    _x = np.random.uniform(0,1,50)
    _y = np.random.uniform(0,1,50)

    fig, ax = plt.subplots(1, n_markers, figsize=(n_markers*4, 4))

    for ax_, path, marker_name in zip(ax, marker_paths, marker_names):
        ax_.set_facecolor('#eee')
        scatter = ax_.scatter(_x, _y, fc=fig.get_facecolor(), ec='C0', lw = 1,
                     marker=path,
                     s=50, zorder=999)
        ax_.set_title(marker_name)

    st.pyplot(fig)
