import os
import requests

# Directory di output
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_wms_satellite(bbox, width, height, layer, filename):
    """
    Scarica direttamente dal server OGC WMS aperto di EUMETSAT
    le mappe satellitari IR/RGB georeferenziate.
    """
    wms_base_url = "https://view.eumetsat.int/geoserver/wms"

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
        "transparent": "true"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NowcastingItalia/1.0"
    }

    try:
        print(f"Scarico layer {layer} per {filename}...")
        response = requests.get(wms_base_url, params=params, headers=headers, timeout=30)

        if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"✅ Salvato con successo: {filepath}")
        else:
            print(f"❌ Errore HTTP {response.status_code} dal server WMS")
    except Exception as e:
        print(f"❌ Eccezione durante il download: {e}")

if __name__ == "__main__":
    # Coordinate Bounding Box EPSG:4326 (min_lat, min_lon, max_lat, max_lon)
    ITALY_BBOX = "35.0,5.0,48.0,20.0"      # Italia e Mediterraneo centrale
    EUROPE_BBOX = "30.0,-10.0,65.0,40.0"   # Europa completa

    # Nomi Layer Ufficiali EUMETSAT WMS Open
    LAYER_IR = "msg_fes:ir108"
    LAYER_CONVECTION = "msg_fes:rgb_convective"

    # 1. Elaborazione ITALIA
    fetch_wms_satellite(ITALY_BBOX, 1200, 1000, LAYER_CONVECTION, "italy_convection.png")
    fetch_wms_satellite(ITALY_BBOX, 1200, 1000, LAYER_IR, "italy_ir.png")

    # 2. Elaborazione EUROPA
    fetch_wms_satellite(EUROPE_BBOX, 1200, 1000, LAYER_CONVECTION, "europe_convection.png")
    fetch_wms_satellite(EUROPE_BBOX, 1200, 1000, LAYER_IR, "europe_ir.png")
    
