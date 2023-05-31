r"""
Module related to functions used
for the deletion of transactions, catagories and payment_modes.

This exports:

-   (function) remove_transactions: used for the deletion of all transactions with corresponding transaction ID proivided.
-   (function) remove_catagory: used for the deletion of all catagories with corresponding catagory name provided.
-   (function) remove_payment_mode: used for the deletion of all payment modes with corresponding payment mode name provided.

"""

try:
    from sys import path
    path.append("..\\Expense Manager")

    import os
    import json
    import data.info as info
    import user.settings as settings
    import transactions.filter as filter
    import transactions.details as details
    import data.pre_requisites as pre_requisites
    import transactions.payment_mode as pay_mode
    from transactions.catagory import Income, Expense
except Exception:
    raise Exception("0xegbl0001")

def remove_transactions(transactions_id: str | list[str]) -> None:
    if transactions_id.__class__ not in (str, list):
            raise Exception("0xerem0001")

    transactions_id: set = set(transactions_id) if transactions_id.__class__ == list else {transactions_id}

    # List of transactions_id queued for deletion that exist, i.e., are valid.
    valid_transactions_id: list[str] = [i for i in transactions_id if i in details.Manage().get_transactions_id()]

    # Deleting transaction files with related transactions_id.  
    i: str
    for i in valid_transactions_id:
        os.system("del \"%s\\trn_id_%s.txt\"" % (info.DATA_TRANSACTIONS, i))

    # Raising error if one or more of the payment modes names provided are not existant.
    if len(valid_transactions_id) != len(transactions_id):
        raise Exception("0xerem0004")

def remove_catagory(catagories: str | list[str], transaction_type: str) -> None:
    if transaction_type not in pre_requisites.TRANSACTION_TYPES or catagories.__class__ not in (str, list):
        raise Exception("0xerem0002")
    
    catagory_type: dict = Income().get_catagories() if transaction_type == "income" else Expense().get_catagories()
    
    catagories: set = set(catagories) if catagories.__class__ == list else {catagories}
    valid_catagories: list[str] = [i for i in catagories if i in catagory_type]

    if "others" in valid_catagories:
        raise Exception("0xerem0005")
    
    for i in filter.Filter().catagory(valid_catagories, transaction_type).filtered_list:
        i.update({"catagory": "others"})
        
        details.Manage().write_transaction(i, exists = True)

    target: dict = {key: value for key, value in catagory_type.items() if key not in valid_catagories}

    with open("%s\\%s.json" % (info.DATA_CATAGORIES, transaction_type), 'w') as file:
        json.dump(target, file, indent = 4)

    # Raising error if one or more of the catagory names provided are non existant.
    if len(catagories) != len(valid_catagories):
        raise Exception("0xerem0006")

def remove_payment_mode(payment_modes: str | list[str]) -> None:
    if payment_modes.__class__ not in (str, list):
        raise Exception("0xerem0003")
    
    # List of payment mode names queued for deletion that exist, i.e., are valid.
    payment_modes: set = set(payment_modes) if payment_modes.__class__ == list else {payment_modes}
    valid_payment_modes: list[str] = [i for i in payment_modes if i in pay_mode.Manage().get_mode_names()]

    if "cash" in valid_payment_modes:
        raise Exception("0xerem0007")

    for i in filter.Filter().payment_mode(valid_payment_modes).filtered_list:
        i.update({"payment_mode": "cash"})
        
        details.Manage().write_transaction(i, exists = True)

    setting:dict = settings.Manage().get_settings()
    setting.update({"default_payment_mode": "cash"})

    settings.Manage().write_settings(setting)

    # Creating payment modes list of only dictionaries that aren't queued for deletion.
    target: list[dict] = [i for i in pay_mode.Manage().get_modes() if i["name"] not in valid_payment_modes]
    
    with open(info.DATA_PAYMENT_MODES, 'w') as file:
        json.dump(target, file, indent = 4)

    # Raising error if one or more of the payment modes names provided are non existant.
    if len(valid_payment_modes) != len(payment_modes):
        raise Exception("0xerem0008")