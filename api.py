from flask import Flask, request, jsonify, escape
import mysql.connector
from wtforms import Form, StringField, validators

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
            description TEXT,
            views INT NOT NULL,
            likes INT NOT NULL
        )
    """)
    connection.commit()

# Classe de formulário para validação
class VideoForm(Form):
    name = StringField('name', [validators.Length(min=1, max=100)])
    description = StringField('description')
    views = StringField('views', [validators.NumberRange(min=0)])
    likes = StringField('likes', [validators.NumberRange(min=0)])

# Validate form
def validate_form(form):
    if form.validate(): # Verifica se o formulário é válido
        return True
    else:
        errors = {field.label.text: field.errors for field in form} # Cria um dicionário com os erros
        return jsonify({'message': 'Invalid input', 'errors': errors}), 400  # Bad Request

#Return video by id
@app.route('/video/<int:video_id>', methods=['GET'])
def get_video(video_id): 
    with connection.cursor() as cursor: 
        cursor.execute('SELECT * FROM videos WHERE id = %s', (video_id,)) # (video_id,) is a tuple
        video = cursor.fetchone() # fetchone() is a method that returns the first row of the result
    if not video:
        return jsonify({'message': 'Video not found'}), 404
    video_data = {
        'id': video[0],
        'name': video[1],
        'description': video[2],
        'views': video[3],
        'likes': video[4]
    }
    return jsonify(video_data)
#Create video by id
@app.route('/video/<int:video_id>', methods=['POST'])
def create_video(video_id):
    data = request.get_json()
    form = VideoForm(data=data) # Instancia o formulário com os dados do JSON

    if not validate_form(form):  # Validating form
        return validate_form(form)
    
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO videos (id, name, description, views, likes) VALUES (%s, %s, %s, %s, %s)',
                       (video_id, form.name.data, form.description.data, form.views.data, form.likes.data))
        connection.commit()
    return jsonify({'message': 'Video created successfully'}), 201

# Update video by id
@app.route('/video/<int:video_id>', methods=['PATCH'])
def update_video(video_id):
    data = request.get_json()
    form = VideoForm(data=data)

    if not validate_form(form):
        return validate_form(form)

    with connection.cursor() as cursor:
        # Atualiza apenas as informações fornecidas no JSON
        update_query = 'UPDATE videos SET '
        update_query += ', '.join(f'{key} = %s' for key, value in data.items() if value is not None)
        update_query += ' WHERE id = %s'

        cursor.execute(update_query, [value for key, value in data.items() if value is not None] + [video_id])
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

        # Atualiza apenas as informações fornecidas no JSON para NULL
        update_query = 'UPDATE videos SET '
        update_query += ', '.join(f'{key} = NULL' for key in data.keys())
        update_query += ' WHERE id = %s'

        cursor.execute(update_query, [video_id])
        connection.commit()

    return jsonify({'message': f'Specific parts of Video with ID {video_id} deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)