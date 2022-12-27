
def validate_account(account):
    if len(account) != 40:
        return False
    try:
        int(account, 16)
    except:
        return False
    return True
