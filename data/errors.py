ERROR = {
    "__global__": {
        "0xegbl0001": "One or more of the required modules are missing.",
        "0xegbl0002": "The data folder was not found.",
        "0xegbl0003": "Class attributes must not be changed from their default values.",
        "0xegbl0004": "Invalid arguments provided for setting class attributes."
    },
    "common": {
        "directory": {
            "0xedir0001": "The path specified cannot be found."
        }
    },
    "transactions": {
        "catagory": {
            "0xecat0001": "Catagories save folder not found.",
            "0xecat0002": "Income Catagories file not found.",
            "0xecat0003": "Income catagories file found to be corrupted.",
            "0xecat0004": "Provided catagory name is not valid.",
            "0xecat0005": "There is no catagory in existance with the provided name.",
            "0xecat0006": "Cannot use the provided catagory name as a catagory with similar name already exists.",
            "0xecat0007": "Expense Catagories file not found.",
            "0xecat0008": "Expense Catagories file found to be corrupted.",
            "0xecat0009": "The income catagories data file exceeds the limit of catagories that can be stored (50).",
            "0xecat0010": "The expense catagories data file exceeds the limit of catagories that can be stored (50).",
            "0xecat0011": "The catagory name cannot exceed the length of 25 characters.",
        },
        "details": {
            "0xetrn0001": "Unexpected files found in the transactions save folder.",
            "0xetrn0002": "Files with unexpected extension found in the save folder.",
            "0xetrn0003": "Corrupted transaction files found in the save folder.",
            "0xetrn0004": "Transactions save folder not found.",
            "0xetrn0005": "The proivided transaction ID is invalid.",
            "0xetrn0006": "Cannot find any transaction with the provided transaction_ID.",
            "0xetrn0007": "There was an error in creating the transaction.",
            "0xetrn0008": "There was an error in verifying the transaction.",
            "0xetrn0009": "The provided catagory is not valid.",
            "0xetrn0010": "Unexpected arguments detected for transaction deletion.",
            "0xetrn0011": "One or more transactions queued for deletion do not exist.",
            "0xetrn0012": "No arguments were provided for editing the transaction."
        },
        "export": {
            "0xetrn0ex1": "Invalid transactions_ID were provided as arguments.",
            "0xetrn0ex2": "The provided save location for the export file cannot be found.",
            "0xetrn0ex3": "No proper name provided for the export file.",
            "0xetrn0ex4": "Cannot continue the process as one or more of the target transaction files are corrupted."
        },
        "analysis": {
            "0xetrn01an": "Invalid arguments detected while analysing transactions.",
        },
        "payment_mode": {
            "0xepym0001": "Payment Modes file cannot be found.",
            "0xepym0002": "Payment Modes data file was found to be corrupted.",
            "0xepym0003": "There was an error in verifying the payment mode.",
            "0xepym0004": "Payment mode name cannot contain more than 30 characters.",
            "0xepym0005": "You cannot exceed the limit of 30 payment modes.",
            "0xepym0006": "There was an error in finding the payment mode with the provided name.",
            "0xepym0007": "No arguments were provided for editing the payment mode.",
            "0xepym0008": "Cannot use the provided payment mode name as a payment mode with similar name already exists.",
            "0xepym0009": "The payment mode data file exceeds the limit of payment modes that can be stored (30).",
            "0xepym0010": "Duplicate payment modes were found in the data folder.",
            "0xepym0011": "Invalid arguments provided for payment modes deletion."
        },
        "filter": {
            "0xetrn01fl": "Invalid arguments were provided for filtering transactions.",
        },
        "sort": {
            "0xetrn01sr": "Unexpected arguments were provided for sorting transactions."
        },
        "remove": {
            "0xerem0001": "Unexpected arguments provided for deleting transactions.",
            "0xerem0002": "Unexpected arguments provided for deleting catagories.",
            "0xerem0003": "Unexpected arguments provided for deleting payment modes.",
            "0xerem0004": "One or more transactions ID provided for transactions deletion are invalid.",
            "0xerem0005": "One or more catagories queued for deletion cannot be removed.",
            "0xerem0006": "One or more catagory names provided for cataogories deletion are invalid.",
            "0xerem0007": "One or more payment modes queued for deletion cannot be removed.",
            "0xerem0008": "One or more payment mode names provided for payment modes deletion are invalid.",
        }
    },
    "budgets": {
        "details": {
            "0xebgt0001": "Budgets save folder not found.",
            "0xebgt0002": "Unexpected files found in the budgets save folder.",
            "0xebgt0003": "There was an error in verifying the budget.",
            "0xebgt0004": "Corrupted budget files found in the save folder.",
            "0xebgt0005": "There was an error in creating the budget.",
            "0xebgt0006": "Cannot find any budget with the provided budget_ID.",
            "0xebgt0007": "One or more budgets queued for deletion do not exist.",
            "0xebgt0008": "No arguments were provided for editing the transaction.",
            "0xebgt0009": "Cannot create the budget as a budget has already been created for the provided month.",
            "0xebgt0010": "Budgets with similar active month were detected.",
        },
        "filter": {
            "0xebgt01fl": "Invalid arguments were provided for filtering budgets.",
        },
        "sort": {
            "0xebgt01sr": "Unexpected arguments were provided for sorting transactions."
        }
    },
    "data": {
        "region": {
            "0xereg0001": "Regions data file not found.",
            "0xereg0002": "Regions data file was found to be corrupted."
        }
    },
    "user": {
        "backup": {
            "0xebkp01us": "Invalid save_location / file_name provided for the backup file.",
            "0xebkp02us": "Invalid file_location provided for the backup file.",
            "0xebkp03us": "The backup was found to be corrupted.",
            "0xebkp04us": "The backup file provided for restoration is not of a valid object type.",
            "0xebkp05us": "The backup file cannot be created as another file with the same name already exists.",
            "0xebkp06us": "The file provided for restoration is not a backup file."
        }
    }
}