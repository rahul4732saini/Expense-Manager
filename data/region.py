try:
    from sys import path
    path.append("..\\Expense Manager")

    import json
    import os.path
    import data.info as info
except Exception:
    raise Exception("0xegbl0001")

def get_regions() -> list[str]:

    # Checking for the existance of the regions file.
    if not os.path.exists(info.DATA_REGION):
        if os.path.exists(info.DATA_PATH):
            raise Exception("0xegbl0002")
        else:
            raise Exception("0xereg0001")
        
    with open(info.DATA_REGION, 'r') as file:
        try:
        # Capturing only the values (names of the countries) of the dictionary.
            regions: list[str] = list(json.load(file).values())
        except Exception:
            raise Exception("0xereg0002")
        
    return regions