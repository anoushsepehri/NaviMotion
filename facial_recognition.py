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
        return
    else:
        if current_motion != "":
            global prev_motion_quantified
            global prev_motion_quantified_time
            global current_motion_time
            if (current_motion == "RIGHT" and prev_motion_quantified == "LEFT" and (current_motion_time-prev_motion_quantified_time)<elapsed_time) or (current_motion == "LEFT" and prev_motion_quantified == "RIGHT" and (current_motion_time-prev_motion_quantified_time)<elapsed_time) or (current_motion == "UP" and prev_motion_quantified == "DOWN" and (current_motion_time-prev_motion_quantified_time)<elapsed_time) or (current_motion == "DOWN" and prev_motion_quantified == "UP" and (current_motion_time-prev_motion_quantified_time)<elapsed_time):
                return
            else:
                prev_motion_quantified = current_motion
                prev_motion_quantified_time = current_motion_time
                print current_motion
                return


cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)

averaged_centroid_list = list()
averaged_centroid_previous = (0,0)
averaged_centroid_current = (0,0)

while True:

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
    motionfilter(prev_motion,current_motion)

# Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
