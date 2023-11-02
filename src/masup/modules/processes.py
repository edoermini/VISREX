from pymem import Pymem
import mmap

class Process:
    def __init__(self, process_name):
        self.process_name = process_name
        self.pm = Pymem(self.process_name)
    
    def extract_memory(self, start_address, bytes_number=mmap.PAGESIZE):
        return self.pm.read_bytes(start_address, bytes_number)