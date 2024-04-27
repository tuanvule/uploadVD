from flask import Flask, request
# import moviepy.editor as mpe
# from PIL import Image, ImageDraw
# import numpy as np
import os
# import fdb.firestore_config
# from fdb.uti.upload import upload_video_to_storage
# import webbrowser
import cv2

app = Flask(__name__)

absolute_path = os.getcwd()

# print("___", absolute_path, "____")

# def declare():
#     global positions, point, frame, video

#     positions = [None,
#                 [(0,2), (0,3), (4,3), (0,4), (1,4), (2,4), (3,4), (4,4)],
#                 [(0,0), (1,0), (2,0), (3,0), (4,0), (0,1), (4,1), (4,2)]]

#     point = []

#     frame = Image.open(absolute_path + "/chessboard.png")
#     frame_cop = frame.copy()
#     draw = ImageDraw.Draw(frame_cop)

#     for x, y in positions[1]:
#         draw.ellipse((x*100+80, y*100+80, x*100+120, y*100+120), fill="blue", outline="blue")
#     for x, y in positions[-1]:
#         draw.ellipse((x*100+80, y*100+80, x*100+120, y*100+120), fill="red", outline="red")

#     frame_cop = np.array(frame_cop)
#     video = [mpe.ImageClip(frame_cop).set_duration(1)]

# declare()

# def generate_image(positions, move, remove):
#     frame_cop = frame.copy()
#     draw = ImageDraw.Draw(frame_cop)

#     for x, y in remove:
#         draw.ellipse((x*100+80, y*100+80, x*100+120, y*100+120), fill=None, outline="#FFC900", width=4)
#     for x, y in positions[1]:
#         draw.ellipse((x*100+80, y*100+80, x*100+120, y*100+120), fill="blue", outline="blue")
#     for x, y in positions[-1]:
#         draw.ellipse((x*100+80, y*100+80, x*100+120, y*100+120), fill="red", outline="red")
#     new_x = move["new_pos"][0]
#     new_y = move["new_pos"][1]
#     old_x = move["selected_pos"][0]
#     old_y = move["selected_pos"][1]
#     draw.ellipse((new_x*100+80, new_y*100+80, new_x*100+120, new_y*100+120), fill=None, outline="green", width=5)
#     draw.ellipse((old_x*100+80, old_y*100+80, old_x*100+120, old_y*100+120), fill=None, outline="green", width=5)

#     frame_cop = np.array(frame_cop)
#     video.append(mpe.ImageClip(frame_cop).set_duration(1))
def __init__():
    global positions, point, frame, video

    game_state = {
                  "board": [[-1, -1, -1, -1, -1],
                            [-1,  0,  0,  0, -1],
                            [ 1,  0,  0,  0, -1],
                            [ 1,  0,  0,  0,  1],
                            [ 1,  1,  1,  1,  1]]}
    positions = [None,
                [(0,2), (0,3), (4,3), (0,4), (1,4), (2,4), (3,4), (4,4)],
                [(0,0), (1,0), (2,0), (3,0), (4,0), (0,1), (4,1), (4,2)]]

    point = []

    frame = cv2.imread(absolute_path + "/chessboard.png")
    frame_cop = frame.copy()
    video = cv2.VideoWriter(absolute_path + "/video.mp4", 0, 1, (600, 600))
    for x, y in positions[1]:
        cv2.circle(frame_cop, (100*x+100,100*y+100), 22, (255,0,0), -1)
    for x, y in positions[-1]:
        cv2.circle(frame_cop, (100*x+100,100*y+100), 22, (0,0,255), -1)
    video.write(frame_cop)

__init__()

def renderVD(positions, move, remove):
    frame_cop = frame.copy()
    for x, y in remove:
        cv2.circle(frame_cop, (100*x+100,100*y+100), 22, (0,201,255), 3)
    for x, y in positions[1]:
        cv2.circle(frame_cop, (100*x+100,100*y+100), 22, (255,0,0), -1)
    for x, y in positions[-1]:
        cv2.circle(frame_cop, (100*x+100,100*y+100), 22, (0,0,255), -1)
    new_x = move["new_pos"][0]
    new_y = move["new_pos"][1]
    old_x = move["selected_pos"][0]
    old_y = move["selected_pos"][1]
    cv2.circle(frame_cop, (100*new_x+100,100*new_y+100), 22, (0,128,0), 3)
    cv2.circle(frame_cop, (100*old_x+100,100*old_y+100), 22, (0,128,0), 3)
    video.write(frame_cop)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/generate_video", methods=['POST'])
def generate_video():
    data = request.get_json()
    for [positions, move, remove] in data:
        print(positions)
        renderVD(positions, move, remove)
    return "hello"
    

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    # open_browser = lambda: webbrowser.open_new("upload-vd.vercel.app")
    # Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
    # open_browser = lambda: webbrowser.open_new("http://127.0.0.1:4000")
    # app.run(port=4000, debug=True, use_reloader=False)
