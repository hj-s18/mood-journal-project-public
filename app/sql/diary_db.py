# diary list 조회 + 년, 월 필터
# diary list 조회 + 감정(0, 1, 2, 3, 4) 필터
# diary 상세 조회
# diary insert
# diary update -> upsert mysql 구문 -> primary key(id) on duplicate -> 해당 id가 있으면 수정, 해당 id가 없으면 등록
# diary delete

from app.sql.db_connect import DBConnect
    
class DiaryDAO:
    def upsert_diary(self, email, password, name):
        cursor = DBConnect.get_db().cursor()
        sql_insert = 'insert into users (email, password, name) values (%s, %s, %s)'
        ret_cnt = cursor.execute(sql_insert, (email, password, name))
        DBConnect.get_db().close()

        return f'insert OK : {ret_cnt}'

    def delete_diary(self):
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

    def get_list_diaries_with_date(self):
        return

    def get_list_diaries_with_mood(self):
        return
    
    def get_diary(self):
        return
    
if __name__ == '__main__':
    user_list = UserDAO().get_users()
    print(user_list)