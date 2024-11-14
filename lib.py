import json
import sqlite3 as sql3

#選單
def prt_opt():
    print("---電影管理系統---")
    print("1. 匯入電影資料檔")
    print("2. 查詢電影")
    print("3. 新增電影")
    print("4. 修改電影")
    print("5. 刪除電影")
    print("6. 匯出電影")
    print("7. 離開系統")
    print("-------------------------------")

#資料庫
def database():
    conn = sql3.connect("movies.db")
    cursors = conn.cursor()
    cursors.execute(
        '''CREATE TABLE IF NOT EXISTS movies (

                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                director TEXT NOT NULL,
                genre TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL CHECK(rating >= 1.0 AND rating <= 10.0)

        )'''
    )

#1. 匯入
def funtion_1(conn):
    cursors = conn.cursor()
    try:
        with open('c:\\mypy\\HW_3rd\\movies.json', 'r', encoding='UTF-8') as mj:
            data = json.load(mj)
            #寫入資料至SQLite
            for i in data:
                cursors.execute("INSERT INTO movies (title, director, genre, year, rating) VALUES (?, ?, ?, ?, ?)", (i["title"], i["director"], i["genre"], i["year"], i["rating"]))
            conn.commit()
            print("電影已匯入\n")
            # print(datas)
    except FileNotFoundError :
        print("\n找不到檔案\n")
    except Exception as e:
        print(f'發生其它錯誤 {e}')

#2. 查詢
def funtion_2(conn):
    cursors = conn.cursor()
    while True:
        searall = input("查詢全部電影嗎?(y/n) ")

        #印出所有資料
        if searall == 'y' or searall == 'Y':
            cursors.execute('SELECT * FROM movies')
            result_all = cursors.fetchall() #獲取所有資料
            print('所有資料：')
            print(type(result_all))

            print(f"id{'':{chr(12288)}<3} 電影名稱{'':{chr(12288)}<6} 導演{'':{chr(12288)}<8} 類型{'':{chr(12288)}<3} 上映年份{'':{chr(12288)}<4} 評分(1.0~10.0)")
            print("-" * 30)

            for i in result_all:
                print(f"{i[0]:{chr(12288)}<5} {i[1]:{chr(12288)}<10} {i[2]:{chr(12288)}<10} {i[3]:{chr(12288)}<5} {i[4]:{chr(12288)}<10} {i[5]}")
            break
        #印出所選資料
        elif searall == 'n' or searall == 'N':
            moviemn = input("請輸入電影名稱: ")
            cursors.execute("SELECT title, director, genre, year, rating FROM movies WHERE title LIKE ?", ('%' + moviemn + '%',))
            results = cursors.fetchall()
            if results:
                print(f"{'電影名稱':{chr(12288)}<10} {'導演':{chr(12288)}<10} {'類型':{chr(12288)}<10} {'年份':{chr(12288)}<10} {'評分':{chr(12288)}<10}")
                print('-' * 40)
                for row in results:
                    print(f"{row[0]:{chr(12288)}<10} {row[1]:{chr(12288)}<10} {row[2]:{chr(12288)}<10} {row[3]:{chr(12288)}<10} {row[4]:{chr(12288)}<10}")
                break
            else:
                print("找不到符合條件的電影。")
                break
        else :
            print("\n無效輸入\n")

#3. 新增
def funtion_3(conn):
    cursors = conn.cursor()

    movies = input("電影名稱: ")
    dirtr = input("導演: ")
    types = input("類型: ")
    years = input("上映年分: ")
    scores = float(input("評分 (1.0 - 10.0):"))
    try:
        cursors.execute("INSERT INTO movies (title, director, genre, year, rating) VALUES (?, ?, ?, ?, ?)", (movies, dirtr, types, years, scores))
        conn.commit()
        print("\n電影已新增\n")
    except sql3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")
    except Exception as e:
        print(f'發生其它錯誤 {e}')

