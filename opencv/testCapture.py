import cv2 as cv

cam = cv.VideoCapture(0)

s, img = cam.read()
if s:
	cv.namedWindow("cam-test")
	cv.imshow("cam-test", img)
	cv.waitkey(0)
	cv.destroyWindow("cam-test")
	cv.imwrite("01.jpg", img)
