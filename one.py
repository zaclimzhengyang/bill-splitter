import flask
from typing import List, Dict
from flask import request

from models.user import User
from mongo_utils import users_collection

app = flask.Flask(__name__)


@app.route("/one", methods=["POST", "GET"])
def people() -> Dict[str, str]:
    """
    users: Dict[str, str] = {
        "message": "user1,user2"
    }
    """
    # parse users_string into users_input
    # "user 1 , user 2,"
    input: Dict[str, str] = request.json
    users_string: str = input["message"]
    list_of_users: List[User] = [
        User(name=user.strip()) for user in users_string.split(",")
    ]
    # insert users_input into users_collection
    users_collection.insert_many([user.dict() for user in list_of_users])
    return {
        "message": "Input the food you bought, separated by commas in this format: food,price,person1,person2,person3",
        "next": "/two",
    }


if __name__ == "__main__":
    app.run(port=3000, debug=True)