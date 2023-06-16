try:
    from sys import path
    path.append("..\\Expense Manager")

    import pickle
    import os.path
    import data.info as info
    from common.objects import Settings
except Exception:
    raise Exception()

class Manage:
    def get_settings(self):
        assert os.path.exists(info.DATA_SETTINGS), "<error>"
        
        with open(info.DATA_SETTINGS, 'r') as file:
            try:
                settings: Settings = pickle.load(file)

                assert settings.__class__ == Settings
            except Exception:
                raise Exception()
            
        return settings

    def write_settings(self, settings: Settings) -> None:

        # Verfying the type of the object.
        assert settings.__class__ == Settings

        with open(info.DATA_SETTINGS, 'w') as file:
            pickle.dump(settings, file)

    def change_theme(self) -> None:
        settings: Settings = self.get_settings()
        settings.theme = "light" if settings.theme == "light" else "dark"

        self.write_settings(settings)

    def set_default_payment_mode(self, payment_mode: str) -> None:
        settings: Settings = self.get_settings()
        settings.default_payment_mode = payment_mode

        self.write_settings(settings)

    def set_currency(self, currency: str) -> None:
        settings: Settings = self.get_settings()
        settings.currency = currency

        self.write_settings(currency)