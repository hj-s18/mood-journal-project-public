from app.sql.db_connect import DBConnect
    
class UserDAO:
    #USER INSERT
    def insert_user(self, email, password, name):
        cursor = DBConnect.get_db().cursor()
        sql_insert = 'insert into users (email, password, name) values (%s, %s, %s)'
        ret_cnt = cursor.execute(sql_insert, (email, password, name))
        DBConnect.get_db().close()

        return f'insert OK : {ret_cnt}'

    #USER SELECT
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
    
    #USER UPDATE
    def update_user(self, user_id, email, password, name):
        cursor = DBConnect.get_db().cursor()
        sql_update = 'UPDATE users SET email=%s, password=%s, name=%s WHERE id=%s'
        ret_cnt = cursor.execute(sql_update, (email, password, name, user_id))
        DBConnect.get_db().commit()
        DBConnect.get_db().close()
        return f'Update OK: {ret_cnt} row(s) affected'

    #USER SELECT 2
    def get_user_by_id(self, user_id):
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT * FROM users WHERE id=%s'
        cursor.execute(sql_select, (user_id,))
        row = cursor.fetchone()
        
        if row:
            return {'id': row[0], 'email': row[1], 'password': row[2], 'name': row[3]}
        
        DBConnect.get_db().close()
        return None
    
    
    def get_user_by_email(self, email):
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT * FROM users WHERE email=%s'
        cursor.execute(sql_select, (email,))
        row = cursor.fetchone()
        
        if row:
            return {'id': row[0], 'email': row[1], 'password': row[2], 'name': row[3]}
        
        DBConnect.get_db().close()
        return None
    
    #USER DELETE
    def delete_user(self, user_id):
        cursor = DBConnect.get_db().cursor()
        sql_delete = 'DELETE FROM users WHERE id=%s'
        ret_cnt = cursor.execute(sql_delete, (user_id,))
        DBConnect.get_db().commit()
        DBConnect.get_db().close()
        
        if ret_cnt > 0:
            return f'User ID {user_id} deleted successfully.'
        else:
            return 'User not found.'

if __name__ == '__main__':
    user_list = UserDAO().get_users()
    print(user_list)