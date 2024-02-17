import gzip

def read_xml_gz():
    with gzip.open(r"C:\Users\qazcd\Desktop\infovisor\downlaod_fr\data\raw\xml\2024-01-05.xml.gz") as f:
        result = f.readlines()

        for line in result[:20]:
            print(line)

read_xml_gz()