from flask import Flask, request, render_template
import numpy as np
import pickle
import requests

import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "ULus5QdOLszZH00BRQ4Fkh9RN4bNLxcDRceE9w6Uut9q"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}





app = Flask(__name__)



@app.route("/")
def f(): 
    return render_template("index.html")

@app.route("/inspect")
def inspect():
    return render_template("inspect.html")
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        var1 = float(request.form["AccX"])
        var2 = float(request.form["AccY"])
        var3 = float(request.form["AccZ"])
        var4 = float(request.form["GyroX"])
        var5 = float(request.form["GyroY"])
        var6 = float(request.form["GyroZ"])
        var7 = float(request.form["Timestamp"])
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"field": [['AccX','AccY','AccZ','GyroX','GyroY','GyroZ','Timestamp']], "values": [[var1,var2,var3,var4,var5,var6,var7]]}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/aa45449b-9d09-412a-972f-3edf6e2e55c1/predictions?version=2023-03-10', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        predictions=response_scoring.json()
        predict=predictions["predictions"][0]['values'][0][0]

        if (predict == 0):
            return render_template('output.html', predict="Slow")
        elif (predict == 1):
             return render_template('output.html',predict="Normal")
        else:
            return render_template('output.html', predict="Aggressive")
    return render_template('index.html')



        
if __name__ == "__main__":
    app.run(debug=True)
