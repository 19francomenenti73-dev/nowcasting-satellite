import os
import io
import requests
from PIL import Image

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_wms_satellite(min_lat, min_lon, max_lat, max_lon, width, height, layer, filename):
    wms_base_url = "https://view.eumetsat.int/geoserver/wms"
    
    # In WMS 1.3.0 con EPSG:4326 l'ordine del BBOX deve essere: minLat, minLon, maxLat, maxLon
    bbox_str = f"{min_lat},{min_lon},{max_lat},{max_lon}"
    
    params = {
        'service': 'WMS',
        'version': '1.3.0',
        'request': 'GetMap',
        'layers': layer,
        'styles': '',
        'crs': 'EPSG:4326',
        'bbox': bbox_str,
        'width': str(width),
        'height': str(height),
        'format': 'image/png',
        'transparent': 'true'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) NowcastingItalia/1.0'
    }

    try:
        print(f"Scaricamento {layer} per {filename}...")
        response = requests.get(wms_base_url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            image = Image.open(io.BytesIO(response.content))
            filepath = os.path.join(OUTPUT_DIR, filename)
            image.save(filepath, 'PNG')
            print(f"OK -> Salvato {filepath}")
        else:
            print(f"ERRORE {response.status_code} su {layer}: {response.text[:200]}")
    except Exception as e:
        print(f"Eccezione durante il download di {filename}: {e}")

if __name__ == "__main__":
    # --- COORDINATE BOUNDING BOX (min_lat, min_lon, max_lat, max_lon) ---
    # Italia e Mediterraneo Centrale
    IT_MIN_LAT, IT_MIN_LON, IT_MAX_LAT, IT_MAX_LON = 35.0, 5.0, 48.0, 20.0
    
    # Europa
    EU_MIN_LAT, EU_MIN_LON, EU_MAX_LAT, EU_MAX_LON = 30.0, -25.0, 70.0, 45.0

    # --- LAYER EUMETVIEW VALIDI ---
    LAYER_CONVECTION = "msg_rgb:convection"
    LAYER_IR = "msg_surface:seviri_colormapped_brightness_temperature_108"

    # 1. Italia (Zoom alta risoluzione)
    fetch_wms_satellite(IT_MIN_LAT, IT_MIN_LON, IT_MAX_LAT, IT_MAX_LON, 1200, 1000, LAYER_CONVECTION, "italy_convection.png")
    fetch_wms_satellite(IT_MIN_LAT, IT_MIN_LON, IT_MAX_LAT, IT_MAX_LON, 1200, 1000, LAYER_IR, "italy_ir.png")

    # 2. Europa
    fetch_wms_satellite(EU_MIN_LAT, EU_MIN_LON, EU_MAX_LAT, EU_MAX_LON, 1920, 1080, LAYER_CONVECTION, "europe_convection.png")
    fetch_wms_satellite(EU_MIN_LAT, EU_MIN_LON, EU_MAX_LAT, EU_MAX_LON, 1920, 1080, LAYER_IR, "europe_ir.png")
    
