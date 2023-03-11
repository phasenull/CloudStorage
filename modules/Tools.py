BITS = 8
def __fit_to_bits(binary:str) -> str:
	return "0"*(BITS-len(binary)) + binary

def convert_character_to_binary(character: str) -> str:
	character = str(character)	
	return __fit_to_bits(bin(ord(character))[2:])


def convert_binary_chunk_to_character(string: str) -> str:
	ascii = 0
	for i in range(len(string)):
		ascii += int(string[-i-1])*(2**abs(i))
	return chr(ascii)

def convert_string_to_binary(string:str):
	chunk = []
	for char in string:
		chunk.append(convert_character_to_binary(char))
	return "".join([str(i) for i in chunk])

def convert_binary_group_to_string(list:list[str]) -> str:
	string = ""
	for i in list:
		string += convert_binary_chunk_to_character(i)
	return string
def convert_binary_to_string(binary:str) -> str:
	return convert_binary_group_to_string(split_binary_chunk(binary))
def split_binary_chunk(string:str) -> list[str]:
	chunk = []
	for i in range(len(string) // BITS):
		chunk.append(string[i*BITS : (i+1)*BITS])
	return chunk