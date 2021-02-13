#### Draw your own marker paths

In matplotlib, you can input a M x 2 array of vertices that specify a path as the marker argument for a scatter plot.

This small streamlit app allows you to handdraw markers yourself and save the vertices for use as scatter markers.

starting the app:
```python
streamlit run app.py
```

###### Using the markers

1) Load them
```python
path = np.loadtxt(f'{filename}.gz')
# They are stored in /saved_paths
```

2) Plot
```python
scatter = ax.scatter(x, y, marker=path)
```

3) Enjoy your own markers!
