# == Aplication Info

APPLICATION_NAME = "Expense Manager"
APPLICATION_VERSION = "1.00"
APPLICATION_DEVELOPER = "Rahul Saini"
APPLICATION_INSTALL_DATE = "10-04-2023"

# == System Info

USER_NAME = "rahul"
MAIN_DRIVE = "C:"

# == Installation Folder Path

MAIN_PATH = "E:\\Projects\\Python Projects\\GUI_Projects\\Expense Manager"

# == Data Files Folder Path

DATA_PATH = "%s\\Users\\%s\\Appdata\\Roaming\\expense_mgr" % (MAIN_DRIVE,USER_NAME)

# == Data Folder Sub Folder Paths

DATA_PAYMENT_MODES = "%s\\payment_modes.json" % DATA_PATH
DATA_TRANSACTIONS = "%s\\transactions.pickle" % DATA_PATH
DATA_BUDGETS = "%s\\budgets" % DATA_PATH
DATA_CATAGORIES = "%s\\catagories" % DATA_PATH
DATA_USER = "%s\\user_details.json" % DATA_PATH
DATA_SETTINGS = "%s\\settings.json" % DATA_PATH
DATA_REGION = "%s\\regions.json" % DATA_PATH
DATA_SECURITY = "%s\\security" % DATA_PATH

# == Cache File Path

DATA_CACHE = "%s\\Windows\\Temp\\exp_mg_cache.pickle" % MAIN_DRIVE