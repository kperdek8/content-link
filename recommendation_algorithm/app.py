from flask import Flask, jsonify, request
from cfg.config import Config
from recommendation_algorithm import recommended_posts

# Generating app's configuration
app_config = Config().config

app = Flask(app_config.APP_NAME)


# TODO: Implement
def get_recommendations(user_data: dict) -> list:
    recommendations = [3, 1, 2]
    return recommendations


# TODO: Implement
def read_user_data(user_id: int) -> dict:
    return {}


@app.route("/get_recommendations/<user_id>", methods=["GET"])
def process_request(user_id: int):
    # TODO: Test if user_id is integer
    user_id = int(user_id)
    user_data = read_user_data(user_id)
    # Dummy function
    recommendations = get_recommendations(user_data)
    # Target function
    # recommendations = recommended_posts()
    return jsonify(recommendations), 200


if __name__ == '__main__':
    app.run()
