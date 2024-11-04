# diary list 조회 + 년, 월 필터
# diary list 조회 + 감정(0, 1, 2, 3, 4) 필터
# diary 상세 조회
# diary insert
# diary update -> upsert mysql 구문 -> primary key(id) on duplicate -> 해당 id가 있으면 수정, 해당 id가 없으면 등록
# diary delete

# from app.sql.db_connect import DBConnect
import pymysql

class DBConnect:
    @classmethod
    def get_db(self):
        return pymysql.connect(
            user="root",
            passwd="test1234!",
            host="127.0.0.1",
            db="mood_journal_project",
            charset="utf8",
            autocommit=True,
        )
        
class DiaryDAO:
    
    def get_diaries(self) :
        
        ret = []
        db = DBConnect.get_db()
        cursor = db.cursor()
        sql_select = 'select * from diaries'
        
        try : 
            cursor.execute(sql_select)
            rows = cursor.fetchall()
            print(rows)
            for row in rows :
                temp = {
                    'id' : row[0],
                    'userid' : row[1],
                    'mood' : row[2],
                    'body' : row[3],
                    'file_urls' : row[4],
                    'date' : row[5]
                }
                ret.append(temp)
        except Exception as e: 
            print("get_diaries Error :", e)
        finally : 
            db.close()
        return ret
    
    def upsert_diary(self, user_id, mood, body, file_urls, date, id = None):
        db = DBConnect.get_db()
        cursor = db.cursor()
        sql_upsert = '''
        insert into diaries (id, user_id, mood, body, file_urls, date)
        values (%s, %s, %s, %s, %s, %s)
        on duplicate key update
            user_id = VALUES(user_id),
            mood = VALUES(mood),
            body = VALUES(body),
            file_urls = VALUES(file_urls),
            date = VALUES(date)
        '''
        if id:
            params = (id, user_id, mood, body, file_urls, date)
        else :
            params = (None, user_id, mood, body, file_urls, date)
        
        try :    
            ret_cnt = cursor.execute(sql_upsert, params)
            db.commit()
        except Exception as e:
            print("upsert Error :", e)
            db.rollback()
        finally :
            db.close()
                        

    def delete_diary(self, id):
        db = DBConnect.get_db()
        cursor = db.cursor()
        sql_delete = 'delete from diaries where id=%s'
        
        try :
            ret_cnt = cursor.execute(sql_delete, (id,))
            db.commit()
        except Exception as e:
            print("delete Error :", e)
            db.rollback()
        finally :
            db.close()
        

    # def get_list_diaries_with_date(self):

            

    # def get_list_diaries_with_mood(self):
    #     return
    
    # def get_diary(self):
    #     return
    
if __name__ == '__main__':
    
    # DiaryDAO().delete_diary(4)
    # DiaryDAO().upsert_diary(1, 0, "testbody", "testfiles", "2024-11-04")
    
    diaries_list = DiaryDAO().get_diaries()
    print(diaries_list)