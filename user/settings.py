try:
    from sys import path
    path.append("..\\Expense Manager")

    import json
    import os.path
    import data.info as info
    import data.pre_requisites as pre_requisites
    import transactions.payment_mode as pay_mode
except Exception:
    raise Exception()

class Manage:
    def get_settings(self):
        if not os.path.exists(info.DATA_SETTINGS):
            raise Exception("0xegbl0002") if not os.path.exists(info.DATA_SETTINGS) else Exception()
        
        with open(info.DATA_SETTINGS, 'r') as file:
            try:
                settings: dict = json.load(file)

                if settings.__class__ != dict:
                    raise Exception()

                self._verify_settings(settings)
            except Exception:
                raise Exception()
            
        return settings

    def _verify_settings(self, settings: dict):
        try:
            if not all(
                [
                    settings["theme"] in pre_requisites.THEME,
                    settings["default_payment_mode"] in pay_mode.Manage().get_mode_names()
                ]
            ):
                raise Exception
        except Exception:
            raise Exception()

    def write_settings(self, settings: dict):
        self._verify_settings(settings)

        with open(info.DATA_SETTINGS, 'w') as file:
            json.dump(settings, file, indent = 4)

    def change_theme(self):
        settings: dict = self.get_settings()
        settings.update({"theme": "dark" if settings["theme"] == "light" else "light"})

        self.write_settings(settings)

    def set_default_payment_mode(self, payment_mode: str) -> None:
        if payment_mode not in pay_mode.Manage().get_mode_names():
            raise Exception()
        
        settings = self.get_settings()
        settings.update({"default_payment_mode": payment_mode})

        self.write_settings(settings)