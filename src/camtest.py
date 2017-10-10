'''
webcam testing
Created on Apr 28, 2017
Copied from:
http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/

@author: user
'''

# import the necessary packages
import argparse
import datetime
#import imutils
import time

import cv2

import googletest

 
# initialize the first frame in the video stream
firstFrame = None


def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=200, help="minimum area size")
    args = vars(ap.parse_args())
     
    # if the video argument is None, then we are reading from webcam
    if args.get("video", None) is None:
        camera = cv2.VideoCapture(0)  # @UndefinedVariable
        time.sleep(1)
        #my cam was starting with blanks
        camera.read()
        camera.read()
        ret,frame = camera.read()
        if ret==False:
            print "ERROR:Failed to read from camera. Make sure camera is connected and working. Check it from other software... Exiting."
            camera.release()
            exit(1)
    # otherwise, we are reading from a video file
    else:
        camera = cv2.VideoCapture(args["video"])  # @UndefinedVariable
     
    # initialize the first frame in the video stream
    firstFrame = None
        
        
    i = 0
    
    occupied = False
    
    writer = None
    fourcc = int(camera.get(cv2.CAP_PROP_FOURCC))
    #fourcc = -1
    frame_size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    
    videoformats = ['H264', 'XVID', 'h263', 'DIVX', 'M4S2', 'MP4V', 'WMVP', 'WMV3', 'WMV1', 'mpeg', 'MPEG']
    
    fps = camera.get(cv2.CAP_PROP_FPS)
    fps = 30
    
    iscolor = True #BW

    '''testing only
    for videoformat in videoformats:
        fourcc = cv2.VideoWriter_fourcc(*videoformat)
        print "Trying: "+videoformat
        filename = "c:/users/user/videos/motion/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"."+videoformat        
        writer = cv2.VideoWriter(filename, fourcc, fps,  frame_size, isColor=iscolor)
        if writer.isOpened():
            break
        else:
            print "Failed opening video writer"
    '''
    videoformat = 'H264' #tested ok with dll found in src folder
    fourcc = cv2.VideoWriter_fourcc(*videoformat)
    
    #google drive api service
    service = googletest.get_service()

                
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"
     
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break
     
        # resize the frame, convert it to grayscale, and blur it
        #frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # @UndefinedVariable
        gray = cv2.GaussianBlur(gray, (21, 21), 0)  # @UndefinedVariable
     
        # if the first frame is None, initialize it, also initialize every N frames
        i = i+1
        if firstFrame is None or i%100==0:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray) # @UndefinedVariable
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1] # @UndefinedVariable
     
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2) # @UndefinedVariable
        (_img, cnts,_hier) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # @UndefinedVariable
     
        # loop over the contours
        occupied = False
        for c in cnts:
            # if the contour is too small, ignore it
            cntrarea = cv2.contourArea(c) # @UndefinedVariable
            #print cntrarea
            if cntrarea < args["min_area"]:
                continue
     
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c) # @UndefinedVariable
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # @UndefinedVariable
            text = "Occupied"
            occupied = True

        # draw the text and timestamp on the frame
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) # @UndefinedVariable
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1) # @UndefinedVariable
     
        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame) # @UndefinedVariable
        #cv2.imshow("Thresh", thresh) # @UndefinedVariable
        #cv2.imshow("Frame Delta", frameDelta) # @UndefinedVariable
        
        if occupied:
            if not writer:
                filename = "c:/users/user/videos/motion/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"."+videoformat
                writer = cv2.VideoWriter(filename, fourcc, fps,  frame_size, isColor=iscolor)
                if not writer.isOpened():
                    print "Failed opening video writer"
                    break;
                
                print "Opened file: "+filename
                
            
            writer.write(frame)
            
        elif writer:
            #close video if room is back to unocuppied
            writer.release()
            writer = None
            print "Closed file: "+filename
            
            #upload the file to 
            print "Uploading the file"
            googletest.upload_file(service, filename)
            print "File uploaded"
            
            
        #wait 30ms to get average 30fps
        key = cv2.waitKey(30) & 0xFF # @UndefinedVariable
        
        # if the `q` key is pressed, break from the loop
        if key == ord("q"):
            break
        
     
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows() # @UndefinedVariable
    
    
if __name__ == "__main__":
    main()