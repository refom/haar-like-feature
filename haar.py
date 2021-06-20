
from integral import sum_kotak


class FeatureType:
    TWO_VERTICAL=(1, 2)
    TWO_HORIZONTAL=(2, 1)
    THREE_HORIZONTAL=(3, 1)
    THREE_VERTICAL=(1, 3)
    FOUR=(2, 2)
    ALL = [TWO_VERTICAL, TWO_HORIZONTAL, THREE_VERTICAL, THREE_HORIZONTAL, FOUR]
    ALL_TEXT = ["TWO_VERTICAL", "TWO_HORIZONTAL", "THREE_VERTICAL", "THREE_HORIZONTAL", "FOUR"]

# (x, y)
class HaarLikeFeature(object):
    def __init__(self, feature_type, top_left, width, height, threshold):
        self.tipe = feature_type
        
        self.top_left = top_left
        self.bottom_right = (top_left[0] + width, top_left[1] + height)

        self.width = width
        self.width2 = width / 2
        self.width3 = width / 3
        
        self.height = height
        self.height2 = height / 2
        self.height3 = height / 3
        
        self.threshold = threshold
    
    def get_score(self, ii_img):
        score = 0

        if self.tipe == FeatureType.TWO_VERTICAL:
            atas = sum_kotak(ii_img, self.top_left, (self.bottom_right[0], int(self.top_left[1] + self.height2)))
            bawah = sum_kotak(ii_img, (self.top_left[0], int(self.top_left[1] + self.height2)), self.bottom_right)
            score = atas - bawah
        elif self.tipe == FeatureType.TWO_HORIZONTAL:
            kiri = sum_kotak(ii_img, self.top_left, (int(self.top_left[0] + self.width2), self.bottom_right[1]))
            kanan = sum_kotak(ii_img, (int(self.top_left[0] + self.width2), self.top_left[1]), self.bottom_right)
            score = kiri - kanan
        elif self.tipe == FeatureType.THREE_HORIZONTAL:
            kiri = sum_kotak(ii_img, self.top_left, (int(self.top_left[0] + self.width3), self.bottom_right[1]))
            tengah = sum_kotak(ii_img, (int(self.top_left[0] + self.width3), self.top_left[1]), (int(self.top_left[0] + 2 * self.width3), self.bottom_right[1]))
            kanan = sum_kotak(ii_img, (int(self.top_left[0] + 2 * self.width3), self.top_left[1]), self.bottom_right)
            score = kiri - tengah + kanan
        elif self.tipe == FeatureType.THREE_VERTICAL:
            atas = sum_kotak(ii_img, self.top_left, (self.bottom_right[0], int(self.top_left[1] + self.height3)))
            tengah = sum_kotak(ii_img, (self.top_left[0], int(self.top_left[1] + self.height3)), (self.bottom_right[0], int(self.top_left[1] + 2 * self.height3)))
            bawah = sum_kotak(ii_img, (self.top_left[0], int(self.top_left[1] + 2 * self.height3)), self.bottom_right)
            score = atas - tengah + bawah
        elif self.tipe == FeatureType.FOUR:
            # top left area
            kiri_atas = sum_kotak(ii_img, self.top_left, (int(self.top_left[0] + self.width2), int(self.top_left[1] + self.height2)))
            # top right area
            kanan_atas = sum_kotak(ii_img, (int(self.top_left[0] + self.width2), self.top_left[1]), (self.bottom_right[0], int(self.top_left[1] + self.height2)))
            # bottom left area
            kiri_bawah = sum_kotak(ii_img, (self.top_left[0], int(self.top_left[1] + self.height2)), (int(self.top_left[0] + self.width2), self.bottom_right[1]))
            # bottom right area
            kanan_bawah = sum_kotak(ii_img, (int(self.top_left[0] + self.width2), int(self.top_left[1] + self.height2)), self.bottom_right)
            score = kiri_atas - kanan_atas - kiri_bawah + kanan_bawah
        return score
    
    def get_result(self, ii_img):
        score = self.get_score(ii_img)
        return (1 if score < self.threshold else -1)

