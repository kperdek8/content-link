import mysql.connector
from flask import Flask, jsonify, request
from cfg.config import Config
#from recommendation_algorithm import get_recommendations

# Generating app's configuration
app_config = Config().config

app = Flask(app_config.APP_NAME)

articles: list = []
article_tags: dict[str, list] = {}


def get_articles() -> list:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT post_name FROM post_tag"
            cursor.execute(query)
            articles = cursor.fetchall()
    return [article[0] for article in articles]


def get_article_tags(article: str) -> list:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT name FROM post_tag WHERE post_name = '{article}'"
            cursor.execute(query)
            tags = cursor.fetchall()
    return [tag[0] for tag in tags]


def get_recommendations(user_data: dict) -> list:
    recommendations = [3, 1, 2]
    return recommendations


def check_if_user_exists(user_id: str) -> bool:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT EXISTS (SELECT * FROM user_interactions where user_id = '{user_id}')"
            cursor.execute(query)
            exists = cursor.fetchone()[0]
    return exists


def read_user_data(user_id: str) -> list:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT user_interactions.post_name FROM user_interactions where user_id = '{user_id}'"

            cursor.execute(query)
            user_data = cursor.fetchall()
    return [interaction[0] for interaction in user_data]


def init():
    global articles, article_tags
    articles = get_articles()
    for article in articles:
        article_tags[article] = get_article_tags(article)


@app.route("/get_recommendations/<user_id>", methods=["GET"])
def process_request(user_id: str):
    if not check_if_user_exists(user_id):
        return jsonify({"error": "user_does_not_exist"}), 404
    user_data = read_user_data(user_id)
    # For testing purpose
    return jsonify(user_data), 200
    ################################
    recommendations = get_recommendations(user_data)
    return jsonify(recommendations), 200


# Start using python app.py
if __name__ == '__main__':
    app.run()
    init()
# Start using flask run
else:
    init()
