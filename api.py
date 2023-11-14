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

#Create video by id
@app.route('/video/<int:video_id>', methods=['POST'])
def create_video(video_id):
    data = request.get_json()
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO videos (id, name, views, likes) VALUES (%s, %s, %s, %s)',
                       (video_id, data['name'], data['views'], data['likes']))
        connection.commit()
    return jsonify({'message': 'Video created successfully'}), 201

# Update video by id
@app.route('/video/<int:video_id>', methods=['PATCH'])
def update_video(video_id):
    data = request.get_json()
    with connection.cursor() as cursor:
        # Atualiza apenas as informações fornecidas no JSON
        update_query = 'UPDATE videos SET '
        update_query += ', '.join(f'{key} = %s' for key, value in data.items())
        update_query += ' WHERE id = %s'

        cursor.execute(update_query, [value for key, value in data.items()] + [video_id])
        connection.commit()
    return jsonify({'message': 'Video updated successfully'})

# Delete video by id
@app.route('/video/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    data = request.get_json()
    
    with connection.cursor() as cursor:
        # Verifica se o vídeo existe
        cursor.execute('SELECT * FROM videos WHERE id = %s', (video_id,))
        video = cursor.fetchone()
        if not video:
            return jsonify({'message': 'Video not found'}), 404
        
        # Atualiza apenas as informações fornecidas no JSON
        update_query = 'UPDATE videos SET '
        update_query += ', '.join(f'{key} = NULL' for key in data.keys())
        update_query += ' WHERE id = %s'

        cursor.execute(update_query, [video_id])
        connection.commit()

    return jsonify({'message': f'Specific parts of Video with ID {video_id} deleted successfully'})