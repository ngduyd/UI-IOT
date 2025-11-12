import os
import logging
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Tạo và trả về một kết nối đến database PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        return conn
    except Error as e:
        logging.error(f"Lỗi khi kết nối tới database PostgreSQL: {e}")
        return None

def init_db():
    """Khởi tạo các bảng cần thiết trong database nếu chúng chưa tồn tại."""
    conn = get_db_connection()
    if conn is None:
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensors (
                    sensor_id SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL,
                    vbat DOUBLE PRECISION,
                    status VARCHAR(20),
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS values (
                    id BIGSERIAL PRIMARY KEY,
                    sensor_id INT REFERENCES sensors(sensor_id) ON DELETE CASCADE,
                    type VARCHAR(20),
                    value DOUBLE PRECISION,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
            """)
            conn.commit()
            logging.info("Database đã được khởi tạo thành công.")
    except Exception as e:
        logging.error(f"Lỗi khi khởi tạo database: {e}")
    finally:
        conn.close()

def add_sensor(name: str) -> bool:
    """
    Thêm một sensor mới vào database nếu tên chưa tồn tại.
    Trả về True nếu thành công, False nếu có lỗi.
    """
    if not name:
        logging.warning("Tên sensor không được để trống.")
        return False

    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO sensors (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET status = (%s), updated_at = NOW();",
                (name, "online")
            )
            conn.commit()
            logging.info(f"Sensor '{name}' đã được thêm hoặc đã tồn tại.")
            return True
    except Error as e:
        if conn:
            conn.rollback()
        logging.error(f"Lỗi database khi thêm sensor '{name}': {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_all_sensors() -> list[dict]:
    """
    Truy vấn và trả về danh sách tất cả các sensor trong database.
    Mỗi sensor là một dictionary.
    """
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return []

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT sensor_id, name, vbat, status, updated_at FROM sensors ORDER BY name;")
            sensors = cur.fetchall()
            return sensors
    finally:
        if conn:
            conn.close()

def get_sensor_data(sensor_id: int, limit: int) -> list[dict]:
    """
    Truy vấn và trả về dữ liệu của một sensor cụ thể, được giới hạn bởi số lượng.
    Mỗi điểm dữ liệu là một dictionary được nhóm theo timestamp.
    """
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return []

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # First, get the last 'limit' distinct timestamps for the sensor
            cur.execute("""
                SELECT DISTINCT created_at 
                FROM values 
                WHERE sensor_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (sensor_id, limit))
            timestamps = [row['created_at'] for row in cur.fetchall()]

            if not timestamps:
                return []

            # Now, fetch all the value rows for these specific timestamps
            cur.execute("""
                SELECT created_at, type, value 
                FROM values 
                WHERE sensor_id = %s AND created_at = ANY(%s)
                ORDER BY created_at DESC
            """, (sensor_id, timestamps))
            
            rows = cur.fetchall()
            
            # Group rows by timestamp into dictionaries
            data_by_timestamp = {}
            for row in rows:
                ts = row['created_at']
                if ts not in data_by_timestamp:
                    # Format timestamp for display
                    data_by_timestamp[ts] = {'timestamp': ts.strftime('%Y-%m-%d %H:%M:%S')}
                data_by_timestamp[ts][row['type']] = row['value']
            
            # Return the list of dictionaries
            return list(data_by_timestamp.values())

    except Error as e:
        logging.error(f"Lỗi database khi lấy dữ liệu sensor: {e}")
        return []
    finally:
        if conn:
            conn.close()