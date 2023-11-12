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