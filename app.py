from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time
import itertools

app = FastAPI()


# The cycle alternates between two groups for 5 seconds each:
# group A values = [100, 101, 102]
# group B values = [300, 301, 302]
# We'll compute which group is active based on the current time.


def current_group_values():
    # cycle_period is 10 seconds: 5s group A, 5s group B
    now = int(time.time())
    period = (now // 5) % 2  # 0 => group A, 1 => group B
    if period == 0:
        return [100.0, 101.0, 102.0]
    else:
        return [300.0, 301.0, 302.0]


def make_payload():
    vals = current_group_values()
    # produce three motes with the values and current timestamps in ms
    ts = int(time.time() * 1000)
    data = []
    motes = ["9.138", "32.131", "53.105"]
    for mote, v in zip(motes, vals):
        data.append({"timestamp": ts, "label": "light1", "value": v, "mote": mote})
    return {"data": data}


@app.get("/AMIO-API")
def read_amio_api():
    """Return a cyclic JSON payload: 5s of [100,101,102], then 5s of [300,301,302], ..."""
    return JSONResponse(content=make_payload())
