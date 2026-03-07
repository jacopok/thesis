## Jupyter widgets

They are super cool. This, for example, will show the location of Virgo.

```{python}
from ipyleaflet import Map, Marker, basemaps, basemap_to_tiles
m = Map(
  basemap=basemap_to_tiles(
    basemaps.NASAGIBS.ModisTerraTrueColorCR, "2017-04-08"
  ),
  center=(43.631414472222225, 10.504496611111112),
  zoom=4
)
m.add_layer(Marker(location=(43.631414472222225, 10.504496611111112)))
m
```

[Here are some more notes and examples](https://quarto.org/docs/interactive/widgets/jupyter.html).

Links to [event viewer](https://peviewer.igwn.org/?event1=GW150914).

## Topics

