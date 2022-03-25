import pyupbit

def get_balance(pyupbit.Upbit upbit, string ticker) :
    return upbit.get_balance(ticker)

