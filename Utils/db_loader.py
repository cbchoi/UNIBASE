import sqlite3

# DB 파일 연결 (없으면 자동 생성)
conn = sqlite3.connect('example.db')

# 커서(cursor) 객체 생성
cur = conn.cursor()