try:
    from sys import path
    path.append("..\\Expense Manager")

    import os.path
    import data.info as info
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
                self._verify_settings(settings)
            except Exception:
                raise Exception()
            
        return settings

    def _verify_settings(self, settings: dict):
        # pending...
        ...

    def _write_settings(self, settings: dict):
        settings: str = str(settings).replace("{", "{\n").replace("}", "\n}").replace(", ", ",\n")

        with open(info.DATA_SETTINGS, 'r') as file:
            file.write(settings)

    def set_theme(self, theme: str):
        if theme not in pre_requisites.THEME:
            raise Exception()
        
        settings: dict = self.get_settings()
        settings.update({"theme": "dark" if theme == "light" else "light"})

        self._verify_settings(settings)
        self._write_settings(settings)

    def set_currency(self, currency: str):
        ...