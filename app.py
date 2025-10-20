from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time
import random

app = FastAPI()


# Natural light cycle based on the provided image:
# - Ambient light (10 seconds): values around 153-225 with natural variance
# - Light ON (5 seconds): values around 275-310 with natural variance
# Total cycle period: 15 seconds

# Base values for each mote during ambient and light-on phases
# From image: mote 153.111 (blue) ~195, mote 81.77 (black) ~215, mote 9.138 (yellow-green) ~205 during ambient
#             mote 153.111 ~305, mote 81.77 ~275, mote 9.138 ~285 during light-on

AMBIENT_BASES = {
    "9.138": 205.0,      # yellow-green line
    "32.131": 215.0,     # middle line (black in image)
    "53.105": 195.0      # blue line
}

LIGHT_ON_BASES = {
    "9.138": 285.0,
    "32.131": 275.0,
    "53.105": 305.0
}


def current_light_state():
    """
    Returns the current light state based on a 15-second cycle:
    - 0-10s: ambient light
    - 10-15s: light ON
    """
    now = int(time.time())
    position_in_cycle = now % 15  # 15-second cycle
    
    if position_in_cycle < 10:
        return "ambient"
    else:
        return "light_on"


def get_natural_value(base_value, variance=5.0):
    """Add natural variance to simulate real sensor readings."""
    return round(base_value + random.uniform(-variance, variance), 2)


def make_payload():
    state = current_light_state()
    ts = int(time.time() * 1000)
    data = []
    motes = ["9.138", "32.131", "53.105"]
    
    for mote in motes:
        if state == "ambient":
            base = AMBIENT_BASES[mote]
            value = get_natural_value(base, variance=5.0)
        else:  # light_on
            base = LIGHT_ON_BASES[mote]
            value = get_natural_value(base, variance=4.0)
        
        data.append({
            "timestamp": ts,
            "label": "light1",
            "value": value,
            "mote": mote
        })
    
    return {"data": data}

@app.get("/AMIO-API")
def read_amio_api():
    """Return a natural cyclic JSON payload: 10s ambient light (~150-225), then 5s light ON (~275-310)."""
    return JSONResponse(content=make_payload())
