BITS = 8
import time
import threading
import multiprocessing
def time_function(func):
	def inner1(*args, **kwargs):
		start = time.time()
		#print(f"Started {func.__name__} at {start} ")
		returned_value = func(*args, **kwargs)
		print(f"Finished {func.__name__} in {time.time() - start} seconds")
		return returned_value
	return inner1

def __fit_to_bits(binary:str) -> str:
	return "0"*(BITS-len(binary)) + binary

def CONVERT_CHARACTER_TO_BINARY(character: str) -> str:
	return __fit_to_bits(bin(ord(character))[2:])


def __convert_binary_chunk_to_character(string: str) -> str:
	ascii = 0
	for i in range(len(string)):
		ascii += int(string[-i-1])*(2**abs(i))
	return chr(ascii)


def save_binary_chunk(chunk_index : int, chunk : str,job_id):
	file = open(f"bin/{job_id}_{chunk_index}.BINARY_CHUNK","w")
	file.write(chunk)
	file.close()

def __handle_chunk(chunk_i : int,chunk_size : int,chunk : str,job_id : str):
	save_binary_chunk(chunk_i,"".join([CONVERT_CHARACTER_TO_BINARY(char) for char in chunk]),job_id)
@time_function
def CONVERT_STRING_TO_BINARY(string:str,chunk_size : int = 36_864,max_threads : int = 10):
	live_threads = []
	thread_count = 0
	string_length = len(string)
	job_id = f"job_{int(time.time())}"
	total_threads = string_length // chunk_size + (string_length % chunk_size != 0 and 1 or 0)
	for i in range(total_threads):
		print(f"Converting String To Binary: {i}/{total_threads}")
		thread = multiprocessing.Process(target=__handle_chunk,args=[i,	chunk_size,	string[i*chunk_size:(i+1)*chunk_size],	job_id	])
		thread.start()
		live_threads.append(thread)
		thread_count += 1
		if thread_count % max_threads == 0:
			print(f"THREAD LOCK {thread_count} / {total_threads}")
			for thread in live_threads:
				thread.join()
				live_threads.remove(thread)
		for thread in live_threads:
			thread.join()
	return job_id,total_threads

def __convert_binary_group_to_string(list:list[str]) -> str:
	string = "".join([__convert_binary_chunk_to_character(i) for i in list])
	return string
def CONVERT_BINARY_TO_STRING(binary:str) -> str:
	return __convert_binary_group_to_string(__split_binary_chunk(binary))
def __split_binary_chunk(string:str) -> list[str]:
	chunk = []
	for i in range(len(string) // BITS):
		chunk.append(string[i*BITS : (i+1)*BITS])
	return chunk