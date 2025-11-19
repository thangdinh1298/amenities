from flask import Flask, render_template, request
import requests

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


def filter_by_radius(amenities, lat, lon, radius_km):
    # No endpoint to fetch all amenities
    pass


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

    return render_template("index.html", amenities=amenities, filter_info=filter_info)


if __name__ == "__main__":
    app.run(debug=True)
