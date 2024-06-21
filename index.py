from flask import Flask, request
import webbrowser
import os
from io import StringIO
import traceback
import sys
import time
import json
import datetime

# import cv2

app = Flask(__name__)

absolute_path = os.getcwd()

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/run_compile', methods=["POST"])
def run_compile():
    res = request.get_json()
    code = res["code"]
    inp_oup = res["inp_oup"]
    org_stdout = sys.stdout
    err = ""

    dd = {
        "return_data": {},
        "code": code,
    }

    user_output = []
    for i in inp_oup:
        f = StringIO()
        sys.stdout = f
        try:
            ldict = {}
            start = time.time()
            exec(code, {}, ldict)
            end = time.time()
            Uoutput = ldict["main"](*i["input"])
            Uoutput = json.loads(json.dumps(Uoutput).replace("(","[").replace(")","]"))
            if type(Uoutput) is list:
                comparision = sorted(i["output"]) == sorted(Uoutput)
            else:
                comparision = i["output"] == Uoutput
            if comparision:
                user_output.append({
                    # "log": f.getvalue(),
                    "output_status" : "AC",
                    "output" : Uoutput,
                    "runtime" : (end-start) * 10**3
                })
            else:
                user_output.append({
                    # "log": f.getvalue(),
                    "output_status" : "WA",
                    "output" : Uoutput
                })
        except:
            err = traceback.format_exc()
            user_output.append({
                # "log": f.getvalue(),
                "output_status" : "SE",
            })
    sys.stdout = org_stdout

    if any(i["output_status"]=="SE" for i in user_output):
        status = "SE"
    elif any(i["output_status"]=="WA" for i in user_output):
        status = "WA"
    else:
        status = "AC"

    if err:
        return_data = {
            "status": "SE",
            "output": [i["output"] for i in inp_oup],
            "err": err,
        }
    else:
        return_data = {
            "status": status,
            "output": [i["output"] for i in inp_oup],
            "user_output": user_output,
        }

    # print(return_data)

    dd["return_data"] = return_data

    return dd

@app.route('/submit_compile', methods=['POST'])
def submit_compile():
    res = request.get_json()

    compile_date = {
        "update_data": {

        },

        "return_data": {

        }
    }

    code = res["code"]
    inp_oup = res["inp_oup"]
    org_stdout = sys.stdout
    soAc = 0
    err = ""

    user_output = []
    start = time.time()
    for i in inp_oup:
        f = StringIO()
        sys.stdout = f
        try:
            ldict = {}
            exec(code, {}, ldict)
            Uoutput = ldict["main"](*i["input"])
            Uoutput = json.loads(json.dumps(Uoutput).replace("(","[").replace(")","]"))
            if type(Uoutput) is list:
                comparision = sorted(i["output"]) == sorted(Uoutput)
            else:
                comparision = i["output"] == Uoutput

            if comparision:
                user_output.append({
                    "log": f.getvalue(),
                    "output_status" : "AC",
                    "output" : Uoutput,
                })
                soAc+=1
            else:
                user_output.append({
                    "log": f.getvalue(),
                    "output_status" : "WA",
                    "output" : Uoutput
                })
        except:
            err = traceback.format_exc()
            user_output.append({
                "log": f.getvalue(),
                "output_status" : "SE",
            })
    end = time.time()
    sys.stdout = org_stdout

    if any(i["output_status"]=="SE" for i in user_output):
        status = "SE"
    elif any(i["output_status"]=="WA" for i in user_output):
        status = "WA"
    else:
        status = "AC"

    now = datetime.datetime.now()

    date_string = now.strftime("%d/%m/%Y")

    compile_date["update_data"] = {
        "code": code,
        "status": status,
        "test_finished": f"{soAc}/{len(user_output)}",
        "submit_time": date_string,
        "run_time": (end-start) * 10**3,
    }

    if err:
        compile_date["return_data"] = {
            "status": "SE",
            "output": [i["output"] for i in inp_oup],
            "err": err,
        }
    else:
        compile_date["return_data"] = {
            "status": status,
            "output": [i["output"] for i in inp_oup],
            "user_output": user_output,
            "test_finished": f"{soAc}/{len(user_output)}",
            "run_time": (end-start) * 10**3,
        }

    return compile_date
@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    open_browser = lambda: webbrowser.open_new("http://127.0.0.1:4000")
    app.run(port=4000, debug=True, use_reloader=False)
