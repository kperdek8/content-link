import mysql.connector
from flask import Flask, jsonify, request
from cfg.config import Config
from recommendation_algorithm import get_recommendations, load_semantic_map

# Generating app's configuration
app_config = Config().config

app = Flask(app_config.APP_NAME)

articles: list = []
article_tags: dict[str, list] = {}
tags: list = []
semantic_map: dict = {}


def get_articles() -> list:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT post_name FROM post_tag"
            cursor.execute(query)
            articles = cursor.fetchall()
    return [article[0] for article in articles]


def get_tags() -> list:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT DISTINCT name FROM post_tag"
            cursor.execute(query)
            tags = cursor.fetchall()
    return [tag[0] for tag in tags]


def get_article_tags(article: str) -> list:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT name FROM post_tag WHERE post_name = '{article}'"
            cursor.execute(query)
            tags = cursor.fetchall()
    return [tag[0] for tag in tags]


def check_if_user_exists(user_id: str) -> bool:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT EXISTS (SELECT * FROM user_interactions where user_id = '{user_id}')"
            cursor.execute(query)
            exists = cursor.fetchone()[0]
    return exists


def read_user_data(user_id: str) -> dict:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT user_interactions.post_name FROM user_interactions where user_id = '{user_id}'"

            cursor.execute(query)
            user_data = cursor.fetchall()
    return {user_id: [interaction[0] for interaction in user_data]}


def init():
    global articles, article_tags, tags, semantic_map
    tags = get_tags()
    articles = get_articles()
    semantic_map_file_path = './somatic_map.csv'
    semantic_map = load_semantic_map(semantic_map_file_path)
    for article in articles:
        article_tags[article] = get_article_tags(article)


@app.route("/get_recommendations/<user_id>", methods=["GET"])
def process_request(user_id: str):
    if not check_if_user_exists(user_id):
        return jsonify({"error": "user_does_not_exist"}), 404
    user_data = read_user_data(user_id)

    # Load the semantic map
    recommendations = get_recommendations(user_id, article_tags, user_data, semantic_map)
    return jsonify(recommendations), 200


# Start using python app.py
if __name__ == '__main__':
    app.run()
    init()
# Start using flask run
else:
    init()
