import psycopg2 as pg
visited=[]
s=0
g=0
l={}

class Student:
    def __init__(self,name,sid,ph,city,dob,pwd,fees,room,days):
        self.sid=int(sid)
        self.pwd=pwd
        self.name=name
        self.ph=ph
        self.city=city
        self.dob=dob
        self.fees=int(fees)
        self.room=int(room)
        self.days=int(days)
        
    
    @classmethod
    def remove_from_db(self,sid):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('select sid from student')
                res=cursor.fetchall()
                for i in res:
                    if str(i[0])==sid:
                        cursor.execute('delete from feedback where sid=%s',(sid,))
                        cursor.execute('delete from poll where sid=%s',(sid,))
                        cursor.execute('delete from request where sid=%s',(sid,))
                        cursor.execute('delete from student where sid=%s',(sid,))
                        return 1
                return 0
	
    @classmethod
    def load_all(self):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT sid,name,room,ph,days,fees from student order by sid')
                info=cursor.fetchall()
                return info


    @classmethod
    def load_from_db(self,sid):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT pwd,name,room,ph,dob,city from student where sid=%s',(sid,))
                info=cursor.fetchone()
                return info

                			
            
    @classmethod
    def setpwd(self,sid,pwd):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute('UPDATE student set pwd=%s where sid=%s',(pwd,sid))
                except:
                    return
                
    @classmethod
    def put_att(self,sid):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('UPDATE student set days=days+1 where sid=%s',(sid,))
		
    def save_to_db(self):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into student values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(self.sid,self.name,self.city,self.ph,self.dob,self.days,self.fees,self.pwd,self.room))
                cursor.execute('UPDATE room set vacancy=vacancy-1 where roomid=%s',(self.room,))
        
        
class Feedback:
    def __init__(self,sid,content):
        self.sid=sid
        self.content=content
        
    def save_to_db(self):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into feedback (sid,content) values (%s,%s)',(self.sid,self.content))
                
    @classmethod
    def load_from_db(self):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT sid,content from feedback')
                info=cursor.fetchall()
                return info



class Food:
    def load_from_db():
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name from food where type='breakfast'")
                info=cursor.fetchall()	
                return info
            
            
    def poll(name,sid):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into poll values (%s,%s)',(name,sid))
                

    def count():
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT poll.name,count(*),type from poll,food where poll.name=food.name group by poll.name,type order by count(*) desc')
                info=cursor.fetchall()
                print(info)
                return info	
   
    @classmethod			
    def load_all(self):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * from food')
                info=cursor.fetchall()
                return info
    
    
    def remove_from_db(rname):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('select name from food')
                res=cursor.fetchall()
                for i in res:
                    if i[0]==rname:
                        try:
                            cursor.execute('delete from poll where name=%s',(rname,))
                            cursor.execute('delete from food where name=%s',(rname,))
                        except:
                            cursor.execute('delete from food where name=%s',(rname,))
                            return 1
                return 0

    def save_to_db(name,typ):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into food values(%s,%s)',(name,typ))

class Bill:
   
    def save_to_db(url):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into bill (url) values(%s)',(url,))
         
    def load_from_db():
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * from bill')
                info=cursor.fetchall()
                return info			

class Room:
    def request(rid,sid):
        global s
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute('INSERT into request values (%s,%s)',(sid,rid))
                    cursor.execute('SELECT vacancy from room where roomid=%s',(rid,))
                    info=cursor.fetchone()
                    print(info[0])
                    if str(info[0])!=str(0):
                        cursor.execute('UPDATE room set vacancy=vacancy+1 where roomid=(select room from student where sid=%s)',sid)
                        cursor.execute('UPDATE room set vacancy=vacancy-1 where roomid=%s',(rid,))
                        cursor.execute('UPDATE student set room=%s where sid=%s',(rid,sid))
                        return
                except:
                    print('exception')
                    return
                
                
    def swap(sid,sid1):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT room from student where sid=%s',(sid,))
                info=cursor.fetchone()
                cursor.execute('SELECT room from student where sid=%s',(sid1,))
                info1=cursor.fetchone()
                print(info1[0])
                cursor.execute('UPDATE student set room=%s where sid=%s',(info1[0],sid))
                cursor.execute('UPDATE student set room=%s where sid=%s',(info[0],sid1))
                
                
    @classmethod
    def load_all(self):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * from room order by roomid')
                info=cursor.fetchall()
                return info
		
								
class Employee:
    def __init__(self,name, eid, ph,city,dob,gen,salary,days):
        self.eid=int(eid)
        self.gen=gen
        self.name=name
        self.ph=ph
        self.city=city
        self.dob=dob
        self.salary=int(salary)
        self.days=int(days)

    @classmethod
    def remove_from_db(self,eid):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('select eid from employee')
                res=cursor.fetchall()
                for i in res:
                    if str(i[0])==eid:
                        cursor.execute('delete from employee where eid=%s',(eid,))
                        return 1
                return 0

    def save_to_db(self):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into employee values (%s,%s,%s,%s,%s,%s,%s,%s)',
(self.eid,self.name,self.city,self.ph,self.salary,self.dob,self.gen,self.days))
                                  
                
                
    @classmethod
    def load_all(self):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT eid,name,ph,days,salary from employee order by eid')
                info=cursor.fetchall()
                print(info)
                return info
            
            
    @classmethod
    def put_att(self,eid):
        with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            with connection.cursor() as cursor:
                cursor.execute('UPDATE employee set days=days+1 where eid=%s',(eid,))
