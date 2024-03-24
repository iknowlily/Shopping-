import mysql.connector


class Databases:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="25762576",
            buffered=True,
            database="fuzhuang",
            auth_plugin='mysql_native_password',
        )
        self.cursor = self.conn.cursor()

db = Databases()
if __name__ == '__main__':
    print(db.__init__())
