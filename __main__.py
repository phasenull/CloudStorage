import time

from classes.FileConverter import FileConverter as CFileConverter
FileConverter = CFileConverter()

binary = FileConverter.CONVERT_FILE_TO_BINARY("latest.log")
binary2 = FileConverter.CONVERT_BINARY_TO_VIDEO(binary,"example-clone-video.mp4")
# log = open("latest.log","w")
# log.write("org: " + binary + "\n\n\n" + "clone: " + binary2)
# log.close()
# file = FileConverter.ConvertBinaryToFile(binary,"example-clone-video.mp4")