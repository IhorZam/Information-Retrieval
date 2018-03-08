with open('/home/ihorzam/Work/PythonFiles/Ready/ByteTest', 'wb') as byteTest:
    bitstring = '1100000001010'
    n = int(bitstring, 2)
    n = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    byteTest.write(n)

with open('/home/ihorzam/Work/PythonFiles/Ready/ByteTest', 'rb') as byteTestRead:
    print("{0:b}".format(int.from_bytes(byteTestRead.readline(), byteorder='big')))