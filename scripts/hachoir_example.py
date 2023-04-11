from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

parser = createParser(r'/mnt/d/Machine Vision/Sports Video CV/interview-detection/data/interim/BHS Baseball/00000.MTS')
metadata = extractMetadata(parser)
print(metadata)
