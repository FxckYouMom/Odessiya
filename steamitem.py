import requests

def DATASTICKER(data):
    urldota = f"https://steamcommunity.com/inventory/{data}/570/2?l=ukrainian&count=75"
    urltf = f"https://steamcommunity.com/inventory/{data}/440/2?l=ukrainian&count=75"

    try:
        resdota = requests.get(url=urldota).json()
        restf = requests.get(url=urltf).json()
        
        # Check for Dota assets
        dota_assets = resdota.get('assets', [])
        total_dota_amount = sum(int(asset['amount']) for asset in dota_assets) if dota_assets else 0

        # Check for TF2 assets
        tf_assets = restf.get('assets', [])
        total_tf_amount = sum(int(asset['amount']) for asset in tf_assets) if tf_assets else 0
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

    dota = f"Dota: {total_dota_amount}"
    tf = f"TF2: {total_tf_amount}"
    return f"{dota}\n{tf}"

