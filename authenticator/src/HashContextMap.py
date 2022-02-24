
#Singletone
class HashContextMap(dict):
   __instance = None

   @staticmethod 
   def getInstance():
      """ Static access method. """
      if HashContextMap.__instance == None:
        HashContextMap()
      return HashContextMap.__instance

   def __init__(self):
      """ Virtually private constructor. """
      if HashContextMap.__instance != None:
         raise Exception("This class is a singletone!")
      else:
         HashContextMap.__instance = self



s = HashContextMap()