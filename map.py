import folium
import pandas as pd

volcanos = pd.read_csv("Volcanoes.txt", sep=',')
lat = list(volcanos["LAT"])
lon = list(volcanos["LON"])
elev = list(volcanos["ELEV"])
name = list(volcanos["NAME"])

html = """Volcano name: 
        <a href "https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
        Height: %s m"""


def color(num):
    if num<1000:
        return "green"
    elif  num < 2000:
        return "orange"
    else:
        return "red"


map = folium.Map(location= (38.58, -99.09), zoom_start= 5, tiles="Mapbox Bright")
fgv= folium.FeatureGroup(name="Volcanos")
for lt,ln,elev,name in zip(lat,lon,elev,name):
    iframe= folium.IFrame(html=html %(name,name, elev), width=200, height=100)
    fgv.add_child(folium.CircleMarker(radius= 6,location=[lt,ln],popup=folium.Popup(iframe),fill_color=color(elev), color='grey', fill_opacity=0.7))

fgp= folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                            style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']<10_000_000
                            else 'yellow' if x['properties']['POP2005']<20_000_000 else 'orange' if x['properties']['POP2005']<100_000_000 else 'red'}))



map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("map.html")

