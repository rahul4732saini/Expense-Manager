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
            raise Exception()
        
        with open(info.DATA_SETTINGS, 'r') as file:
            try:
                settings: dict = json.load(file)

                if settings.keys() != pre_requisites.SETTINGS_KEYS:
                    raise Exception()

                self._verify_all_settings(settings)
            except Exception:
                raise Exception()
            
        return settings

    def _verify_theme(self, theme: str):
        if theme not in pre_requisites.THEME:
            raise Exception()
        
        return self

    def _verify_default_pay_mode(self, payment_mode: str):
        if payment_mode not in pay_mode.Manage().get_mode_names():
            raise Exception()
        
        return self
    
    def _verify_currency(self, currency: str):
        # pending...
        
        return self
    
    def _verify_all_settings(self, settings: dict) -> None:

        # Verifying all settings.        
        self._verify_theme(settings["theme"])._verify_default_pay_mode(settings["default_payment_mode"])\
        ._verify_currency(settings["currency"])

    def write_settings(self, settings: dict) -> None:
        with open(info.DATA_SETTINGS, 'w') as file:
            json.dump(settings, file, indent = 4)

    def change_theme(self) -> None:
        settings: dict = self.get_settings()
        settings.update({"theme": "dark" if settings["theme"] == "light" else "light"})

        self.write_settings(settings)

    def set_default_payment_mode(self, payment_mode: str) -> None:
        self._verify_default_pay_mode(payment_mode)

        settings = self.get_settings()
        settings.update({"default_payment_mode": payment_mode})
        self.write_settings(settings)

    def set_currency(self, currency: str) -> None:
        self._verify_currency(currency)

        #pending...