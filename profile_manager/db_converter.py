import sqlite3

def create_sqlite_from_schema(db_schema, db_instance, db_name="database.db"):
    """
    dictionary schema와 instance로부터 SQLite 데이터베이스를 생성
    
    Args:
        db_schema: dict - 테이블 스키마 정의
        db_instance: list - 테이블에 삽입할 데이터
        db_name: str - 데이터베이스 파일명
    """
    
    # SQLite 연결
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # 각 테이블에 대해 처리
        for table_name, columns in db_schema.items():
            
            # CREATE TABLE 구문 생성
            column_definitions = []
            for col_info in columns:
                if len(col_info) == 3:  # (name, type, constraint)
                    name, data_type, constraint = col_info
                    if constraint.upper() == "PRIMARY":
                        column_def = f"{name} {data_type} PRIMARY KEY"
                    else:
                        column_def = f"{name} {data_type} {constraint}"
                elif len(col_info) == 2:  # (name, type)
                    name, data_type = col_info
                    column_def = f"{name} {data_type}"
                else:
                    raise ValueError(f"잘못된 컬럼 정의: {col_info}")
                
                column_definitions.append(column_def)
            
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
            
            print(f"테이블 생성 SQL: {create_table_sql}")
            cursor.execute(create_table_sql)
            
            # INSERT 구문 생성 및 실행
            if db_instance:
                placeholders = ', '.join(['?' for _ in range(len(columns))])
                insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                
                print(f"데이터 삽입 SQL: {insert_sql}")
                print(f"삽입할 데이터: {db_instance}")
                
                cursor.execute(insert_sql, db_instance)
        
        # 변경사항 커밋
        conn.commit()
        print(f"\n데이터베이스 '{db_name}' 생성 완료")
                
    except Exception as e:
        print(f"오류 발생: {e}")
        conn.rollback()
    
    finally:
        conn.close()

# 사용 예시
if __name__ == "__main__":
    # 주어진 스키마와 인스턴스
    db_schema = {
        "profile": [
            ("uuid", "TEXT", "PRIMARY"), 
            ("name1", "INTEGER"), 
            ("name2", "TEXT")
        ]
    }
    db_instance = ["abc", 1, "def"]
    
    # 데이터베이스 생성
    create_sqlite_from_schema(db_schema, db_instance)