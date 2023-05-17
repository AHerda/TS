from warnings import warn

FLAG = "01111110"
GEN = "1001"

### Kodowanie

def crc(data: str, add_zeros: bool) -> str:
    if add_zeros:
        data += "0" * (len(GEN) - 1)
    temp = data[:len(GEN)]

    while len(data) >= len(GEN):
        if temp[0] == "1":
            temp = bin(int(temp, 2) ^ int(GEN, 2))[2:].zfill(len(temp))
        
        temp = temp[1:]
        if len(data) > len(GEN):
            temp += data[len(GEN)]
        
        data = data[1:]
    
    return temp

def preventFlags(data: str) -> str:
    result = ""
    counter = 0

    for bit in data:
        result += bit

        if bit == "1":
            counter += 1
        else:
            counter = 0
        if counter == 5:
            result += "0"
    
    return result

def encode(data: str, datasize = 32) -> str:
    frames = []
    for i in range(0, len(data), 32):
        frame = data[i: min(i + datasize, len(data))]
        frame += crc(frame, True)
        frame = preventFlags(frame)
        frames.append(FLAG + frame + FLAG)
    return "".join(frames)


### Ddekodowanie

def filterPreventFlags(data: str) -> str:
    result = ""
    parts = data.split("111110")
    for i in range(len(parts)):
        if len(parts[i]) == 0:
            result += "11111"
        else:
            result += parts[i]
            if i + 1 != len(parts):
                result += "11111"

    return result

def decode(data: str) -> str:
    frames = list(filter(None, data.split(FLAG)))
    decoded = []

    for frame in frames:
        frame = filterPreventFlags(frame)
        if crc(frame, False) != "0" * (len(GEN) - 1):
            warn("Frame containing {} is wrong".format(frame))
        else:
            frame = frame[:-(len(GEN) - 1)]
            decoded.append(frame)
    
    return "".join(decoded)

x = "0111111010101011111"
print(x)
x = encode(x)
print(x)
x = decode(x)
print(x)