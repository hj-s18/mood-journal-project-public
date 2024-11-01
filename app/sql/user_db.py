from app.sql.db_connect import DBConnect
    
class UserDAO:
    def insert_user(self, email, password, name):
        cursor = DBConnect.get_db().cursor()
        sql_insert = 'insert into users (email, password, name) values (%s, %s, %s)'
        ret_cnt = cursor.execute(sql_insert, (email, password, name))
        DBConnect.get_db().close()

        return f'insert OK : {ret_cnt}'

    def get_users(self):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'select * from users'

        try:
            # 실행
            cursor.execute(sql_select)

            rows = cursor.fetchall()
            for row in rows:
                temp = {
                    'id': row[0], 
                    'email': row[1], 
                    'name': row[3],
                    }
                ret.append(temp)
        except:
            pass

        finally:
            DBConnect.get_db().close()
            
        return ret

if __name__ == '__main__':
    user_list = UserDAO().get_users()
    print(user_list)