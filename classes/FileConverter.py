import modules.Tools as tools
import cv2
import time
import os
import threading
from PIL import Image, ImageDraw


def time_function(func):
	def inner1(*args, **kwargs):
		start = time.time()
		print(f"Started {func.__name__} at {start} ")
		returned_value = func(*args, **kwargs)
		print(f"Finished {func.__name__} in {time.time() - start} seconds")
		return returned_value
	return inner1


class FileConverter():
	def __init__(self, threads: int = 10, video_fps: int = 30, video_res: tuple[int, int] = (256, 144), images_folder: str = "images") -> None:
		self.threads = threads
		self.fps = video_fps
		self.res = video_res
		self.images_folder = images_folder
		self.__chars_per_frame = self.res[0] * self.res[1]

	def handle_frame(self, frame: int, frames: int, chunk: str):
		img = Image.new(mode="RGB", size=self.res, color=(0, 255, 0))
		drawer = ImageDraw.Draw(img)
		# print("CHUNK_LENGTH:",len(chunk))
		canvas = [0, 0]
		for char_i in range(len(chunk)):
			char = chunk[char_i]
			color = char == "1" and (255, 255, 255) or (0, 0, 0)
			# print(char, " | ", str(color))
			drawer.point(canvas, color)
			canvas[0] += 1
			if (char_i + 1) % self.res[0] == 0:
				canvas[0] = 0
				canvas[1] += 1
		canvas[0] = self.res[0]
		print(f"{frame}\t({frames})\t{canvas[0]}\t{canvas[1]}")
		img.save(f"{self.images_folder}/frame_{frame+1}.png")
		img.close()

	@time_function
	def CONVERT_FILE_TO_BINARY(self, file_path: str):
		# test123w
		file = open(file_path, "rb")
		bytes = str(file.read())
		file.close()
		binary = tools.convert_string_to_binary(bytes)
		del bytes
		return binary

	@time_function
	def CONVERT_VIDEO_TO_BINARY(self, path: str) -> str:
		to_return = ""
		data = ""

		return to_return

	@time_function
	def CONVER_BINARY_TO_FILE(self, binary: str, path_to_save:str) -> str:
		path = path_to_save
		file = open(path_to_save, "wb")
		string = tools.convert_binary_to_string(binary)
		file.write(bytes(string, "utf-8"))
		file.close()
		string = None
		return binary
	
	@time_function
	def CONVERT_BINARY_TO_VIDEO(self, binary: str, path_to_save:str):
		started_at = time.time()
		frames = (len(binary) // self.__chars_per_frame) + \
			(len(binary) % self.__chars_per_frame != 0 and 1 or 0)
		print("Total Frames:", frames)
		print(
			f"Total Pixels : {len(binary)} ({self.__chars_per_frame} per frame)")
		threads = []
		for frame in range(frames):
			chunk = binary[frame * self.__chars_per_frame: (frame+1)*self.__chars_per_frame]
			thread = threading.Thread(target=self.handle_frame, args=[frame, frames, chunk])
			threads.append(thread)
			thread.start()
		for thread in threads:
			thread.join()
		print(f"Finished Rendering in {int((time.time()-started_at)*100)/100}")
		video_name = f'{path_to_save}'
		images = [img for img in os.listdir(
			self.images_folder) if img.endswith(".png")]
		images.sort()
		frame = cv2.imread(os.path.join(self.images_folder, images[0]))
		height, width, layers = frame.shape

		video = cv2.VideoWriter(video_name, 0, self.fps, (width, height))

		for image in images:
			video.write(cv2.imread(os.path.join(self.images_folder, image)))

		cv2.destroyAllWindows()
		video.release()