#4. 修改
def funtion_4(conn):
    cursor = conn.cursor()

    # 輸入要修改的電影名稱
    exprmn = input("請輸入要修改的電影名稱: ")

    try:
        cursor.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + exprmn + '%',))
        results = cursor.fetchall()

        if results:
            # 顯示查詢結果
            print(f"{'電影名稱':{chr(12288)}<10} {'導演':{chr(12288)}<10} {'類型':{chr(12288)}<10} {'年份':{chr(12288)}<10} {'評分':{chr(12288)}<10}")
            print('-' * 40)
            for row in results:
                print(f"{row[0]:{chr(12288)}<10} {row[1]:{chr(12288)}<10} {row[2]:{chr(12288)}<10} {row[3]:{chr(12288)}<10} {row[4]:{chr(12288)}<10}")

            movie_id = results[0][0]

            netitle  = input("請輸入新的電影名稱 (若不修改請直接按 Enter): ")
            nedire = input("請輸入新的導演 (若不修改請直接按 Enter): ")
            negen = input("請輸入新的類型 (若不修改請直接按 Enter): ")
            neyear = input("請輸入新的上映年份 (若不修改請直接按 Enter): ")
            nerat = input("請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter): ")

            # 生成更新語句，僅對輸入值不為空的欄位進行更新
            updates = []
            values = []

            if netitle:
                updates.append("title = ?")
                values.append(netitle)
            if nedire:
                updates.append("director = ?")
                values.append(nedire)
            if negen:
                updates.append("genre = ?")
                values.append(negen)
            if neyear:
                updates.append("year = ?")
                values.append(int(neyear))
            if nerat:
                values.append(float(nerat))
                updates.append("rating = ?")

            # 更新資料
            if updates:
                sql = f"UPDATE movies SET {', '.join(updates)} WHERE id = ?"
                values.append(movie_id)
                cursor.execute(sql, values)
                conn.commit()
                print("資料已修改")
            else:
                print("未進行任何修改。")

        else:
            print("找不到符合條件的電影。")

    except Exception as e:
        print(f'發生錯誤: {e}')

#5. 刪除
def funtion_5(conn):
    cursors = conn.cursor()
    delme = input("刪除全部電影嗎？(y/n): ")
    while True:
        if delme == 'y' or delme == 'Y':
            cursors.execute('DELETE FROM movies ')
            conn.commit()
            break
        elif delme == 'n' or delme == 'N':
            exprmn = input("請輸入要刪除的電影名稱: ")
            try:
                cursors.execute("SELECT title, director, genre, year, rating FROM movies WHERE title LIKE ?", ('%' + exprmn + '%',))
                results = cursors.fetchall()
                if results:
                    # 顯示找到的電影資料
                    print("找到以下電影資料：")
                    for row in results:
                        print(row)
                    # 確認是否刪除
                    confirm = input("確定要刪除這些電影嗎？(y/n): ")
                    if confirm.lower() == 'y':
                        cursors.execute("DELETE FROM movies WHERE title LIKE ?", ('%' + exprmn + '%',))
                        conn.commit()
                        print("指定的電影資料已刪除。")
                    else:
                        print("取消刪除操作。")
                else:
                    print("找不到符合條件的電影。")
                break
            except Exception as e:
                print(f'發生錯誤: {e}')
                break
        else:
            print("無效輸入")
            break



#6. 匯出
def funtion_6(conn):
    cursors = conn.cursor()
    expr = input("匯出全部電影嗎？(y/n): ")
    while True:
        if expr == 'y' or expr == 'Y':  #全部
            cursors.execute("SELECT title, director, genre, year, rating FROM movies")  # 查詢所有電影資料
            rows = cursors.fetchall()

            columns = ["title", "director", "genre", "year", "rating"]
            data = [dict(zip(columns, row)) for row in rows]

            with open('exported.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print("電影已匯出\n")
            break
        elif expr == 'n' or expr == 'N':    #指定
            exprmn = input("請輸入要匯出的電影名稱: ")
            try:
                cursors.execute("SELECT title, director, genre, year, rating FROM movies WHERE title LIKE ?", ('%' + exprmn + '%',))
                results = cursors.fetchall()
                if results:
                    columns = ["title", "director", "genre", "year", "rating"]
                    data = [dict(zip(columns, row)) for row in results]
                    with open('exported.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii = False, indent=4)
                    print("電影資料已匯出至 exported.json")
                    break
                else:
                    print("找不到檔案...")
                    break
            except FileNotFoundError:
                print('找不到檔案...')
                break
            except Exception as e:
                print(f'發生其它錯誤: {e}')
                break
        else:
            print("無效輸入")
            break
