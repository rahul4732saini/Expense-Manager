r"""
Module related to functions required for the
management and trobuelshooting of user details.

(Class) User:
-------------
-   get_details: return all the user details in the form of a dicionary.
-   edit_details: used to alter the user details.
"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    import json
    import os.path
    import data.info as info
    from data.region import get_regions
    from email_validator import validate_email
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception("0xegbl0001")

class User:
    def get_details(self) -> dict:
        if not os.path.exists(info.DATA_USER):
            raise Exception("0xegbl0001") if not os.path.exists(info.DATA_PATH) else Exception()

        try:
            with open(info.DATA_USER, 'r') as file:
                details: dict = json.load(file)

                if details.__class__ != dict:
                    raise Exception

                self._verify_details(details)
        except Exception:
            raise Exception()
        
        return details
    
    def _verify_details(self, user_details: dict) -> None:
        # taking user_details as namespace details
        details = user_details

        # Verifying the presence of all required keys.
        if details.keys() != pre_requisites.USER_DETAILS_KEYS:
            raise Exception()

        if not all(
            [   
                # Verifying user_name.
                details["first_name"].__class__ == str and len(details["first_name"]) < 15 and details["first_name"].isalpha(),
                details["middle_name"] == None or details["middle_name"].__class__ == str and len(details["middle_name"]) < 15 and details["middle_name"].isalpha(),
                details["last_name"].__class__ == str and len(details["last_name"]) < 15 and details["last_name"].isalpha(),

                # Verifying region.
                details["region"] == None or details["region"].__class__ == str and details["region"] in get_regions(),
            ]
        ):
            raise Exception()
        
        # Verifying email_id.
        try:
            validate_email(details["email"])
        except Exception:
            raise Exception()

    def edit_details(self,
                     first_name: str = None,
                     middle_name: str = None,
                     email: str = None,
                     region: str = None) -> None:
        
        edit = {key: value for key, value in locals().items() if key != "self" and value != None}
        
        details = self.get_details()
        details.update(edit)
        self._verify_details(details)
        
        with open(info.DATA_USER, 'w') as file:
            json.dump(details, file, indent = 4)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    ...