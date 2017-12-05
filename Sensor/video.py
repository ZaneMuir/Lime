import cv2
import numpy as np
from tqdm import tqdm

drawing = 0
box = []
def mouse_paint_callback(event, x, y, flag, param):
    global drawing,box
    preview = np.zeros((1080,1920,3))
    preview = param
    if event == cv2.EVENT_LBUTTONDOWN:
        #print("click")
        box.append(x)
        box.append(y)
    elif event == cv2.EVENT_LBUTTONUP:
        #print("up")
        drawing += 1
        box.append(x)
        box.append(box[-2])
        preview = cv2.line(preview,
                tuple(box[-4:-2]),
                tuple(box[-2:]),
                (0x00,0xff,0x00),2)
        cv2.imshow("webcam_raw",preview)


def main(camName, outputFileName,width=200):
    global box,preview
    webcam = cv2.VideoCapture(camName)
    cv2.namedWindow("webcam_raw")
    #cv2.namedWindow("demo")


    print("fps: %.2f"%webcam.get(cv2.CAP_PROP_FPS))
    print("resolution: %.0f*%.0f"%( webcam.get(cv2.CAP_PROP_FRAME_WIDTH),
                                    webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("length: %.2f seconds"%(webcam.get(cv2.CAP_PROP_FRAME_COUNT)/webcam.get(cv2.CAP_PROP_FPS)))

    frameScale = 1
    if webcam.get(cv2.CAP_PROP_FRAME_WIDTH) > 720:
        frameScale = webcam.get(cv2.CAP_PROP_FRAME_WIDTH) / 720

    ret, frame = webcam.read()
    preview = np.array(frame[::int(frameScale),::int(frameScale)])
    #print(type(frame))
    cv2.imshow("webcam_raw",preview)
    cv2.setMouseCallback("webcam_raw",mouse_paint_callback,preview)
    while True:
        if cv2.waitKey(1) == 13:
            #cv2.destroyWindow("webcam_raw")
            break

    roi = np.array(box) * int(frameScale)
    outputFile = open(outputFileName,'w')
    outputFile.write("frame,time,left,right\n")
    print(roi)

    '''frame = cv2.line(frame,
        tuple(roi[-4:-2]),
        tuple(roi[-2:]),
        (0x00,0xff,0x00),2)
    frame = cv2.line(frame,
        tuple(roi[0:2]),
        tuple(roi[2:4]),
        (0xff,0x00,0x00),2)
    while True:
        cv2.imshow("demo", frame)
        if cv2.waitKey(1) == 13:
            break'''
    pbar = tqdm(total=webcam.get(cv2.CAP_PROP_FRAME_COUNT))
    try:
        pos = 1
        while webcam.isOpened():
            ret,frame = webcam.read()
            left = frame[roi[1]-width//2:roi[3]+width//2,roi[0]:roi[2],2].mean()
            right = frame[roi[5]-width//2:roi[7]+width//2,roi[4]:roi[6],2].mean()
            #cv2.imshow("demo",left)
            pos += 1
            outputFile.write("%d,%.2f,%.2f,%.2f\n"%(pos,pos/25,left,right))
            pbar.update(1)
    except KeyboardInterrupt:
        pass
    except TypeError:
        #final frame
        pass
    pbar.close()
    outputFile.close()
    webcam.release()

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
