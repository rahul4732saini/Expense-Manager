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

    import re
    import json
    import os.path
    import data.info as info
    from functools import wraps
    from data.region import get_regions
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_details(self) -> dict:
        if not os.path.exists(info.DATA_USER):
            raise Exception("0xegbl0001") if not os.path.exists(info.DATA_PATH) else Exception()

        try:
            with open(info.DATA_USER, 'r') as file:
                details: dict = json.load(file)

                # Verifying the credentials.
                self._verify_all_details(details)
        except Exception:
            raise Exception()
        
        return details
    
    def _name_verification(function):
        
        @wraps(function)
        def wrapper(self, *args, **kwargs):

            if not re.match(r"^[a-z, A-Z, \s]+$", function(self, *args, **kwargs)):
                raise Exception()
            
            return self
        
        return wrapper
    
    @_name_verification
    def _verify_first_name(self, first_name: str):
        return first_name
    
    @_name_verification
    def _verify_middle_name(self, middle_name: str):
        if middle_name != None:
            return middle_name
        
    @_name_verification
    def _verify_last_name(self, last_name: str):
        return last_name
        
    def _verify_region(self, region: str | None):
        if region.title() not in get_regions():
            raise Exception()
        
        return self
        
    def _verify_email(self, email: str | None):
        if email != None and not re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email):
            raise Exception()
        
        return self
            
    def _verify_all_details(self, details: dict) -> None:

        # Verifying all user_details
        self._verify_email(details["email"])._verify_region(details["region"])._verify_first_name(details["first_name"])\
        ._verify_middle_name(details["middle_name"])._verify_last_name(details["last_name"])

    def edit_details(self,
                     first_name: str | None = None,
                     middle_name: str | None = None,
                     last_name: str | None = None,
                     email: str | None = None,
                     region: str | None = None) -> None:
        
        edit = {key: value for key, value in locals().items() if key != "self" and value != None}
        
        if len(edit) == 0:
            raise Exception()
        
        verify: dict = {
            "first_name": self._verify_first_name,
            "middle_name": self._verify_middle_name,
            "last_name": self._verify_last_name,
            "email": self._verify_email,
            "region": self._verify_region
        }
        
        key: str
        value: str
        for key, value in edit.items():
            verify[key](value)

        details = self.get_details()
        details.update(edit)

        with open(info.DATA_USER, 'w') as file:
            json.load(details, file)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    ...