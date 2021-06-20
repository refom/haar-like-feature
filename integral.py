import numpy as np


"""
+--------   +------------
| 1 2 3 .   | 0  0  0  0 .
| 4 5 6 .   | 0  1  3  6 .
| . . . .   | 0  5 12 21 .
            | . . . . . .
"""

def integral_image(img_arr):
    
    # Pertambahan untuk kolom
    col_sum = np.zeros(img_arr.shape)
    # Pertambahan untuk row
    ii_arr = np.zeros((img_arr.shape[0] + 1, img_arr.shape[1] + 1))

    for x in range(img_arr.shape[1]):
        for y in range(img_arr.shape[0]):
            # Tambahkan pixel diatasnya yang sudah ditambahkan dengan pixel yg diatasnya
            # Intinya nambahin bagian kolom
            col_sum[y, x] = col_sum[y-1, x] + img_arr[y, x]

            # Tambahkan pixel di kiri yg sudah ditambahkan dengan pixel yg dikirinya
            # Intinya nambahin bagian row
            ii_arr[y+1, x+1] = ii_arr[y+1, x] + col_sum[y, x]

    return ii_arr


def sum_kotak(ii_arr, top_left, bottom_right):
    # swap dari (x, y) menjadi (y, x)
    top_left = (top_left[1], top_left[0])
    bottom_right = (bottom_right[1], bottom_right[0])

    if top_left == bottom_right:
        return ii_arr[top_left]

    # Ambil titik kanan atas dan kiri bawah
    top_right = (top_left[0], bottom_right[1])
    bottom_left = (bottom_right[0], top_left[1])

    # Kalkulasi kotak yang diinginkan
    return ii_arr[bottom_right] - ii_arr[bottom_left] - ii_arr[top_right] + ii_arr[top_left]


