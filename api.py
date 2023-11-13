from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'irhael',
    'password': 'ELITE31337#',
    'database': 'videos_data',
}

connection = mysql.connector.connect(**db_config)

with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            views INT NOT NULL,
            likes INT NOT NULL
        )
    """)
    connection.commit()

#Return video by id
@app.route('/video/<int:video_id>', methods=['GET'])
def get_video(video_id): 
    with connection.cursor() as cursor: 
        cursor.execute('SELECT * FROM videos WHERE id = %s', (video_id,)) # (video_id,) is a tuple
        video = cursor.fetchone() # fetchone() is a method that returns the first row of the result
    if not video:
        return jsonify({'message': 'Video not found'}), 404
    return jsonify({'id': video[0], 'name': video[1], 'views': video[2], 'likes': video[3]})
