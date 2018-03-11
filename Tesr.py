def decoder(line):
    zsuv_length = 0
    result_line = ""
    aux_byte = "1"
    i = 0
    line = line[1:]
    while i < len(line):
        if line[i] == '0' and zsuv_length == 0:
            result_line += aux_byte + " "
            i += 1
        elif line[i] == '1':
            zsuv_length += 1
            i += 1
        elif line[i] == '0':
            if i + zsuv_length > len(line):
                continue
            i += 1
            for j in range(i, zsuv_length + i):
                aux_byte += line[j]
            result_line += str(int(aux_byte, 2)) + " "
            aux_byte = "1"
            i = i + zsuv_length
            zsuv_length = 0
    return result_line


with open('/home/ihorzam/Work/PythonFiles/Ready/LastResult', 'rb') as byteTestRead:
    with open('/home/ihorzam/Work/PythonFiles/Ready/LastResult.txt', 'w') as res:
        res.write(decoder("{0:b}".format(int.from_bytes(byteTestRead.readline(), byteorder='big'))))
