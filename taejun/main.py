import pyupbit
import misc


def main():
    [access_key, secret_key] = misc.get_key()

    print('access_key = %s' % access_key)
    print('secret_key = %s' % secret_key)

    upbit = pyupbit.Upbit(access_key, secret_key)
    print(misc.get_balance(upbit, "KRW"))


if __name__ == "__main__":
    main()
