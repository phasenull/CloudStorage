import modules.Tools as tools
import cv2
import time	
import os
import threading
from PIL import Image, ImageDraw
FPS = 60
RES = (256,144)
CHARS_PER_FRAME = RES[0] * RES[1]
image_folder = 'images'
class FileConverter():
	def handle_frame(self,frame:int,frames:int,chunk:str):
		img = Image.new(mode = "RGB",size = RES,color = (0,255,0))
		drawer = ImageDraw.Draw(img)
		# print("CHUNK_LENGTH:",len(chunk))
		canvas = [0,0]
		for char_i in range(len(chunk)):
			char = chunk[char_i]
			color = char == "1" and (255,255,255) or (0,0,0)
			# print(char, " | ", str(color))
			drawer.point(canvas,color)
			canvas[0] += 1
			if (char_i + 1) % RES[0] == 0:
				canvas[0] = 0
				canvas[1] += 1
		canvas[0] = RES[0]
		print(f"{frame}\t({frames})\t{canvas[0]}\t{canvas[1]}")
		img.save(f"{image_folder}/frame_{frame+1}.png")
		img.close()

	def __init__(self):
		return
	def ConvertFileToBinary(self,fp:str):
		file = open(fp,"rb")
		bytes = str(file.read())
		file.close()
		binary = tools.convert_string_to_binary(bytes)
		bytes = None
		return binary
	def ConvertVideoToBinary(self,path:str) -> str:
		to_return = ""
		data = ""
		
		return to_return

	def ConverBinaryToFile(self,binary:str,path_to_save:str) -> str:
		path = path_to_save
		file = open(path_to_save,"wb")
		string = tools.convert_binary_to_string(binary)
		file.write(bytes(string,"utf-8"))
		file.close()
		string = None
		return binary
	def ConvertBinaryToVideo(self,binary:str,path_to_save:str):
		started_at = time.time()
		frames = (len(binary) // CHARS_PER_FRAME) + (len(binary) % CHARS_PER_FRAME != 0 and 1 or 0)
		print("Total Frames:",frames)
		print(f"Total Pixels : {len(binary)} ({CHARS_PER_FRAME} per frame)")
		threads = []
		for frame in range(frames):
			chunk = binary[frame*CHARS_PER_FRAME : (frame+1)*CHARS_PER_FRAME]
			thread = threading.Thread(target=self.handle_frame,args=[frame,frames,chunk])
			threads.append(thread)
			thread.start()
		for thread in threads:
			thread.join()
		print(f"Finished Rendering in {int((time.time()-started_at)*100)/100}")
		video_name = f'{path_to_save}'
		images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
		images.sort()
		frame = cv2.imread(os.path.join(image_folder, images[0]))
		height, width, layers = frame.shape

		video = cv2.VideoWriter(video_name, 0, FPS, (width,height))

		for image in images:
			video.write(cv2.imread(os.path.join(image_folder, image)))

		cv2.destroyAllWindows()
		video.release()