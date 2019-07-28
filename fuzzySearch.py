import pandas as pd
import difflib
import json
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='./templates')
@app.route("/search", methods=['GET'])
def fuzzySearch():
    search_word = request.args.get('word') #read query string from here
    temp_df = pd.DataFrame()
    data_frame = pd.read_csv("word_search.tsv", sep='\t', names=["word", "count"]) #Read .tsv file through pandas function
    data_frame["word"] = data_frame["word"].apply(lambda x: str(x)) #Here I converted word list to string
    searched_data_frame = difflib.get_close_matches(search_word, data_frame["word"], n=25) #Searched close matches of given word and resolved constraint 1 and 2(a, b)
    temp_df["word"] = searched_data_frame
    count = []
    for item in searched_data_frame: #In this for loop I resolved the constraint 2(b). I get the index of top 25 search result and according to that take count and sort it.
        index = searched_data_frame.index(item)
        freq = data_frame["count"][index]
        count.append(freq)
    temp_df["count"] = count
    temp_df = temp_df.sort_values(["count"], ascending = False)
    return temp_df['word'].to_json(orient='records') #Final json result of top 25 word



@app.route("/", methods=['GET'])
def home_page():
    return render_template('index.html') #HTML template of search home page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)