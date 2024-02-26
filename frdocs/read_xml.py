import gzip
from msgpack import load

def read_xml_gz():
    with gzip.open(r"C:\Users\qazcd\Desktop\infovisor\downlaod_fr\data\raw\xml\2024-01-05.xml.gz") as f:
        result = f.readlines()

        for line in result[:20]:
            print(line)

def read_msgpack():
    with open(r"C:\Users\qazcd\Desktop\infovisor\download_fr\data\agenda\2023-04\0331-AA06.msgpack", 'rb') as f:
        data = load(f)
        print(data)

#read_xml_gz()
read_msgpack()