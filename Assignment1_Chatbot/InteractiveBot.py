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
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file) # load data จาก json
    return data

def findMatch(user_question: str, question: list[str]) -> Optional[str]:
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

def getAnswer(question: str, knowledge: Dict[str, List[Dict[str, str]]]) -> Optional[str]:
    for item in knowledge["faqs"]:
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

def push_msg(array_header, array_post_data):
    url = "https://api.line.me/v2/bot/message/push"
    response = requests.post(url, headers=array_header, json=array_post_data)
    return response.json()
    
def quick_reply_list():
    knowledge: dict = loadInformationFile('Assignment1_Chatbot/Information.json')
    actions = []
    for idx,question in enumerate(knowledge['faqs']):
        if question["label"] == "skip":
            continue
        elif idx == 13:
            action = {
            "type": "action",
            "action": {
                "type": "message",
                "label": "ต่อไป",
                "text": "ต่อไป"
                }
            }
            actions.append(action)
        else:
            action = {
            "type": "action",
            "action": {
                "type": "message",
                "label": question["label"],
                "text": question["question"]
                }
            }
            actions.append(action)
    
        # print(actions)
    return actions

def ChatBot(User_Input,content):
    knowledge: dict = loadInformationFile('Assignment1_Chatbot/Information.json')
    user_input: str = User_Input # type: ignore

    reply_token = content['events'][0]['replyToken']
    userId = content['events'][0]['source']['userId']

    question_match: str | None = findMatch(user_input, [q["question"] for q in knowledge["faqs"]])


    if question_match:
        answer: str = getAnswer(question_match, knowledge) # type: ignore
        print(f"Bot : {answer}")

        array_post_data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": answer
            }
            ]
        }

    elif user_input == "ตัวเลือก":
        quick_reply_list_1 = quick_reply_list()[0:13]
            
        array_post_data = {
            "to": userId,
            "messages": [
                {
                "type": "text",
                "text": "ตัวเลือก",
                "quickReply": {
                    "items": quick_reply_list_1
                }
                }
            ]
            }
    
    elif user_input == "ต่อไป":
        quick_reply_list_2 = quick_reply_list()[14:]
            
        array_post_data = {
            "to": userId,
            "messages": [
                {
                "type": "text",
                "text": "ตัวเลือก2",
                "quickReply": {
                    "items": quick_reply_list_2
                }
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

    array_post_data = ChatBot(message,content)
    # print(array_post_data)
    # print("message:",message)
    # print(content)

    if message == "ตัวเลือก":
        push_msg(array_header, array_post_data)
        return "OK", 200
    
    elif message == "ต่อไป":
        push_msg(array_header, array_post_data)
        return "OK", 200
    
    else:
        reply_msg(array_header, array_post_data)
        return "OK", 200

if __name__ == '__main__':
    app.run(port=8080)