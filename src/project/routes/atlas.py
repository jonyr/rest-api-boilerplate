import googlemaps
from flask import Blueprint, request, render_template

atlas_bp = Blueprint("atlas", __name__, template_folder="templates")


@atlas_bp.get("/atlas/geocoder")
def geocoder():
    address = request.args.get("address")
    gmaps = googlemaps.Client(key="AIzaSyD4MgH003Spb_1GTTTgg-J3fFsYWUkhI-o")
    # Geocoding an address
    # geocode_result = gmaps.geocode(address)

    place_id = "EkVDYWxsZSAxNCA2OTgsIEIxOTAwRFZEIExhIFBsYXRhLCBQcm92aW5jaWEgZGUgQnVlbm9zIEFpcmVzLCBBcmdlbnRpbmEiMRIvChQKEgm1tgE5M-ailRF1DcyH1tWr3BC6BSoUChIJ0xlWLi_mopUR9gNmAVlXRtg"

    geocode_result = gmaps.place(place_id)
    print(geocode_result)
    return {"status": True}, 200


@atlas_bp.get("/atlas/places")
def places():
    return render_template("places.html")
