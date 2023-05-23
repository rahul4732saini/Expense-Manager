try:
    from sys import path
    path.append("..\\Expense Manager")

    import os.path
    import data.info as info
    import transactions.payment_mode as pay_mode
    import data.pre_requisites as pre_requisites
except Exception:
    raise Exception()

class Manage:
    def get_settings(self):
        if not os.path.exists(info.DATA_SETTINGS):
            raise Exception("0xegbl0002") if not os.path.exists(info.DATA_SETTINGS) else Exception()
        
        with open(info.DATA_SETTINGS, 'r') as file:
            try:
                settings: dict = eval(file.read().replace("\n", ""))

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

    def _write_settings(self, settings: dict):
        settings: str = str(settings).replace("{", "{\n").replace("}", "\n}").replace(", ", ",\n")

        with open(info.DATA_SETTINGS, 'w') as file:
            file.write(settings)

    def set_theme(self, theme: str):
        if theme not in pre_requisites.THEME:
            raise Exception()
        
        settings: dict = self.get_settings()
        settings.update({"theme": "dark" if theme == "dark" else "light"})

        self._verify_settings(settings)
        self._write_settings(settings)

    def set_default_payment_mode(self, payment_mode: str) -> None:
        if payment_mode not in pay_mode.Manage().get_mode_names():
            raise Exception()
        
        settings = self.get_settings()
        settings.update({"default_payment_mode": payment_mode})

        self._verify_settings(settings)
        self._write_settings(settings)