import pygame, sys, os
from pygame import surface
from pygame.locals import *

from warna import COLORS
from utils import get_all_image
from benda import Benda
from font_teks import FontText
from button import ButtonText


# Window
class Window:
	def __init__(self, screen_size):
		self.size = screen_size

		pygame.display.set_caption("Cek Feature")
		self.surface = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

		self.clock = pygame.time.Clock()
		self.run = True
		self.fps = 120

	def update(self):
		self.size = self.surface.get_size()
		self.surface.fill(COLORS.light_gray)

# buat Refresh
def load_img(all_path_img):
	all_imgs = []
	all_btns = []

	y = 20
	for img in all_path_img:
		nama = os.path.basename(img)
		all_imgs.append(Benda(nama, img, (300,100)))
		all_btns.append(ButtonText(nama, (20, y), color=(0,0,0), hover_color=(255,255,255)))
		y += 25

	return all_imgs, all_btns


def main():
	pygame.init()

	window = Window((1000, 640))

	FontText.update()

	all_path_img = get_all_image()
	# Benda, Button
	all_imgs, all_btns = load_img(all_path_img)

	# kosong
	current_img = -1

	while window.run:
		events = pygame.event.get()

		window.update()

		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

		# Perhitungan
		if current_img != -1:
			all_imgs[current_img].get_input(events)
			all_imgs[current_img].grab()
		ButtonText.handle_event(events)


		# Gambar
		# nama file
		for idx, btn in enumerate(all_btns):
			btn.render(window.surface)
			if btn.get_click():
				current_img = idx
		
		# gambarnya
		if current_img != -1:
			all_imgs[current_img].render(window.surface)
			if all_imgs[current_img].draw_rect or not all_imgs[current_img].hide_rect:
				all_imgs[current_img].render_rect(window.surface)


		window.clock.tick(window.fps)
		pygame.display.flip()


if __name__ == "__main__":
	main()

