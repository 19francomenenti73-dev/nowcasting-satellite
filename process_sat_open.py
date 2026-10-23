import os
import requests

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_HISTORY = 6  # Numero di fotogrammi storici da mantenere per l'animazione

def rotate_history(base_name):
    """Sposta i file storici per fare spazio al nuovo fotogramma"""
    for i in range(MAX_HISTORY - 1, 0, -1):
        old_file = os.path.join(OUTPUT_DIR, f"{base_name}_{i}.png")
        new_file = os.path.join(OUTPUT_DIR, f"{base_name}_{i+1}.png")
        if os.path.exists(old_file):
            if os.path.exists(new_file):
                os.remove(new_file)
            os.rename(old_file, new_file)
    
    first_file = os.path.join(OUTPUT_DIR, f"{base_name}_0.png")
    target_file = os.path.join(OUTPUT_DIR, f"{base_name}_1.png")
    if os.path.exists(first_file):
        if os.path.exists(target_file):
            os.remove(target_file)
        os.rename(first_file, target_file)

def fetch_wms_satellite(bbox, width, height, layer, base_name):
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
        print(f"Scarico layer {layer} per {base_name}...")
        response = requests.get(wms_base_url, params=params, headers=headers, timeout=30)

        if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
            # Ruota la cronologia prima di salvare il nuovo
            rotate_history(base_name)
            
            # Salva il nuovo fotogramma come _0 (il più recente) e come file principale statico
            latest_path = os.path.join(OUTPUT_DIR, f"{base_name}_0.png")
            static_path = os.path.join(OUTPUT_DIR, f"{base_name}.png")
            
            with open(latest_path, "wb") as f:
                f.write(response.content)
            
            with open(static_path, "wb") as f:
                f.write(response.content)
                
            print(f"✅ Salvato con successo e storico aggiornato: {base_name}")
        else:
            print(f"❌ Errore HTTP {response.status_code} dal server WMS per {base_name}")
    except Exception as e:
        print(f"❌ Eccezione durante il download di {base_name}: {e}")

if __name__ == "__main__":
    # Bounding Box con proporzioni corrette per evitare distorsioni e mosaici
    ITALY_BBOX = "35.0,6.0,47.0,18.0"      # Rapporto ottimizzato per Italia
    EUROPE_BBOX = "30.0,-10.0,60.0,30.0"   # Rapporto ottimizzato per Europa

    LAYER_IR = "msg_fes:ir108"
    LAYER_CONVECTION = "msg_fes:rgb_convective"

    # Download con risoluzione pulita
    fetch_wms_satellite(ITALY_BBOX, 1000, 1000, LAYER_CONVECTION, "italy_convection")
    fetch_wms_satellite(ITALY_BBOX, 1000, 1000, LAYER_IR, "italy_ir")
    fetch_wms_satellite(EUROPE_BBOX, 1200, 900, LAYER_CONVECTION, "europe_convection")
    fetch_wms_satellite(EUROPE_BBOX, 1200, 900, LAYER_IR, "europe_ir")
    
