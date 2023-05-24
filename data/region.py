try:
    from sys import path
    path.append("..\\Expense Manager")

    import json
    import os.path
    import requests
    import data.info as info
except Exception:
    raise Exception("0xegbl0001")

def _check_region_file_path() -> bool:
    if not os.path.exists(info.DATA_REGION):
        if not os.path.exists(info.DATA_PATH):
            raise Exception()
        else:
            return False
        
    return True

def get_regions() -> list[str]:
    if _check_region_file_path():
        try:
            with open(info.DATA_REGION, 'r') as file:
                regions: list = list(json.loads(file.read()).values())

            if regions.__class__ != list:
                raise Exception
            
            return regions
        except Exception:
            raise Exception()

    URL = "https://countrylist.jquery.app/data/en_GB/country.json"
    
    try:
        regions: dict = requests.get(URL).json()
    except :
        raise Exception
    
    with open(info.DATA_REGION, 'w') as file:
        file.write(json.dumps(regions).replace("{", "{\n").replace("}", "\n}").replace(", ", ",\n"))
    
    return list(regions.values())