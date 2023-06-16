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

    import pickle
    import os.path
    import data.info as info
    from common.objects import User
except Exception:
    raise Exception("0xegbl0001")

class Manage:
    def get_details(self) -> User:
        assert os.path.exists(info.DATA_USER), "<error>"
        
        try:
            with open(info.DATA_USER, 'r') as file:
                details: User = pickle.load(file)

            assert details.__class__ == User
        except Exception:
            raise Exception()
        
        return details

    def edit_details(self,
                     first_name: str | None = None,
                     middle_name: str | None = None,
                     last_name: str | None = None,
                     email: str | None = None,
                     region: str | None = None) -> None:
        
        edit: dict = {key: value for key, value in locals().items() if (key, value) != ("self", None)}
        
        assert len(edit) > 0, "<error>"

        user_details: User = self.get_details()

        mapping: dict = {
            "first_name": user_details.first_name,
            "middle_name": user_details.middle_name,
            "last_name": user_details.last_name,
            "email": user_details.email_id,
            "region": user_details.region
        }

        key: str
        value: str
        for key, value in edit.items():
            mapping[key] = value

        with open(info.DATA_USER, 'w') as file:
            pickle.dump(user_details, file)