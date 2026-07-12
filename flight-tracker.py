import time

current_time = time.localtime()
print(current_time)

from opensky_api import OpenSkyApi, TokenManager

tm = TokenManager.from_json_file("credentials.json")

with OpenSkyApi(token_manager=tm) as api:
    states = api.get_states()

    print(f"Found {len(states.states)} aircraft")

    for aircraft in states.states[:10]:
        print(aircraft.callsign)