try:
    from sys import path
    path.append("..\\Expense Manager")

    import requests
except Exception:
    raise Exception("0xegbl0001")

def get_regions():
    URL = "https://countrylist.jquery.app/data/en_GB/country.json"

    try:
        regions: dict = requests.get(URL).json()
    except Exception:
        raise Exception
    
    return list(regions.values())