from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import time
import random
import os

app = FastAPI()

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


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
    base_ts = int(time.time() * 1000)
    data = []
    motes = ["9.138", "32.131", "53.105"]
    
    for idx, mote in enumerate(motes):
        if state == "ambient":
            base = AMBIENT_BASES[mote]
            value = get_natural_value(base, variance=5.0)
        else:  # light_on
            base = LIGHT_ON_BASES[mote]
            value = get_natural_value(base, variance=4.0)
        
        # Add slight offset to each mote's timestamp to simulate real sensor arrival times
        ts = base_ts + random.randint(0, 100)  # 0-100ms offset
        
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

@app.get("/AMIO-API/gui")
def gui():
    """Serve the live graph GUI."""
    graph_path = os.path.join(static_dir, "graph.html")
    return FileResponse(graph_path)
