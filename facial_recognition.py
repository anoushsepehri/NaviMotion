import cv2
import sys
import time

prev_x=0
prev_y=0

def deltapos(x,y,prev_x,prev_y):

    delta_x=prev_x-x
    delta_y=prev_y-y

    prev_x=x
    prev_y=y

    return(delta_x,delta_y)

def motiondetec(cood):
    delta_x=cood[0]
    delta_y=cood[1]

    if delta_x<-7:
        return "LEFT"
    elif delta_x>7:
        return "RIGHT"
    elif delta_y<-5:
        return "DOWN"
    else:
        return " "



cood=[]
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    time.sleep(0.05)
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
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
       
        cood=deltapos(x+(w/2),(y+(+h/2)),prev_x,prev_y)
        prev_x=(x+(w/2))
        prev_y=(y+(h/2))
        output=motiondetec(cood)
        print (output)


# Display the resulting frame
    cv2.imshow('Video', frame)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()