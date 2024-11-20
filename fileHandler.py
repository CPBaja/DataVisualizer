import os
import pandas as pd

class FileHandler:

	def __init__(self):

		self.open_files = []
		self.file_names = []


	def openFile(self, path):

		df = pd.read_csv(path,skiprows=5)
		self.open_files.append(df)
		self.file_names.append(path.split('/')[1].split('.')[0])

	def listOpenFiles(self):

		print("Open files:")

		for file in self.file_names:
			print(file)

		print()

	
	def getFile(self, filename):

		for i in range(len(self.file_names)):
			if self.file_names[i] is filename:
				break
		return self.open_files[i]

