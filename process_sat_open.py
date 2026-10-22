import os
import io
import requests
from PIL import Image

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_wms_satellite(bbox, width, height, layer, filename):
    wms_base_url = "https://view.eumetsat.int/geoserver/wms"
    params = {
        'service': 'WMS',
        'version': '1.3.0',
        'request': 'GetMap',
        'layers': layer,
        'styles': '',
        'crs': 'EPSG:4326',
        'bbox': f"{bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]}",
        'width': str(width),
        'height': str(height),
        'format': 'image/png',
        'transparent': 'true'
    }
    headers = {'User-Agent': 'Mozilla/5.0 NowcastingItalia/1.0'}
    
    print(f"Richiesta layer: {layer}...")
    response = requests.get(wms_base_url, params=params, headers=headers, timeout=30)
    
    print(f"Status Code ricevuto: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")

    if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
        image = Image.open(io.BytesIO(response.content))
        filepath = os.path.join(OUTPUT_DIR, filename)
        image.save(filepath, 'PNG')
        print(f"SUCCESSO: Salvato {filepath}")
    else:
        print(f"ERRORE DAL SERVER: {response.text[:300]}");

if __name__ == "__main__":
    EUROPE_BBOX = [-25.0, 30.0, 45.0, 70.0]
    ITALY_BBOX = [5.0, 35.0, 20.0, 48.0]
    
    # Testiamo prima con un singolo layer per vedere l'output esatto nei log
    fetch_wms_satellite(ITALY_BBOX, 800, 600, "msg_rgb:convection", "italy_convection.png")
  
