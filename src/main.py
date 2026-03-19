import sys
import argparse
from typing import List
import json

# Create todo list app that supports 4 commands:
# - ADD <task_description>
# - REMOVE <task_id>
# - DONE <task_id>
# - LIST
# You can use the app via cli
# > ADD "Do laundry"
# Added "Do laundry" to the task list with id=1
# > LIST
# 1 [ ] "Do laundry"
# > DONE 1
# > LIST
# 1 [X] "Do laundry"
# > REMOVE 1
# > LIST
# No tasks on the list

class ToDoListError(Exception):
    """Wyjątek dla aplikacji ToDoList."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ToDoList:
    def __init__(self):
        self.list_of_to_dos = {}
        self.i = 0

    def dodaj(self,message):
        task = {"description": message, "done": False, "index": self.i}
        self.list_of_to_dos[self.i] = task
        self.i += 1


    def list_of_things(self) -> List[str]:
        list_of_strings = []
        for message in self.list_of_to_dos.values():
            # 1: [X?] <description>
            if(message["done"] == False):
                list_of_strings.append(str(message["index"])+":"+ "[ ]" +message["description"])
            else:
                list_of_strings.append(str(message["index"])+":"+ "[X]" +message["description"])
        return list_of_strings

    def remove_from_list(self,index):
        indexing = int(index)
        if indexing not in self.list_of_to_dos:
            raise ToDoListError('Cannot remove todo: no todo with index=0')
        del self.list_of_to_dos[indexing]



    def done(self,index):
        indexing = int(index)
        if indexing not in self.list_of_to_dos:
            raise ToDoListError(f'Cannot mark done todo: no todo with index= {index}')
        self.list_of_to_dos[indexing]['done'] = True
    #serializacja
    def save_to_file(self, filename):
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump({"i": self.i, "tasks": self.list_of_to_dos}, f, ensure_ascii=False, indent=2)
    #deserializacja
    def load_from_file(self, filename):
        try:
            self.list_of_to_dos, self.i  = odczytaj_z_pliku(filename)

        except (FileNotFoundError):
            self.list_of_to_dos = {}
            self.i = 0


        '''    
        def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding="utf-8") as f:
                data = json.load(f)
                print("tutaj data")
                print(data)
                self.i = data.get("i", 0)
                self.list_of_to_dos = {int(k): v for k, v in data.get("tasks", {}).items()}
        except (FileNotFoundError, json.JSONDecodeError):
            self.list_of_to_dos = {}
            self.i = 0
            
        '''
        #print("tutaj data po try")
        '''
        {
            'i': 3,
            'tasks': {
                '0': {'description': 'JEDEN', 'done': True, 'index': 0},
                '1': {'description': 'DWA', 'done': False, 'index': 1},
                '2': {'description': 'TRZY', 'done': False, 'index': 2}
            }
        }
        '''
        #print(data)



# Returns:
# { "name": "ADD", "description": "<parsed-description>" }
# { "name": "REMOVE", "index": <parsed-index>" }
# etc.
def parse_command(input_string):#ADD XD
    two_information = input_string.split(" ",1)
    name = two_information[0].upper()

    if(name == "ADD"):
        if len(two_information) < 2:
            raise ToDoListError("ADD requires a description")
        argument = two_information[1]
        return {"name" : name, "description" : argument}
    elif (name == "REMOVE"):
        argument = two_information[1]
        return {"name": name, "index": int(argument)}
    elif (name == "DONE"):
        argument = two_information[1]
        return {"name": name, "index": int(argument)}
    elif (name == "LIST"):
        return {"name": name}
    elif (name == "EXIT"):
        return {"name": name}
    else:
        raise ToDoListError('Unknown command {}'.format(input_string))

def clear_file(filename):
    with open(filename, "w", encoding="utf-8") as file:
        pass
def odczytaj_z_pliku(filename):
    list_of_to_dos = {}
    message = ""
    i=0
    with open(filename,'r') as file:
        linia = file.read()
        for element in linia.split("\n"):
            if element == "":
                break
            task = {"description": message, "done": False, "index": i}
            liczba_wartosc = element.split(":")
            czy_done_message = element.split("]")
            if czy_done_message[0][3] == "x" or czy_done_message[0][3] == "X":
                task["done"] = True
            else:
                task["done"] = False
            task["description"] = czy_done_message[1][1:len(czy_done_message[1])]
            task["index"] = int(liczba_wartosc[0])
            list_of_to_dos[i] = task
            i = i + 1
        return list_of_to_dos,i





if __name__ == '__main__':
    print("odczyt z pliku")
    list_of_to_dos , i = odczytaj_z_pliku('test.txt')
    print(i)
    print(list_of_to_dos)
    print("jestem w funkcji odczytaj z pliku")
    filename = sys.argv[1]
    print("Loaded database file:" , filename)


    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--clear", action="store_true")
    args = parser.parse_args()
    filename = args.file
    if args.clear:
        open(filename, "w", encoding="utf-8").close()
    else:
        print("Database contents:")
        todolist = ToDoList()
        todolist.load_from_file(filename)

        for item in todolist.list_of_things():
            print(item)

    todolist = ToDoList()
    todolist.load_from_file(filename)
    print("Use only words:" + "" + "ADD, LIST, REMOVE, EXIT, DONE")
    first_information = ""
    while (first_information != "EXIT"):
        try:
            print('>', end='')
            input_string = input()
            command = parse_command(input_string)

            if (command["name"] == "ADD"):
                todolist.dodaj(command["description"])
            if (command["name"] == "LIST"):
                lista = todolist.list_of_things()
                for l in lista:
                    print(l)

            if (command["name"] == "REMOVE"):
                todolist.remove_from_list(command["index"])
            if (command["name"] == "DONE"):
                todolist.done(command["index"])
            if (command["name"] == "EXIT"):
                todolist.save_to_file(filename)
                print("Dane zapisane do pliku.")
                break
        except ToDoListError as e:
            print("Błąd:", e)
        except ValueError:
            print("Błąd: id musi być liczbą")

