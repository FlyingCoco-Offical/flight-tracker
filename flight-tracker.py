import requests
import webbrowser
import folium
from IPython.display import display


def create_map(planes, title="Aircraft Map"):
    if not planes:
        print("No aircraft to display.")
        return

    # Center map on first aircraft
    first = planes[0]
    flight_map = folium.Map(
        location=[first.get("lat"), first.get("lon")],
        zoom_start=7
    )

    for plane in planes:
        lat = plane.get("lat")
        lon = plane.get("lon")

        if lat is None or lon is None:
            continue

        popup = f"""
        Flight: {plane.get('flight', 'Unknown')}<br>
        Registration: {plane.get('r', 'Unknown')}<br>
        Aircraft Type: {plane.get('t', 'Unknown')}<br>
        Altitude: {plane.get('alt_baro', 'Unknown')} ft<br>
        Speed: {plane.get('gs', 'Unknown')} knots
        """

        folium.Marker(
            [lat, lon],
            popup=popup,
            icon=folium.Icon(color="blue", icon="plane")
        ).add_to(flight_map)

    display(flight_map)


print("Welcome to AKM Flight Tracker powered by ADSB.LOL")
print("Select an option to continue:")
print("1. Track a flight by callsign")
print("2. Show all emergency flights")

one_or_two = int(input("Please type a selection from above: "))


if one_or_two == 1:

    callsign = input("Enter a callsign: ").upper()

    url = f"https://api.adsb.lol/v2/callsign/{callsign}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data["ac"]:

            plane = data["ac"][0]

            print("\nFlight:", plane.get("flight"))
            print("Registration:", plane.get("r"))
            print("Aircraft type:", plane.get("t"))
            print("Latitude:", plane.get("lat"))
            print("Longitude:", plane.get("lon"))
            print("Altitude:", plane.get("alt_baro"), "ft")
            print("Speed:", plane.get("gs"))

            print("")
            print("Tracking Link:",
                  f"https://globe.adsb.lol/?icao={plane.get('hex')}")

            openlink = input(
                "Would you like to open the tracking link (y/n): "
            ).lower()

            if openlink == "y":
                webbrowser.open(
                    f"https://globe.adsb.lol/?icao={plane.get('hex')}"
                )

            elif openlink == "n":
                print("--Thank you--")

            # Display map
            create_map([plane])


        else:
            print("Flight not currently tracked")

    else:
        print("API Error:", response.status_code)



elif one_or_two == 2:

    print("\nSquawk Types:")
    print("A) 7500: Active Hijacking")
    print("B) 7600: Communication Failure")
    print("C) 7700: Mechanical/Other Failure")
    print("D) All Emergencies")

    squawk_type = input(
        "Which squawk would you like to track: "
    ).lower()


    if squawk_type == "a":
        codes = ["7500"]

    elif squawk_type == "b":
        codes = ["7600"]

    elif squawk_type == "c":
        codes = ["7700"]

    elif squawk_type == "d":
        codes = ["7500", "7600", "7700"]

    else:
        print("Invalid option")
        codes = []


    emergency_planes = []


    for code in codes:

        url = f"https://api.adsb.lol/v2/squawk/{code}"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            print(f"\nSquawk {code}:")
            print(f"Aircraft found: {data['total']}")

            for plane in data["ac"]:

                emergency_planes.append(plane)

                print(
                    "Flight:", plane.get("flight", "Unknown"),
                    "Registration:", plane.get("r", "Unknown"),
                    "Type:", plane.get("t", "Unknown"),
                    "Lat:", plane.get("lat"),
                    "Lon:", plane.get("lon")
                )

        else:
            print("API Error:", response.status_code)


    # Show all emergency aircraft on one map
    create_map(emergency_planes)
