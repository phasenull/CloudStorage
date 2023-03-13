import modules.Tools as tools
from modules.Tools import time_function
import cv2
import time
import os
from PIL import Image, ImageDraw
import shutil
import threading
import multiprocessing
class FileConverter():
	def __init__(self, threads: int = 10, video_fps: int = 30, video_res: tuple[int, int] = (256, 144), images_folder: str = "images") -> None:
		self.threads = threads
		self.fps = video_fps
		self.res = video_res
		self.images_folder = images_folder
		self.__chars_per_frame = self.res[0] * self.res[1]
		self.clear()
		print(f"Init with params: [threads={self.threads},fps={self.fps}],res={self.res},images_folder={self.images_folder}]")
	def clear(self):
		print("CLEARING")
		path = self.images_folder
		if os.path.exists("bin"):
			shutil.rmtree("bin")
		if os.path.exists(path):
			shutil.rmtree(path)
		if os.path.exists("output.mp4"):
			os.remove("output.mp4")
		print("CLEARED")
		self.makedir()
	def makedir(self):
		os.mkdir("bin")
		os.mkdir(self.images_folder)
	def Handle_frame(self, frame: int, frames: int, job_id: str):
		chunk_id = f"{job_id}_{frame}.BINARY_CHUNK"
		chunk_f = open(f"bin/{chunk_id}","r")
		chunk = chunk_f.read()
		chunk_f.close()
		img = Image.new(mode="RGB", size=self.res, color=(0, 255, 0))
		drawer = ImageDraw.Draw(img)
		# print("CHUNK_LENGTH:",len(chunk))
		chunk_len = len(chunk)
		canvas = [0, 0]
		for char_i in range(chunk_len):
			char = chunk[char_i]
			color = char == "1" and (255, 255, 255) or (0, 0, 0)
			drawer.point(canvas, color)
			canvas[0] += 1
			if (char_i + 1) % self.res[0] == 0:
				canvas[0] = 0
				canvas[1] += 1
		canvas[0] = self.res[0]
		#print(f"{frame}\t({frames})\t{canvas[0]}\t{canvas[1]}")
		img.save(f"{self.images_folder}/frame_{frame+1}.png")
		img.close()

	@time_function
	def CONVERT_FILE_TO_BINARY(self, file_path : str):
		file = open(file_path, "rb")
		bytes = str(file.read())[2:-1:]
		file.close()
		print("Finished Reading")
		print("Started Converting To Binary")
		job_id,job_length = tools.CONVERT_STRING_TO_BINARY(bytes,chunk_size=self.__chars_per_frame,max_threads=self.threads)
		del file
		return job_id,job_length,bytes
	def Handle_VtF_image(self,image_path,job_id,job_index):
		image = Image.open(image_path)
		canvas = [0,0]
		binary_chunk = ""
		for i in range(image.size[0] * image.size[1]):
			color : tuple[int,int,int] = image.getpixel(tuple(canvas))
			binary_chunk += (color == (0,0,0) and "0") or (color == (255,255,255) and "1") or ""
			canvas[0] += 1
			if canvas[0] % image.size[0] == 0:
				canvas[0] = 0
				canvas[1] += 1
		binary_chunk = tools.CONVERT_BINARY_TO_STRING(binary_chunk)
		del image

		# SAVE

		folder_location = "bin"
		output_chunk_location = f"{folder_location}/{job_id}_{job_index}.BYTE_CHUNK"
		file = open(output_chunk_location,"w")
		file.write(binary_chunk)
		file.close()

	@time_function
	def CONVERT_VIDEO_TO_BINARY(self, input_video: str,output_path: str):
		video = cv2.VideoCapture(input_video)
		success,image = video.read()
		i = 0
		job_id = int(time.time())
		while success:
			cv2.imwrite(f"{self.images_folder}/V_F_{job_id}_{i}.png", image)
			success, image = video.read()
			i += 1
		print(f"Rendered Video to File images ({i})")
		images = sorted(os.listdir(self.images_folder))
		images_len = len(images)
		thread_count = 0
		live_threads = []
		for path in images:
			if not path.startswith("frame_"):
				images_len += -1
				continue
			print(f"{thread_count}\t({images_len})")
			thread = multiprocessing.Process(target=self.Handle_VtF_image, args=["images/"+path, job_id,thread_count])
			thread.start()
			live_threads.append(thread)
			thread_count += 1
			if thread_count % self.threads == 0:
				print(f"THREAD LOCK {thread_count+1} / {images_len}")
				for thread in live_threads:
					thread.join()
					live_threads.remove(thread)
		for thread in live_threads:
			thread.join()
		
		final_video = open(output_path,"wb")
		byte_chunks = os.listdir("bin")
		for i in byte_chunks:
			if i.endswith(".BYTE_CHUNK"):
				read_chunk = open("bin/"+i,"r")
				final_video.write(bytes(read_chunk.read(),"utf-8"))
				read_chunk.close()
		final_video.close()
		print("FINAL VIDEO RENDERED!")
		return final_video.name

	@time_function
	def CONVER_BINARY_TO_FILE(self, binary: str, path_to_save:str) -> str:
		path = path_to_save
		file = open(path_to_save, "wb")
		string = tools.CONVERT_BINARY_TO_STRING(binary)
		file.write(bytes(string.replace("Three","selam"), "utf-8"))
		del string
		file.close()
		return binary
	
	@time_function
	def CONVERT_BINARY_TO_VIDEO(self, job_id : str, path_to_save:str,frames : int):
		started_at = time.time()
		print("Total Frames:", {frames})
		print(f"Total Pixels : {frames * self.__chars_per_frame} ({self.__chars_per_frame} per frame)")
		live_threads = []
		thread_count = 0
		for frame in range(frames):
			print(f"{frame}\t({frames})")
			thread = multiprocessing.Process(target=self.Handle_frame, args=[frame, frames, job_id])
			thread.start()
			live_threads.append(thread)
			thread_count += 1
			if thread_count % self.threads == 0:
				print(f"THREAD LOCK {thread_count+1} / {frames}")
				for thread in live_threads:
					thread.join()
					live_threads.remove(thread)
		for thread in live_threads:
			thread.join()
		print(f"Finished Rendering in {int((time.time()-started_at)*100)/100}")
		video_name = f'{path_to_save}'
		images = [img for img in os.listdir(
			self.images_folder) if img.endswith(".png")]
		images.sort()
		video = cv2.VideoWriter(video_name, 0, self.fps, (self.res[0], self.res[1]))
		for image in images:
			video.write(cv2.imread(os.path.join(self.images_folder, image)))
		cv2.destroyAllWindows()
		video.release()
		return video