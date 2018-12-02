import tkinter as tk
import cv2
import sys
import time

prev_x = 0
prev_y = 0
error = 3
elapsed_time = 1

prev_motion_quantified = "LEFT" # can be LEFT,RIGHT,TOP,DOWN
prev_motion_quantified_time = time.time()
prev_motion = "" # can be LEFT,RIGHT,TOP,DOWN,<empty string>
current_motion = "" # can be LEFT,RIGHT,TOP,DOWN,<empty string>
current_motion_time = time.time()

class Device:
    def __init__(self,id,name,location,state):
        self.id = id        # id of the device
        self.name = name    # name of the device, can be repeated
        self.loc = location # loc is location in residence
        self.state = state  # state is Boolean True=On, False=Off

dev1 = Device(1,"Light 1", "House", False)
dev2 = Device(2,"Light 2", "House", False)
dev3 = Device(3,"Light 3", "House", False)

def motiondetect(centroid1, centroid2):
    delta_x=centroid2[0]-centroid1[0]
    delta_y=centroid2[1]-centroid1[1]

    if delta_x > error and abs(delta_x) > abs(delta_y):
        return "LEFT", time.time()
    elif delta_x < -error and abs(delta_x) > abs(delta_y):
        return "RIGHT", time.time()
    elif delta_y > error and abs(delta_y) > abs(delta_x):
        return "DOWN", time.time()
    elif delta_y < -error and abs(delta_y) > abs(delta_x):
        return "UP", time.time()
    else:
        return "", time.time()

def motionfilter(prev_motion,current_motion):
    if current_motion == prev_motion:
        return " "
    else:
        if current_motion != "":
            global prev_motion_quantified
            global prev_motion_quantified_time
            global current_motion_time
            if (current_motion == "RIGHT" and prev_motion_quantified == "LEFT" and (current_motion_time-prev_motion_quantified_time)<elapsed_time) \
                or (current_motion == "LEFT" and prev_motion_quantified == "RIGHT" and (current_motion_time-prev_motion_quantified_time)<elapsed_time) \
                or (current_motion == "UP" and prev_motion_quantified == "DOWN" and (current_motion_time-prev_motion_quantified_time)<elapsed_time) \
                or (current_motion == "DOWN" and prev_motion_quantified == "UP" and (current_motion_time-prev_motion_quantified_time)<elapsed_time):
                return " "
            else:
                prev_motion_quantified = current_motion
                prev_motion_quantified_time = current_motion_time
                return current_motion
        else:
            return " "

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)

averaged_centroid_list = list()
averaged_centroid_previous = (0,0)
averaged_centroid_current = (0,0)

# _________________ Window ________________#

# initialize window
window = tk.Tk()

# list of all the devices
listD = (dev1, dev2, dev3)

#initial device
initialD = listD[0]

#initial center text
center_text = tk.Label(text=initialD, master=window, height=20, width=20)
center_text.grid(column=1, row=2)
#center_text.insert(tk.END, initialD)

# ______ Functions _________
def textupdate(input, initial):

    new_strings = ""
    new_string = ""
    button_up.configure(bg="white")
    button_down.configure(bg="white")
    button_enter.configure(bg="white")
    button_back.configure(bg="white")

    #conditionals for different face movements
    if input == "UP":
        if listD.index(initial) - 1 >= 0:
            new_string = listD[listD.index(initial) - 1]
            new_strings = listD[listD.index(initial) - 1]

        else:
            new_string = initial
            new_strings = initial
        button_up.configure(bg="green")

    elif input == "DOWN":
        if listD.index(initial) + 1 < len(listD):
            new_string = listD[listD.index(initial) + 1]
            new_strings = listD[listD.index(initial) + 1]
        else:
            new_string = initial
            new_strings = initial
        button_down.configure(bg="green")
    elif input == "RIGHT":
        initial.state = True
        new_string = initial
        button_enter.configure(bg="green")
    elif input == "LEFT":
        initial.state = False
        new_string = initial
        button_back.configure(bg="green")
    else:
        new_string = initial
        new_strings = initial

    if not input == " ":
        if new_string.state:
            center_text.configure(text=new_string.name + " State: On")
            window.config(background="yellow")
        else:
            center_text.configure(text=new_string.name + " State: Off")
            window.config(background="black")
    return new_string

window.title("The App")
window.geometry("800x800")
window.config(background="black")

# title
title = tk.Label(text="This is our app")
title.grid(row=0, column=1)

#Button
button_up = tk.Button(text="Go Up", height=10, width=20)
button_up.grid(row=1,column=0, columnspan=3, sticky="we")

button_down = tk.Button(text="Go Down", height=10, width=20)
button_down.grid(row=3, column=0, columnspan=3, sticky="we")

button_enter = tk.Button(text="Enter", height=20, width=10)
button_enter.grid(row=2, column=2)

button_back = tk.Button(text="Back", height=20, width=10)
button_back.grid(row=2, column=0)

#Label
#tk.Label (window, text="lable", bg="black", fg="white", font="none 12 bold").grid(row=0, column=0)

#text
#center_text = tk.Text(master=window, height=20, width=20)
#center_text.grid(column=1, row=2)
#center_text.insert(tk.END, "Hello")



while True:
    # time.sleep(0.05)
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(40, 40),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:

        centroid = (x+w/2,y+h/2)
        averaged_centroid_list.append(centroid)
        averaged_centroid_list = averaged_centroid_list[-5:]
        averaged_centroid_x = int(sum(i[0] for i in averaged_centroid_list)/ len(averaged_centroid_list))
        averaged_centroid_y = int(sum(i[1] for i in averaged_centroid_list) / len(averaged_centroid_list))
        averaged_centroid_previous = averaged_centroid_current
        averaged_centroid_current = (averaged_centroid_x,averaged_centroid_y)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame,averaged_centroid_current,5,(0,255,0),2)

    prev_motion = current_motion
    current_motion, current_motion_time = motiondetect(averaged_centroid_previous,averaged_centroid_current)
    output=motionfilter(prev_motion,current_motion)
    print(output)
    initialD=textupdate(output,initialD)


# Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    window.update()

# When everything is done, release the capture
#video_capture.release()




cv2.destroyAllWindows()
