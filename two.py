import flask
from typing import List, Dict, Any
from flask import request

from models.food import Food
from models.user import User
from mongo_utils import users_collection, foods_collection

app = flask.Flask(__name__)


def calculate_bill_split(
    foods: List[Food], users: List[User]
) -> List[Dict[str, float]]:
    user_to_people_bill: Dict[str, float] = {}

    for user in users:
        user_to_people_bill[user.name] = 0

    for food in foods:
        price_for_each: float = food.price / len(food.list_of_people)
        for people in food.list_of_people:
            user_to_people_bill[people.strip()] += price_for_each

    return [{user: bill} for user, bill in user_to_people_bill.items()]


@app.route("/two", methods=["POST", "GET"])
def food() -> Dict[str, Any]:
    """
    input: Dict[str, str] = {
        "message": "food1,price1,user1,user2,user3"
    }

    terminating_input: Dict[str, str] = {
        "message": "done"
    }

    intermediate_response: Dict[str, str] = {
        "message": "Input the food you bought, separated by commas in this format: food,price,person1,person2,person3",
        "next": "/two"
    }

    final_response: Dict[str, str] = {
        "message": [
            {
                "zheng yang": "bill splitted"
            },
            {
                "clement": "bill splitted"
            }
        ]
    }
    """

    input: Dict[str, str] = request.json
    message: str = input["message"]

    if message == "done":
        users: List[User] = [
            User.parse_obj(user_dict) for user_dict in users_collection.find()
        ]
        foods: List[Food] = [
            Food.parse_obj(food_dict) for food_dict in foods_collection.find()
        ]
        bill_split: List[Dict[str, float]] = calculate_bill_split(foods, users)
        return {"message": bill_split}
    else:
        list_of_inputs: List[str] = message.split(",")
        food_name: str = list_of_inputs[0]
        food_price: float = float(list_of_inputs[1])
        list_of_people: List[str] = list_of_inputs[2:]
        food: Food = Food(name=food_name, price=food_price, list_of_people=list_of_people)
        foods_collection.insert_one(food.dict())
        return {
            "message": "Input the food you bought, separated by commas in this format: food,price,person1,person2,person3",
            "next": "/two",
        }


if __name__ == "__main__":
    app.run(port=3001,debug=True)