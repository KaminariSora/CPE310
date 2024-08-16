import json
import random
from difflib import get_close_matches
from typing import List, Optional, Dict

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

def ChatBot():
    knowledge: dict = loadInformationFile('Assignment1_Chatbot/Information.json')
    while True:
        user_input: str = input("User : ")
        if user_input.lower() in ['quit', 'exit']:
            break

        best_match: str | None = findMatch(user_input, [q["question"] for q in knowledge["question"]])
        if best_match:
            answer: str = getAnswer(best_match, knowledge)
            print(f"Bot : {answer}")
        else: 
            notice = "I don't know the answer"
            print(f"Bot : {notice}")
            new_answer = str = input("Teach new answer or 'skip' to skip: ")
            if new_answer.lower() != 'skip':
                knowledge["question"].append(
                    {
                        "question" : user_input,
                        "answer" : new_answer
                    }
                )
                saveInformation('Assignment1_Chatbot/Information.json', knowledge)
                print("Bot : Thank you for teaching meʕ•́ᴥ•̀ʔっ")

if __name__ == '__main__':
    ChatBot()