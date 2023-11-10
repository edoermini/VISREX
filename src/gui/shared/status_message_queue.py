from PyQt6.QtCore import QMutex, QMutexLocker

class StatusMessagesQueue:
	def __init__(self):
		self.mutex = QMutex()
		self.messages = []
		self.current_message_index = 0
	
	def add(self, message:str) -> int:
		with QMutexLocker(self.mutex):
			index = len(self.messages)
			self.messages.append(message)

		return index
	
	def remove(self, index:int) -> None:
		with QMutexLocker(self.mutex):
			self.messages.pop(index)
	
	def get_message_rotation(self) -> (str | None):
		with QMutexLocker(self.mutex):
			if len(self.messages) == 0:
				return None
			
			message = self.messages[self.current_message_index]
			# Move to the next message in the list
			self.current_message_index = (self.current_message_index + 1) % len(self.messages)

		return message