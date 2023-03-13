if __name__ == '__main__':
	from classes.FileConverter import FileConverter as CFileConverter
	FileConverter = CFileConverter(10,video_res=(8,8))
	input_video = "inputs/source_code.txt"
	output_video = "inputs/source_output.mp4"
	job_id,job_length,bytes = FileConverter.CONVERT_FILE_TO_BINARY(input_video)
	print(bytes) # works as expected
	binary2 = FileConverter.CONVERT_BINARY_TO_VIDEO(job_id,output_video,job_length)
	video = FileConverter.CONVERT_VIDEO_TO_BINARY(output_video,f"output/converted.{input_video[7:]}")