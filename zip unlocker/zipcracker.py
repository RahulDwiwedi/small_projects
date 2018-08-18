from zipfile import ZipFile


def cracker(passw):
    try:

        f = ZipFile('test.7z')
        f.extractall(path="loc/", pwd=passw)
        print("Password Found : "+str(passw))


    except Exception as e:
        print(e)
        pass


pass_file = open('test_password.txt', 'r')
passwords = pass_file.read().split("\n")

for password in passwords:
    password = bytes(password, 'utf-8')
    cracker(password)
