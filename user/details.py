r"""
Module related to functions required for the
management and trobuelshooting of user details.

(Class) User:
-------------
-   get_details: return all the user details in the form of a dicionary.
-   edit_details: used to alter the user details.
"""

# Broken code...
# To be fixed...

try:
    from sys import path
    path.append("..\\Expense Manager")

    import re
    import os.path
    import data.info as info
    from datetime import date
    from data.region import get_regions
    from email_validator import validate_email
except Exception:
    raise Exception("0xegbl0001")

class User:
    def get_details(self) -> dict:
        if not os.path.exists(info.DATA_USER):
            raise Exception() if not os.path.exists(info.DATA_PATH) else Exception()

        try:
            with open(info.DATA_USER, 'r') as file:
                details = eval(file.read().replace("\n", ""))

                if details.__class__ != dict:
                    raise Exception

                self._verify_details(details)
        except Exception:
            raise Exception()
        
        return details

    def _verify_details(self, user_details: dict) -> None:
        ...

    def edit_details(self,
                     first_name: str,
                     middle_name: str,
                     email: str,
                     region: str,
                     date_of_birth: date) -> None:
        
        details = self.get_details()
        edit = {key: value for key, value in locals().items() if key != "self" and value != None}

        details.update(edit)
        self._verify_details(details)
        
        details = str(details).replace("{", "{\n").replace("}", "\n}").replace(", ", ",\n")

        with open(info.DATA_USER, 'w') as file:
            file.write(details)

class TroubleShoot:
    # The following functions return True if fixed else False if the problem isn't fixed.
    # Mention to the data.errors file for more information about the errors.

    ...