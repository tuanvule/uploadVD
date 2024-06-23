from flask import Flask, request
import webbrowser
import os
from io import StringIO
import traceback
import sys
import time
import json
from timeout_decorator import timeout
from tool import valid_move, distance
# import datetime

# import cv2

@timeout(1)
def safe_exec(code, input, locals):
    exec(code, {"valid_move": valid_move, "distance": distance}, locals)
    func_to_del = ['eval', 'exec', 'input', '__import__', 'open']
    backup_builtins = {func:__builtins__.__dict__[func] for func in func_to_del}

    for func in func_to_del:
        del __builtins__.__dict__[func]

    oup = locals["main"](*input)

    for func, impl in backup_builtins.items():
        __builtins__.__dict__[func] = impl

    return oup

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
            Uoutput = safe_exec(code, i["input"], ldict)
            end = time.time()
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
                    "runtime" : (end-start) * 10**3
                })
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
            Uoutput = safe_exec(code, i["input"], ldict)
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

    compile_date["update_data"] = {
        "code": code,
        "status": status,
        "test_finished": f"{soAc}/{len(user_output)}",
        "submit_time": res["time"],
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

# if __name__ == '__main__':
#     open_browser = lambda: webbrowser.open_new("http://127.0.0.1:4000")
#     app.run(port=4000, debug=True, use_reloader=False)