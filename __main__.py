if __name__ == '__main__':
	import time
	from classes.FileConverter import FileConverter as CFileConverter
	FileConverter = CFileConverter(10,video_res=(1920,1080))

	job_id,job_length = FileConverter.CONVERT_FILE_TO_BINARY("latest.log")
	binary2 = FileConverter.CONVERT_BINARY_TO_VIDEO(job_id,"output.mp4",job_length)
	# log = open("latest.log","w")
	# log.write("org: " + binary + "\n\n\n" + "clone: " + binary2)
	# log.close()
	# file = FileConverter.ConvertBinaryToFile(binary,"example-clone-video.mp4")