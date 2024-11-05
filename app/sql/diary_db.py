# diary list 조회 + 년, 월 필터
# diary list 조회 + 감정(0, 1, 2, 3, 4) 필터
# diary 상세 조회
# diary insert
# diary update -> upsert mysql 구문 -> primary key(id) on duplicate -> 해당 id가 있으면 수정, 해당 id가 없으면 등록
# diary delete

# from app.sql.db_connect import DBConnect
import pymysql
from app.sql.db_connect import DBConnect
        
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
    
    def upsert_diary(self, user_id, mood, body, date, id = None):
        db = DBConnect.get_db()
        cursor = db.cursor()
        sql_upsert = '''
        insert into diaries (id, user_id, mood, body, date)
        values (%s, %s, %s, %s, %s)
        on duplicate key update
            user_id = VALUES(user_id),
            mood = VALUES(mood),
            body = VALUES(body),
            file_urls = VALUES(file_urls),
            date = VALUES(date)
        '''
        if id:
            params = (id, user_id, mood, body, date)
        else :
            params = (None, user_id, mood, body, date)
        
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

    def get_list_diaries_with_date(self, user_id, year, month):
        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month + 1}-01"

        ret = []
        db = DBConnect.get_db()
        cursor = db.cursor()
        sql_select = "select * from diaries where date >= %s and date < %s and user_id = %s"

        try :
            cursor.execute(sql_select, (start_date, end_date, user_id))            
            rows = cursor.fetchall()
            
            for row in rows:
                temp = {
                    'id' : row[0],
                    'mood' : row[2],
                    'body' : row[3],
                    'file_urls' : row[4],
                    'day': row[5].day,
                    'date' : row[5]
                }
                ret.append(temp)
            
            return ret
        except Exception as e:
            print("get_list_diaries_with_date Error :", e)
        finally :
            db.close() 


    def get_list_diaries_with_mood(self, user_id, mood_choice):
        ret = []
        db = DBConnect.get_db()
        cursor = db.cursor()
        
        try :
            # mood_choice = int(input("0~4 기분을 고르세요. >>>"))
            if mood_choice not in range(0,5) :
                print("유효하지 않은 기분 값입니다.")
                return ret 
            
            sql_select = "select * from diaries where mood = %s and user_id = %s"
            cursor.execute(sql_select, (mood_choice, user_id))
            rows = cursor.fetchall()
            
            for row in rows :
                temp = {
                    'id' : row[0],
                    'mood' : row[2],
                    'body' : row[3],
                    'file_urls' : row[4],
                    'date' : row[5]
                }
                ret.append(temp)
            return ret
                
        except Exception as e:
            print("get_list_diaries_with_date Error :", e)
        finally :
            db.close() 
            
                
                
    def get_diary(self, id):
        ret = []
        db = DBConnect.get_db()
        cursor = db.cursor()
        sql_select = 'select * from diaries where id = %s'
        
        try :
            cursor.execute(sql_select,(id,))
            row = cursor.fetchall()
            ret = {
                'id' : row[0][0],
                'mood' : row[0][2],
                'body' : row[0][3],
                'file_urls' : row[0][4],
                'date' : row[0][5]
            }
            
            return ret
            
        except Exception as e:
            print("get_list_diaries_with_date Error :", e)
        finally :
            db.close() 
            
            
            
                
if __name__ == '__main__':
    
    # DiaryDAO().delete_diary(4)
    # DiaryDAO().upsert_diary(1, 0, "testbody", "testfiles", "2024-11-04")
    # print(DiaryDAO().get_list_diaries_with_date(1, 2024, 10))
    print(DiaryDAO().get_list_diaries_with_mood(1, 1))

    
    # diaries_list = DiaryDAO().get_diaries()
    # print(diaries_list)