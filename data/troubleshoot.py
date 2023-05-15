PAYMENT_MODE = {
    "0xepym0001": {
        "data_file_content":
        str([
            {
                "name": "cash",
                "color": "green",
                "initial_balance": 0,
                "catagory": "wallet"
                }
            ]
        ).replace("{", "{\n")\
        .replace("}", "\n}")\
        .replace("[", "[\n")\
        .replace("]", "\n]")\
        .replace(", ", ",\n")
    }
}

TRANSACTIONS = {
}