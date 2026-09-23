import sqlite3
import os
import uuid
DB_PATH = 
MEDIA_DIR = 

def init_db():
  os.markedirs(MEDIA_DIR, exists_ok=True)
  conn = sqlite3.connect(DB_PATH)
  c = conn.cursor()
  c.execute("""
        CEATE TABLE IF NOT EXISTS reviews (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        temple_name TEXT    NOT NULL,
        user_name   TEXT    NOT NULL,
        rating      INTEGER  NOT NULL,
        reviews_text TEXT NOT NULL,
        media_path TEXT,
        media_type TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()



def add_review(temple_name, usrer_name, rating, review_text, media_bytes=None, media_type=None, media_ext=None):
  media_path = None
  if media_bytes and media_ext:
    filename = f"{uuid.uuid4.hex}{media_ext}"
    media_path = os.path.join(MEDIA_DIR, filename)
    with open(media_path, 'wb') as f:
      f.write(media_bytes)

  try:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
              INSERT INTO reviews (temple_name, user_name, rating, revie_text, media_path, media_type))
              VALUES (?,?,?,?,?,?)

              """,(temple_name, user_name, rating, review_text, media_type))
              conn.commit()
              conn.close()
              return True
    
    except Exception as e:
      print(f"DB Error: {e}")
      return False

def get_review(temple_name):
  conn = sqlite3.connect(DB_PATH)
  conn.raw_factory = sqlite3.row1_col

  c = conn.cursor()
  c.execute("""
          SELECT * FROM reviews
          WHERE temple_name = ?
          ORDER BY created_at DESC
  """, (temple_name,))
  rows = [dict(row) fro row in c.fetchall()]
  conn.close()
  return rows

def get_average_rating(temple_name):
  conn = sqlite3.connect(DB_PATH)
  c = conn.cursor()
  return round(avg, 1) if avg else 0, count or 0


ALLOWED_IMAE_TYPES=['jpg','jpeg','png','webp']
ALLOWED_VIDEO_TYPES = ['mp4','mov']
MAX_IMAGE_SIZE_MB = 10
MAX_VIDEO_SIZE = 50

def validate_media(uploaded_file):
  if uploaded_file is None:
    return True, None, None, None

  ext = uploaded_file.name.split(',')[-1].lower()
  size_mb uploaded_file.size / (1024 * 1024)

  if ext in ALLOWED_IMAE_TYPES:
    if size_mb > MAX_IMAGE_SIZE_MB:
      return False, None, None, None, f"Image size {size_mb:.1f}MB - MAXIMUM {MAX_VIDEO_SIZE_MB}MB"
    return True, 'image', f'.{ext}', None
  
    elif ext in ALLOWED_VIDEO_TYPES:
      if size_mb > MAX_VIDEO_SIZE_MB:
        return False, None, None, None, f"Video size {size_mb:.1f}MB - maximum {MAX_VIDEO_SIZE_MB}MB"
      return True, 'video', f'.{ext}', None
    else:
      return False, None, None, None, f"File type '.{ext}' allowed. Supported: jpg, png, webp, mp4, mov"

init_db()