u"""video主要包含视频处理的主要函数."""
import cv2
import numpy as np
from tqdm import tqdm
from .database import createNewPoseTable

drawing = 0
box = []


def mouse_paint_callback(event, x, y, flag, param):
    global drawing, box
    preview = np.zeros((1080, 1920, 3))
    preview = param
    if event == cv2.EVENT_LBUTTONDOWN:
        # print("click")
        box.append(x)
        box.append(y)
    elif event == cv2.EVENT_LBUTTONUP:
        # print("up")
        drawing += 1
        box.append(x)
        box.append(box[-2])
        preview = cv2.line(preview,
                           tuple(box[-4:-2]),
                           tuple(box[-2:]),
                           (0x00, 0xff, 0x00), 2)
        cv2.imshow("webcam_raw", preview)


def main(camName, dbCursor, session_name, ncage=2, width=20):
    global box, preview
    webcam = cv2.VideoCapture(camName)

    cv2.namedWindow("webcam_raw")

    # print meta info
    print("fps: %.2f" % webcam.get(cv2.CAP_PROP_FPS))
    print("resolution: %.0f*%.0f" % (webcam.get(cv2.CAP_PROP_FRAME_WIDTH),
                                     webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("length: %.2f seconds" % (webcam.get(cv2.CAP_PROP_FRAME_COUNT) /
                                    webcam.get(cv2.CAP_PROP_FPS)))

    # scale frame to a better size, ie. 720p
    frameScale = 1
    if webcam.get(cv2.CAP_PROP_FRAME_WIDTH) > 720:
        frameScale = webcam.get(cv2.CAP_PROP_FRAME_WIDTH) / 720

    webcam.set(cv2.CAP_PROP_POS_FRAMES, 60*25)
    ret, frame = webcam.read()
    preview = np.array(frame[::int(frameScale), ::int(frameScale)])
    cv2.imshow("webcam_raw", preview)
    cv2.setMouseCallback("webcam_raw", mouse_paint_callback, preview)

    while True:
        if cv2.waitKey(1) == 13:
            # cv2.destroyWindow("webcam_raw")
            break

    roi = np.array(box) * int(frameScale)
    print(roi[:ncage*4])

    pbar = tqdm(total=webcam.get(cv2.CAP_PROP_FRAME_COUNT))

    title = ['p%d' % (i + 1) for i in range(ncage)]
    result = []

    webcam.set(cv2.CAP_PROP_POS_FRAMES, 0)
    try:
        pos = 1
        while webcam.isOpened():
            item = [pos, pos/25]
            ret, frame = webcam.read()
            for index in range(ncage):
                item.append(float(
                    frame[roi[1+index*4]-width//2:roi[3+index*4]+width//2,
                          roi[0+index*4]:roi[2+index*4], 2].mean()))
            result.append(tuple(item))
            pos += 1
            pbar.update(1)
    except KeyboardInterrupt:
        pass
    except TypeError:
        # final frame
        pass

    pbar.close()
    webcam.release()
    createNewPoseTable(dbCursor, session_name, title, result)  # TODO
    return True


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
