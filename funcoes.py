import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def inverter_cor(path):
    img_bgr = cv2.imread(path, 1)

    color = ('b', 'g', 'r')

    hist_original = []
    for i, col in enumerate(color):
        histr = cv2.calcHist([img_bgr], [i], None, [256], [0, 256])
        hist_original.append(histr)

    img_negativa = 255 - img_bgr

    hist_negativa = []
    for i, col in enumerate(color):
        histr = cv2.calcHist([img_negativa], [i], None, [256], [0, 256])
        hist_negativa.append(histr)

    def histogram_to_image(hist_list):
        plt.figure()
        for i, col in enumerate(color):
            plt.plot(hist_list[i], color=col)
            plt.xlim([0, 256])
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(img_arr, 1)
        buf.close()
        return img

    hist_img_orig = histogram_to_image(hist_original)
    hist_img_neg = histogram_to_image(hist_negativa)

    return img_negativa, hist_img_orig, hist_img_neg


def convolucao(path, intensidade: int):
    
    image = cv2.imread(path)
    
    intensidade = intensidade + 5

    kernel = np.array([[0, -1, 0],
                    [-1, intensidade, -1],
                    [0, -1, 0]])

    imagem_convolucionada = cv2.filter2D(image, -1, kernel)
    
    return imagem_convolucionada

def blur(path, intensidade: int):
    
    image = cv2.imread(path)

    average_blur = cv2.blur(image, (intensidade, intensidade))
    
    return average_blur