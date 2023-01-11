
def validate_account(account):
    if len(account) != 40:
        return False
    try:
        int(account, 16)
    except:
        return False
    return True

def store_basecoin(account):
    with open("data/baseCoin.txt", "w") as f:
        f.write(account)

def get_basecoin():
    try:
        with open("data/baseCoin.txt", "r") as f:
            return f.read()
    except:
        return None
