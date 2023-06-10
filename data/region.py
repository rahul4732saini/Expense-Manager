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
        raise Exception("0xereg0001")
        
    with open(info.DATA_REGION, 'r') as file:
        try:
        # Capturing only the values (names of the countries) of the dictionary.
            regions: list[str] = json.load(file)
        except Exception:
            raise Exception("0xereg0002")
        
    return regions

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    ...