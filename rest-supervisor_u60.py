import os
while True:
    try:
        response = self.conn.getresponse().read()
        print(response)
    except:
        os.system("python rest-checker_u60.py")