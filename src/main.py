
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
    pass

class ToDoList:
    def __init__(self):
        self.list_of_to_dos = {}
        self.i = 0

    def dodaj(self,message):
        task = {"description": message, "done": False, "index": self.i}
        self.list_of_to_dos[self.i] = task
        self.i += 1


    def list_of_things(self):
        list_of_strings = []
        for message in self.list_of_to_dos.values():
            # 1: [X?] <description>
            if(message["done"] == False):
                list_of_strings.append(str(message["index"])+":"+ "[ ]" +message["description"])
            else:
                list_of_strings.append(str(message["index"])+":"+ "[X]" +message["description"])
        return list_of_strings

    def remove_from_list(self,index):
        if not index in self.list_of_to_dos:
            raise ToDoListError('Cannot remove todo: no todo with index=0')
        indexing = int(index)
        del self.list_of_to_dos[indexing]

    def done(self,index):
        indexing = int(index)
        if not index in self.list_of_to_dos:
            raise ToDoListError('Cannot mark done todo: no todo with index=0')

        self.list_of_to_dos[indexing]['done'] = True

# Returns:
# { "name": "ADD", "description": "<parsed-description>" }
# { "name": "REMOVE", "index": <parsed-index>" }
# etc.
def parse_command(input_string):#ADD XD
    two_information = input_string.split(" ")
    name = two_information[0]

    if(name == "ADD"):
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


if __name__ == '__main__':
    todolist = ToDoList()
    print("Use only words:"+""+"ADD, LIST, REMOVE, EXIT")
    first_information = ""
    while (first_information != "EXIT"):
        print('>', end='')
        input_string = input()
        command = parse_command(input_string)

        if(command["name"] == "ADD"):
            todolist.dodaj(command["description"])
        if(command["name"] == "LIST"):
            lista = todolist.list_of_things()
            for l in lista:
                print(l)

        if( command["name"]== "REMOVE"):
            todolist.remove_from_list(command["index"])
        if(command["name"] == "DONE"):
            todolist.done(command["index"])
