from flask import Flask, render_template, request
import requests
import math

app = Flask(__name__)

def get_property_amenities(prop_id):
    url = f"https://www.microburbs.com.au/report_generator/api/property/amenity"
    params = {'id': prop_id}
    headers = {
        "Authorization": f"Bearer test"
    }
    try:
        res = requests.get(url, timeout=5, params=params, headers=headers)
        if res.status_code == 200:
            return res.json().get("information", {}).get("results", [])
    except:
        pass
    return []


def get_suburb_amenities(suburb):
    url = f"https://www.microburbs.com.au/report_generator/api/suburb/amenity"
    params = {'suburb': suburb}
    headers = {
        "Authorization": f"Bearer test"
    }
    try:
        res = requests.get(url, timeout=5, params=params, headers=headers)
        # print(res.url)
        # print(res.json())
        if res.status_code == 200:
            return res.json().get("results", [])
    except:
        pass
    return []

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth.
    Returns distance in kilometers.
    """
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def filter_by_radius(amenities, lat, lon, radius_km):
    # No endpoint to fetch all amenities
    try:
        filtered = []
        for amenity in amenities:
            distance = haversine(lat, lon, float(amenity["lat"]), float(amenity["lon"]))
            print('dist in km', distance)
            if distance <= radius_km:
                filtered.append(amenity)
        return filtered
    except:
        pass
    return amenities

# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    amenities = []
    filter_info = {}

    if request.method == "POST":
        filter_type = request.form.get("filter_type")

        if filter_type == "prop_id":
            prop_id = (request.form.get("prop_id") or "").strip()
            if prop_id:
                amenities = get_property_amenities(prop_id)
                filter_info = {"filter": "Property ID", "value": prop_id}

        elif filter_type == "suburb":
            suburb = (request.form.get("suburb") or "").strip()
            if suburb:
                amenities = get_suburb_amenities(suburb)
                filter_info = {"filter": "Suburb", "value": suburb}

        if amenities:
            # Optional location filter
            print('Here')
            lat = request.form.get("lat", "").strip()
            lon = request.form.get("lon", "").strip()
            radius = request.form.get("radius", "").strip()
            print('lat', lat)
            print('lon', lon)
            print('radius', radius)
            print(request.form)

            if lat and lon and radius:
                amenities = filter_by_radius(amenities, lat, lon, radius)
                print('Filtered', amenities)

    return render_template("index.html", amenities=amenities, filter_info=filter_info)


if __name__ == "__main__":
    app.run(debug=True)
