if __name__ == '__main__':
	import time
	from classes.FileConverter import FileConverter as CFileConverter
	FileConverter = CFileConverter(10,video_res=(1920,1080))

	job_id,job_length = FileConverter.CONVERT_FILE_TO_BINARY("input.txt")
	binary2 = FileConverter.CONVERT_BINARY_TO_VIDEO(job_id,"output.mp4",job_length)