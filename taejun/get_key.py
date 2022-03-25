import os.path

def get_key() :
    f = open(os.path.expanduser('~')+"/.upbit_key.dat",'r')
    access_key = f.readline().split()[0]
    secret_key = f.readline().split()[0]
    print('access_key = %s'%access_key)
    print('secret_key = %s'%secret_key)

if __name__ == "__main__" :
    get_key()
