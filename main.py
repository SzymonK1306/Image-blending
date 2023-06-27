import cv2 as cv
import numpy as np,sys
apple = cv.imread('apple.jpg')
orange = cv.imread('orange.jpg')
mask = np.zeros(apple.shape[:2], dtype='uint8')
cv.rectangle(mask, (0, 0), (int(apple.shape[0]/2), int(apple.shape[1])), 255, -1)
maskList = [mask]
# generate Gaussian pyramid for A
GaussFloor = apple.copy()
# GaussFloor = cv.bitwise_and(GaussFloor, GaussFloor, mask=mask)
gaussPiramidA = [GaussFloor]

for i in range(6):
    GaussFloor = cv.pyrDown(GaussFloor)
    # mask = cv.pyrDown(mask)
    # GaussFloor = cv.bitwise_and(GaussFloor, GaussFloor, mask=mask)
    # cv.imshow('c', GaussFloor)
    # cv.waitKey(0)
    gaussPiramidA.append(GaussFloor)
    # maskList.append(mask)
# generate Gaussian pyramid for B
# del maskList[-1]
# maskList.reverse()
mask = np.zeros(apple.shape[:2], dtype='uint8')
cv.rectangle(mask, (int(apple.shape[0]/2), 0), (int(apple.shape[0]), int(apple.shape[1])), 255, -1)
GaussFloor = orange.copy()
# GaussFloor = cv.bitwise_and(GaussFloor, GaussFloor, mask=mask)
gaussPiramidB = [GaussFloor]
for i in range(6):
    GaussFloor = cv.pyrDown(GaussFloor)
    # mask = cv.pyrDown(mask)
    # GaussFloor = cv.bitwise_and(GaussFloor, GaussFloor, mask=mask)
    gaussPiramidB.append(GaussFloor)
# generate Laplacian Pyramid for A
laplacePiramidA = [gaussPiramidA[5]]
for i in range(5,0,-1):
    GE = cv.pyrUp(gaussPiramidA[i], dstsize=(gaussPiramidA[i - 1].shape[1], gaussPiramidA[i - 1].shape[0]))
    L = cv.subtract(gaussPiramidA[i - 1], GE)
    # cv.imshow('GE', GE)
    # cv.imshow('Down', gaussPiramidA[i])
    # cv.imshow('c', L)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    laplacePiramidA.append(L)
# generate Laplacian Pyramid for B
laplacePiramidB = [gaussPiramidB[5]]
for i in range(5,0,-1):
    GE = cv.pyrUp(gaussPiramidB[i], dstsize=(gaussPiramidB[i - 1].shape[1], gaussPiramidB[i - 1].shape[0]))
    L = cv.subtract(gaussPiramidB[i - 1], GE)
    laplacePiramidB.append(L)

# Now add left and right halves of images in each level
LS = []
for la,lb in zip(laplacePiramidA, laplacePiramidB):
    rows,cols,dpt = la.shape
    ls = np.hstack((la[:,0:cols//2], lb[:,cols//2:]))
    # ls = np.hstack((la, lb))
    # ls = cv.add(la, lb)
    LS.append(ls)
# now reconstruct
ls_ = LS[0]
for i in range(1,6):
    ls_ = cv.pyrUp(ls_, dstsize=(LS[i].shape[1],LS[i].shape[0]))
    ls_ = cv.add(ls_, LS[i])

# image with direct connecting each half
real = np.hstack((apple[:, :cols // 2], orange[:, cols // 2:]))
cv.imwrite('Pyramid_blending2.jpg',ls_)
cv.imwrite('Direct_blending.jpg',real)
# cv.imshow('cos',mask)
# cv.imshow('oa',ls_)
cv.waitKey(0)