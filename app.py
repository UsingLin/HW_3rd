import lib
import sqlite3 as sql3


#連線資料庫，新增電影資料表
conn = sql3.connect("movies.db")
cursors = conn.cursor()
lib.database()

while True:
    lib.prt_opt()
    opt = input("請選擇操作選項 (1 ~ 7): ")

    if opt == '1':      #匯入電影資料檔      ok
        lib.funtion_1(conn)
    elif opt == '2':    #2. 查詢            ok
        lib.funtion_2(conn)
    elif opt == '3':    #3. 新增            ok
        lib.funtion_3(conn)
    elif opt == '4':    #4. 修改            ok
        lib.funtion_4(conn)
    elif opt == '5':    #5. 刪除            ok
        lib.funtion_5(conn)
    elif opt == '6' :   #6. 匯出            ok
        lib.funtion_6(conn)
    elif opt == '7':    #7. exit            ok
        conn.close()
        break
