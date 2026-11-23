import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check(name, ok, detail=""):
    print(f"{'OK  ' if ok else 'FAIL'} {name} {detail}")

# OpenWeather
key = os.getenv("OPENWEATHER_API_KEY")
r = requests.get("https://api.openweathermap.org/data/2.5/weather",
                 params={"q": "Karachi", "appid": key}, timeout=20)
check("OpenWeather", r.status_code == 200, f"(status {r.status_code})")

# AQICN
token = os.getenv("AQICN_TOKEN")
r = requests.get("https://api.waqi.info/feed/karachi/",
                 params={"token": token}, timeout=20)
check("AQICN", r.ok and r.json().get("status") == "ok", f"(status {r.status_code})")

# Open-Meteo (no key needed)
r = requests.get("https://api.open-meteo.com/v1/forecast",
                 params={"latitude": 24.8607, "longitude": 67.0011,
                         "hourly": "uv_index", "forecast_days": 1}, timeout=20)
check("Open-Meteo UV", r.status_code == 200, f"(status {r.status_code})")

# Groq
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    client.models.list()
    check("Groq", True)
except Exception as e:
    check("Groq", False, str(e)[:100])

# Hopsworks
try:
    import hopsworks
    project = hopsworks.login(project=os.getenv("HOPSWORKS_PROJECT"),
                              api_key_value=os.getenv("HOPSWORKS_API_KEY"))
    check("Hopsworks", True, f"(project: {project.name})")
except Exception as e:
    check("Hopsworks", False, str(e)[:100])