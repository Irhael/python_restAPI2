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