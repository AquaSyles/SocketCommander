import pickle
command = input("Write command: ")
command = command.split(" ")
dictionary = {'command': command[0], "parameters": command[1:]}

print(dictionary)
