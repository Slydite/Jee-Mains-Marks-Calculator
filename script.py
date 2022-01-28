from bs4 import BeautifulSoup
import csv
#load the file for chosen answers
choices_soup = BeautifulSoup(open('./chosen.html'), 'html.parser')

question_panel_tables = choices_soup.find_all("table", class_="questionPnlTbl")

choices = {}

for qpt in question_panel_tables:
    qpbody = qpt.tbody
    cbody = qpbody.find("table", class_="menu-tbl").tbody
    qbody = qpbody.find("table", class_="questionRowTbl").tbody

    ques_id = cbody.contents[1].find("td", class_="bold").string.strip()

    if len(cbody.contents) == 8: # mcq
        chosen = cbody.contents[7].find("td", class_="bold").string.strip()
        
        if chosen != "--":
            chosen_id = cbody.contents[int(chosen)+1].find("td", class_="bold").string.strip()
            print(f"ans: {chosen_id}")
        else:
            print("no ans")
            chosen_id = None

        choices[ques_id] = chosen_id
    elif len(cbody.contents) == 3: # int
        chosen = qbody.contents[4].find("td", class_="bold").string.strip()
        
        if chosen == "--":
            print("no ans")
            chosen = None
        else:
            print(f"ans: {chosen}")

        choices[ques_id] = chosen
    else:
        raise ValueError("unknown question type")

#load the file for correct answers
table_id = "ctl00_LoginContent_grAnswerKey"


answers_soup = BeautifulSoup(open('./answers.html'), 'html.parser')

answers_table = answers_soup.find("table", id=table_id).tbody

answers = {}

for row in answers_table.find_all("tr"):
    cols = row.find_all("span")
    if len(cols) >= 3:
        ques_id = cols[1].string
        answer_id = cols[2].string
        answers[ques_id] = answer_id
        print(f"expect ans: {answer_id}")

print("ANSWERS:")
score = 0
correct = 0
incorrect = 0
unanswered = 0
for q,a in answers.items():
    print(f"{choices[q]} , {a}", end="")
    if a == choices[q]:
        score += 4
        correct += 1
        print(", correct")
    elif choices[q] == None:
        unanswered += 1
        print(", unattempted")
    else:
        if(int(a)>100000000):
          score -= 1
          incorrect += 1
          print(", incorrect")
        else:
          incorrect += 1
          print(", incorrect")

print("Score: {}".format(score))
print("Correct: {}, Incorrect: {}, Unanswered: {}".format(correct, incorrect, unanswered))


