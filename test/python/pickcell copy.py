import cv2
import numpy as np
import argparse
import time


def main():
    #img1, img2 = args()
    img1 = cv2.imread('test/output/daen/1_arranged.png')
    img2 = cv2.imread('test/output/daen/6_arranged.png')
    start = time.time()
    result = pick(img1, img2)
    end = time.time()
    print('time: ', end - start)

def test():
    img1 = cv2.imread('test/output/daen/1_arranged.png')
    img2 = cv2.imread('test/output/daen/6_arranged.png')
    h, w = img2.shape[:2]
    length = h * w
    img1 = img1.reshape(length, 3)
    img2 = img2.reshape(length, 3)
    if not ((img1[0].sum() == 50) and (img2[0].sum() == 0)):
        print('docchimo zero')

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in1')
    parser.add_argument('--in2')
    args = parser.parse_args()
    return args.in1, args.in2

def pick(img1, img2):
    #img1 = cv2.imread(img1)
    #img2 = cv2.imread(img2)
    aa = [[[  0,  74, 255], 831.0],\
[[  0,  64, 255], 832.0],
[[  0,  53, 255], 833.0],
[[  0,  43, 255], 834.0],
[[  0,  33, 255], 835.0],
[[  0,  21, 255], 836.0],
[[  0,  11, 255], 837.0],
[[  0,   1, 255], 838.0],
[[  0,  95, 255], 829.0],
[[  0, 105, 255], 828.0],
[[  0, 117, 255], 827.0],
[[  0, 127, 255], 826.0],
[[  0, 136, 255], 825.0],
[[  0, 148, 255], 824.0],
[[  0, 158, 255], 823.0],
[[  0, 168, 255], 822.0],
[[  0, 179, 255], 821.0],
[[  0, 189, 255], 820.0],
[[  0, 199, 255], 819.0],
[[  0, 210, 255], 818.0],
[[  0, 220, 255], 817.0],
[[  0, 231, 255], 816.0],
[[  0, 241, 255], 815.0],
[[  0, 251, 255], 814.0],
[[  0, 255, 241], 813.0],
[[  0, 255, 221], 812.0],
[[  0, 255, 201], 811.0],
[[  0, 255, 179], 810.0],
[[  0, 255, 159], 809.0],
[[  0, 255, 139], 808.0],
[[  0, 255, 116], 807.0],
[[  0, 255,  96], 806.0],
[[  0, 255,  74], 805.0],
[[  0, 255,  54], 804.0],
[[  0, 255,  34], 803.0],
[[  0, 255,  11], 802.0],
[[  9, 255,   4], 801.0],
[[ 28, 255,  14], 800.0],
[[ 51, 255,  26], 799.0],
[[ 71, 255,  36], 798.0],
[[ 91, 255,  46], 797.0],
[[113, 255,  57], 796.0],
[[133, 255,  67], 795.0],
[[156, 255,  78], 794.0],
[[176, 255,  88], 793.0],
[[195, 255,  98], 792.0],
[[218, 255, 110], 791.0],
[[238, 255, 119], 790.0],
[[255, 252, 127], 789.0],
[[255, 229, 115], 788.0],
[[255, 210, 105], 787.0],
[[255, 190,  95], 786.0],
[[255, 167,  84], 785.0],
[[255, 147,  74], 784.0],
[[255, 125,  63], 783.0],
[[255, 105,  53], 782.0],
[[255,  85,  43], 781.0],
[[255,  62,  31], 780.0],
[[255,  42,  21], 779.0],
[[255,  23,  11], 778.0],
[[255,   0,   0], 777.0],
[[235,   0,   0], 776.0],
[[215,   0,   0], 775.0],
[[193,   0,   0], 774.0],
[[173,   0,   0], 773.0],
[[150,   0,   0], 772.0],
[[130,   0,   0], 771.0],
[[111,   0,   0], 770.0],
[[88,  0,  0], 769.0],
[[68,  0,  0], 768.0],
[[48,  0,  0], 767.0],
[[25,  0,  0], 766.0],
[[6, 0, 0], 765.0]
]
    ll = np.array([[  0,  74, 255],[  0,  64, 255],[  0,  53, 255],[  0,  43, 255],[  0,  33, 255],[  0,  21, 255],[  0,  11, 255],[  0,   1, 255],[  0,  95, 255],[  0, 105, 255],[  0, 117, 255],[  0, 127, 255],[  0, 136, 255],[  0, 148, 255],[  0, 158, 255],[  0, 168, 255],[  0, 179, 255],[  0, 189, 255],[  0, 199, 255],[  0, 210, 255],[  0, 220, 255],[  0, 231, 255],[  0, 241, 255],[  0, 251, 255],[  0, 255, 241],[  0, 255, 221],[  0, 255, 201],[  0, 255, 179],[  0, 255, 159],[  0, 255, 139],[  0, 255, 116],[  0, 255,  96],[  0, 255,  74],[  0, 255,  54],[  0, 255,  34],[  0, 255,  11],[  9, 255,   4],[ 28, 255,  14],[ 51, 255,  26],[ 71, 255,  36],[ 91, 255,  46],[113, 255,  57],[133, 255,  67],[156, 255,  78],[176, 255,  88],[195, 255,  98],[218, 255, 110],[238, 255, 119],[255, 252, 127],[255, 229, 115],[255, 210, 105],[255, 190,  95],[255, 167,  84],[255, 147,  74],[255, 125,  63],[255, 105,  53],[255,  85,  43],[255,  62,  31],[255,  42,  21],[255,  23,  11],[255,   0,   0],[235,   0,   0], [215,   0,   0],[193,   0,   0],[173,   0,   0],[150,   0,   0],[130,   0,   0], [111,   0,   0],[88,  0,  0],[68,  0,  0],[48,  0,  0],[25,  0,  0],[6, 0, 0]])
    h, w = img1.shape[:2]
    length = h * w
    img1 = img1.reshape(length, 3)
    img2 = img2.reshape(length, 3)
    img1a = np.split(img1, 2, 0)
    result = []
    for i in range(length):
        if not ((img1[i].sum() <= 50) or (img2[i].sum() == 0)):
            idx = np.abs(ll - img2[i]).sum(axis=1).argmin()
            result.append([i, img1[i], img2[i], aa[idx][1]])
            #for c in ll:
            #    a = [x - y for (x, y) in zip(c, img2[i])]
            #    b = np.absolute(a).sum()
            #    if min > b:
            #        min = b
            #        val = c[1]
            #result.append([img1[i], img2[i], val])
    return result

if __name__ == '__main__':
    main()
    #test()