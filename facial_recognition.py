import cv2
import sys
import time

prev_x=0
prev_y=0

def motiondetect(centroid1, centroid2):
    delta_x=centroid2[0]-centroid1[0]
    delta_y=centroid2[1]-centroid1[1]

    if delta_x<-2:
        return "LEFT"
    elif delta_x>2:
        return "RIGHT"
    elif delta_y<-5:
        return "DOWN"
    else:
        return " "


cood = []
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)

averaged_centroid_list = list()
averaged_centroid_previous = (0,0)
averaged_centroid_current = (0,0)

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
        averaged_centroid_x = sum(i[0] for i in averaged_centroid_list)/ len(averaged_centroid_list)
        averaged_centroid_y = sum(i[1] for i in averaged_centroid_list) / len(averaged_centroid_list)
        averaged_centroid_previous = averaged_centroid_current
        averaged_centroid_current = (averaged_centroid_x,averaged_centroid_y)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame,averaged_centroid_current,5,(255,0,0),2)

    output=motiondetect(averaged_centroid_previous,averaged_centroid_current)
    print (output)

# Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
