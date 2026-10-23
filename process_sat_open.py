import os
import requests

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_wms_safe(bbox, width, height, layer, filename):
    wms_url = "https://view.eumetsat.int/geoserver/wms"
    params = {
        "service": "WMS",
        "version": "1.3.0",
        "request": "GetMap",
        "layers": layer,
        "styles": "",
        "crs": "EPSG:4326",
        "bbox": bbox,
        "width": str(width),
        "height": str(height),
        "format": "image/png",
        "transparent": "false"
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        print(f"Scaricamento layer {layer}...")
        res = requests.get(wms_url, params=params, headers=headers, timeout=25)
        if res.status_code == 200 and "image" in res.headers.get("Content-Type", ""):
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(res.content)
            print(f"✅ Salvato: {filepath}")
        else:
            print(f"⚠️ Errore server WMS per {layer}: {res.status_code}")
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")

if __name__ == "__main__":
    # Bounding box stabili e proporzionati per l'Italia e l'Europa
    ITALY_BBOX = "35.0,6.0,47.0,18.0"
    EUROPE_BBOX = "30.0,-10.0,60.0,30.0"

    # Layer EUMETSAT FES stabili e garantiti
    LAYER_IR = "msg_fes:ir108"
    LAYER_WV = "msg_fes:wv062"

    # Download mappe correnti
    fetch_wms_safe(ITALY_BBOX, 1000, 1000, LAYER_IR, "italy_ir.png")
    fetch_wms_safe(ITALY_BBOX, 1000, 1000, LAYER_WV, "italy_wv.png")
    fetch_wms_safe(EUROPE_BBOX, 1200, 900, LAYER_IR, "europe_ir.png")
    fetch_wms_safe(EUROPE_BBOX, 1200, 900, LAYER_WV, "europe_wv.png")
    
