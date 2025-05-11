import googlemaps

gmaps = googlemaps.Client(key="AIzaSyAUfq-BIYNsNrbUGLvJ7Am4sfRNFcFO73A")

res = gmaps.distance_matrix(
    ["Ho Chi Minh City"],
    ["Tan Son Nhat Airport"],
    mode="driving"
)

print(res)
