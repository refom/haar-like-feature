import pygame
from pygame import Vector2

import numpy as np
from PIL import Image
from warna import COLORS
from integral import integral_image
from haar import FeatureType, HaarLikeFeature
from font_teks import FontText

class Benda:
    FontText.update()
    first_mouse_pos = (0,0)
    last_mouse_pos = (0,0)
    min_feature_width = 4
    max_feature_width = 7
    min_feature_height = 4
    max_feature_height = 7

    def __init__(self, nama, img, pos):
        self.nama = nama
        self.img = pygame.image.load(img)
        self.pos = Vector2(pos)
        self.rect = self.img.get_rect(center=pos)

        self.button_down = False
        self.draw_rect = False
        self.hide_rect = True
        self.sudah_dieksekusi = False

        images = Image.open(img).convert("L")
        image_arr = np.array(images)
        self.int_img = integral_image(image_arr)
        self.result = []

    def render(self, surface):
        width, height = surface.get_size()

        # render gambar
        self.pos.x = width/2
        self.pos.y = height/2
        self.rect = self.img.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(self.img, self.rect)
        pos = [self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft]
        pygame.draw.polygon(surface, COLORS.black, pos, 2)

        # Render hasil
        if self.result:
            ada_wajah = 0
            win_size = surface.get_size()
            y = 20
            for hasil, feature in zip(self.result, FeatureType.ALL_TEXT):
                teks = FontText.font_normal.render(f"{feature} = {hasil}", True, COLORS.black)
                rect = teks.get_rect(topright=(win_size[0] - 20, y))
                surface.blit(teks, rect)
                y += 25
                if hasil:
                    ada_wajah += 1
            
            if ada_wajah == 5:
                teks = FontText.font_normal.render("Hasil = Wajah Ditemukan", True, COLORS.black)
                rect = teks.get_rect(topright=(win_size[0] - 20, y))
                surface.blit(teks, rect)


    def render_rect(self, surface):
        p1 = self.first_mouse_pos
        p2 = (self.first_mouse_pos[0], self.last_mouse_pos[1])
        p3 = self.last_mouse_pos
        p4 = (self.last_mouse_pos[0], self.first_mouse_pos[1])
        
        if self.rect.collidepoint(p1) and self.rect.collidepoint(p2) and self.rect.collidepoint(p3) and self.rect.collidepoint(p4):
            pygame.draw.polygon(surface, COLORS.light_green, [p1, p2, p3, p4], 2)


    def eksekusi_haar(self):
        if not self.hide_rect:
            if not self.button_down:
                if not self.sudah_dieksekusi:
                    self.sudah_dieksekusi = True
                    print("Mulai Eksekusi")
                    x = self.first_mouse_pos[0] - self.last_mouse_pos[0]
                    y = self.first_mouse_pos[1] - self.last_mouse_pos[1]
                    if x <= 0 and y <= 0:
                        top_left = self.first_mouse_pos
                    else:
                        top_left = self.last_mouse_pos
                    
                    top_left = (top_left[0] - self.rect.left, top_left[1] - self.rect.top)
                    print(f"Dapat titik kiri atas {top_left}")

                    width = abs(x)
                    height = abs(y)
                    print(f"Width, Height: {width}, {height}")

                    if width <= self.max_feature_width or height <= self.max_feature_height:
                        print("kotak terlalu kecil")
                        return

                    print("Kotak sesuai kriteria")
                    all_feature = []
                    for feature in FeatureType.ALL:
                        one_feature = []
                        for feature_width in range(self.min_feature_width, self.max_feature_width, feature[0]):
                            for feature_height in range(self.min_feature_height, self.max_feature_height, feature[1]):
                                for x in range(width - feature_width):
                                    for y in range(height - feature_height):
                                        x = top_left[0] - x
                                        y = top_left[1] + y
                                        fitur = HaarLikeFeature(feature, (x, y), feature_width, feature_height, 0)
                                        score = fitur.get_result(self.int_img)
                                        if score > 0:
                                            one_feature.append(fitur)
                        all_feature.append(one_feature)

                    print("Dapat semua feature")
                    for feature in all_feature:
                        print(len(feature))
                        if len(feature) > 0:
                            self.result.append(True)
                        else:
                            self.result.append(False)

                    print("Result:")
                    print(self.result)

    def reset_eksekusi(self):
        self.sudah_dieksekusi = False
        self.result = []


    def grab(self):
        # Jika gak gambar
        if not self.draw_rect:
            # Jika ditekan
            if self.button_down:
                # Simpan posnya
                self.draw_rect = True
                self.hide_rect = False
                self.first_mouse_pos = pygame.mouse.get_pos()
        # Jika lagi gambar
        else:
            # mouse di lepas
            if not self.button_down:
                self.draw_rect = False
            self.last_mouse_pos = pygame.mouse.get_pos()


    def get_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(event.pos):
                    self.button_down = True
                if event.button == 3:
                    self.hide_rect = True
                    self.reset_eksekusi()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.button_down = False




