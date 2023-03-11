from classes.FileConverter import FileConverter as CFileConverter
FileConverter = CFileConverter()
binary = FileConverter.ConvertFileToBinary("latest.log")
binary2 = FileConverter.ConvertBinaryToVideo(binary,"example-clone-video.mp4")
# log = open("latest.log","w")
# log.write("org: " + binary + "\n\n\n" + "clone: " + binary2)
# log.close()
# file = FileConverter.ConvertBinaryToFile(binary,"example-clone-video.mp4")