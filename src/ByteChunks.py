class ByteChunks:
	def __iter__(self) -> Iterable[bytes]: ...
	def getChunky(self, chunk_size = 0) -> Iterable[bytes]: ...
	@property
	def get(self): return b"".join(self);
pass

class SimpleByteChunks(ByteChunks):
	def __init__(self, data: bytes):
		self.data = data;
	pass
	def __iter__(self): return (self.data,);
	def getChunky(self, chunk_size = 0):
		if chunk_size == 0: return (self.data,);
		return (
			self.data[i : i + chunk_size] 
			for i in range(0, len(self.data), chunk_size)
		);
	pass
pass
