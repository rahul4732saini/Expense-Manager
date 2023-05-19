try:
    from sys import path
    path.append("..\\Expense Manager")

    import re
    import os.path
    import data.info as info
    from datetime import date
except Exception:
    raise Exception("0xegbl0001")

class Details:
    def get_details(self) -> dict:
        if not os.path.exists(info.DATA_USER):
            raise Exception()

        with open(info.DATA_USER, 'r') as file:
            details = eval(file.read().replace("\n", ""))

        self._verify_details(details)
        return details
        
    def _verify_details(self, dt: dict) -> None:
    # Using details as dt

        if not all(
            [
                dt["first_name"].__class__ == str and dt["first_name"].__len__() < 15,
                dt["middle_name"] == None or dt["middle_name"].__class__ == str and dt["middle_name"].__len__() < 15,
                dt["last_name"].__class__ == str and dt["last_name"].__len__() < 15,
                dt["email"] == None or dt["email"].__class__ == str,
                dt["region"].__class__ == str,
                dt["date_of_birth"].__class__ == date and dt["date_of_birth"] < date.today()
            ]
        ):
            raise Exception()

    def _write_details(self, details: dict) -> None:
        details = str(details).replace("{", "{\n").replace("}", "\n}").replace(", ", ",\n")

        with open(info.DATA_USER, 'w') as file:
            file.write(details)

    def add_details(self,
                    first_name: str,
                    middle_name: str,
                    last_name: str,
                    email: str,
                    region: str,
                    date_of_birth: date) -> None:
        
        if self.get_details():
            raise Exception()

        details = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "email": email,
            "region": region,
            "date_of_birth": date_of_birth
        }

        self._verify_details(details)
        self._write_details(details)

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
        self._write_details(details)

print(Details().get_details())