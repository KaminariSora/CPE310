import json
import random
from difflib import get_close_matches
from typing import List, Optional, Dict

#kla
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

access_token = "J1HFcSzYDnwyuTeV8TAWW7WIkhBxx/lYIokmBdDxMb2zqrh1ECJ9vxipVejdBinDja4T1Vn9n4ikl5lGFG1APHXi9b4GHbX3Hteyjq4FpO/7Qi/ax03Igx3rvWS0Cz6z/dEcd+MppS/ASjMh7XtdRAdB04t89/1O/w1cDnyilFU="  # Copy Channel access token here


def loadInformationFile(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file) # load data จาก json
    return data

def saveInformation(file_path: str, data: str):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2) # เขียนข้อมูลลง json

def findMatch(user_question: str, question: list[str]) -> Optional[str]:
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

def getAnswer(question: str, knowledge: Dict[str, List[Dict[str, str]]]) -> Optional[str]:
    for item in knowledge["question"]:
        if isinstance(item["question"], list):
            for q in item["question"]:
                if q.lower() == question.lower():
                    return random.choice(item["answer"]) if isinstance(item["answer"], list) else item["answer"]
        else:
            if item["question"].lower() == question.lower():
                return random.choice(item["answer"]) if isinstance(item["answer"], list) else item["answer"]
    return None

def reply_msg(array_header, array_post_data):
    url = "https://api.line.me/v2/bot/message/reply"
    response = requests.post(url, headers=array_header, json=array_post_data)
    return response.json()

def ChatBot(User_Input,reply_token):
    knowledge: dict = loadInformationFile('Assignment1_Chatbot/Information.json')
    user_input: str = User_Input # type: ignore

    best_match: str | None = findMatch(user_input, [q["question"] for q in knowledge["question"]]) # type: ignore
    if best_match:
        answer: str = getAnswer(best_match, knowledge) # type: ignore
        print(f"Bot : {answer}")
    # else: 
    #     answer = "I don't know the answer \nTeach new answer or 'skip' to skip: "

        # print(f"Bot : {answer}")
        # new_answer = str = User_Input
        # if new_answer.lower() != 'skip':
        #     knowledge["question"].append(
        #         {
        #             "question" : user_input,
        #             "answer" : new_answer
        #         }
        #     )
        #     saveInformation('Assignment1_Chatbot/Information.json', knowledge)
        #     print("Bot : Thank you for teaching meʕ•́ᴥ•̀ʔっ")

    array_post_data = {
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": answer
                }
            ]
        }
    
    return array_post_data

@app.route("/", methods=['POST'])
def webhook():
    content = request.get_json()
    array_header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    message = content['events'][0]['message']['text']
    reply_token = content['events'][0]['replyToken']

    # print("message:",message)
    print(content)
    # print("reply_token:",reply_token)

    array_post_data = ChatBot(message,reply_token)
    # print(array_post_data)
    reply_msg(array_header, array_post_data)
    return "OK", 200

if __name__ == '__main__':
    app.run(port=8080)