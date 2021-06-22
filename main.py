import pygame, sys, os
from pygame.locals import *

from warna import COLORS
from utils import get_all_image, BoxBergerak
from benda import Benda
from button import ButtonText
from input_box import InputBox
from font_teks import FontText


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
def load_img(all_path_img, width, height):
	all_imgs = []
	all_btns = []

	y = 20
	for img in all_path_img:
		nama = os.path.basename(img)
		all_imgs.append(Benda(nama, img, (width/2, height/2)))
		all_btns.append(ButtonText(nama, (20, y), color=(0,0,0), hover_color=(255,255,255)))
		y += 25

	return all_imgs, all_btns


def main():
	pygame.init()

	window = Window((1000, 640))

	images_path = os.path.join(os.getcwd(), 'images')
	all_path_img = get_all_image(images_path)
	# Benda, Button
	all_imgs, all_btns = load_img(all_path_img, window.size[0], window.size[1])

	# kosong
	current_img = -1
	threshold_box = InputBox((200, 20), (50, 20), Benda.threshold, title="Threshold", text_color=COLORS.black, hover_color=COLORS.dark_gray, active_color=COLORS.white, text_size=22)

	option_teks = FontText.font_normal.render("Options", True, COLORS.black)
	option_box = BoxBergerak((150, 50), (200, 200), COLORS.deepskyblue)

	width_feature = Benda.max_feature_width
	height_feature = Benda.max_feature_height
	feature_box = BoxBergerak((400, 50), (width_feature, height_feature), COLORS.green_shade)

	min_width_box = InputBox((0, 0), (50, 20), Benda.min_feature_width, title="Min Width", text_color=COLORS.black, hover_color=COLORS.dark_gray, active_color=COLORS.white, text_size=22)
	max_width_box = InputBox((0, 0), (50, 20), Benda.max_feature_width, title="Max Width", text_color=COLORS.black, hover_color=COLORS.dark_gray, active_color=COLORS.white, text_size=22)
	min_height_box = InputBox((0, 0), (50, 20), Benda.min_feature_height, title="Min Height", text_color=COLORS.black, hover_color=COLORS.dark_gray, active_color=COLORS.white, text_size=22)
	max_height_box = InputBox((0, 0), (50, 20), Benda.max_feature_height, title="Max Height", text_color=COLORS.black, hover_color=COLORS.dark_gray, active_color=COLORS.white, text_size=22)

	r_teks = FontText.font_normal.render("Right Click for Reset", True, COLORS.black)
	box_teks = FontText.font_normal.render("Green box is Max Feature size", True, COLORS.black)


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
		option_box.get_input(events)
		option_box.grab()

		feature_box.rect.width = Benda.max_feature_width
		feature_box.rect.height = Benda.max_feature_height
		feature_box.get_input(events)
		feature_box.grab()

		y = 50
		for i_box in InputBox.all_input_box:
			i_box.pos.x = option_box.pos.x + 20
			i_box.pos.y = option_box.pos.y + y
			y += 25

		InputBox.handle_event(events)
		ButtonText.handle_event(events)

		if min_width_box.change:
			Benda.min_feature_width = min_width_box.value
			min_width_box.change = False
		if max_width_box.change:
			Benda.max_feature_width = max_width_box.value
			max_width_box.change = False
		if min_height_box.change:
			Benda.min_feature_height = min_height_box.value
			min_height_box.change = False
		if max_height_box.change:
			Benda.max_feature_height = max_height_box.value
			max_height_box.change = False

		if current_img != -1:
			if threshold_box.change:
				all_imgs[current_img].threshold = threshold_box.value
				threshold_box.change = False
			all_imgs[current_img].get_input(events)
			all_imgs[current_img].grab()
			all_imgs[current_img].eksekusi_haar()


		# Gambar
		# gambarnya
		if current_img != -1:
			all_imgs[current_img].render(window.surface)
			if all_imgs[current_img].draw_rect or not all_imgs[current_img].hide_rect:
				all_imgs[current_img].render_rect(window.surface)

		# nama file
		for idx, btn in enumerate(all_btns):
			btn.render(window.surface)
			if btn.get_click():
				current_img = idx

		# Box
		option_box.render(window.surface)
		feature_box.render(window.surface)

		# Option
		xy_option = (option_box.pos.x + 25, option_box.pos.y + 20)
		window.surface.blit(option_teks, xy_option)
		for i_box in InputBox.all_input_box:
			i_box.render(window.surface)
		
		# Info
		window.surface.blit(r_teks, (20, window.size[1] - 50))
		window.surface.blit(box_teks, (20, window.size[1] - 30))

		window.clock.tick(window.fps)
		pygame.display.flip()


if __name__ == "__main__":
	main()

