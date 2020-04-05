from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
from google.oauth2 import service_account
from googleapiclient.discovery import build
import sys

app = Flask(__name__)
CORS(app)

#For WSGI Purposes
application = app


@app.route('/questions', methods=['GET'])
def get_questions():
    with open('questions.json', 'r') as question_file :
        data = question_file.read()

        # parse file
        obj = json.loads(data)
        questions = [x['q'] for x in obj['questions']]
    
        return jsonify(questions)

@app.route('/answers', methods=['POST'])
def post_answers():
    with open('questions.json', 'r') as json_file:
        #get questions
        data = json_file.read()
        obj = json.loads(data)
        questions = obj['questions']
    
        #Parse requests 
        body = request.json
        
        answers = body['answers']

        #Check if user answerd all true or not
        if (all([x == 5 for x in answers]) or all([x == 0 for x in answers]) ) :
            return jsonify({
                'suggestion': "It's still too tricky to find your shade of blue..."
            })

        else :
            array_of_panitia = obj['divisions']
            array_of_score = [0 for i in range(len(array_of_panitia))] 
            score_map = dict(zip(array_of_panitia,array_of_score))

            #code to count answer
            for key,question in zip(answers,questions) :

                #Get result
                result = answers[key] 
                
                #find out what type it is
                if (question['type'] == 'single') :
                    score_map[question['choices'][result]] += 1

                elif (question['type'] == 'range'):
                    score_map[question['target']] += result

        
            max_score = max(score_map)
            list_of_max = [key for key in score_map if score_map[key]==score_map[max_score]]
            # for maximum in list_of_max :
                # print(maximum, file=sys.stdout, flush=True)
            if (len(list_of_max) > 3) : 
                #Sort the suggestions
                suggestions = [key for key in score_map if score_map[key]==score_map[max_score]]
                random.shuffle(suggestions)                    
                suggestions_containing_only_3_items = suggestions[0:3]

            else : 
                suggestions_containing_only_3_items = list(sorted(score_map, key=score_map.get, reverse=True))[:3]

            return jsonify({
                'suggestion': suggestions_containing_only_3_items
            })


if __name__ == '__main__':
    app.run(debug=True)
    
