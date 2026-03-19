import argparse
import json
import sys

from typing import List


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

    def dodaj(self, message):
        task = {"description": message, "done": False, "index": self.i}
        self.list_of_to_dos[self.i] = task
        self.i += 1

    def list_of_things(self) -> List[str]:
        """
        Creates representation of todol list items in format: <int>: [<status>] <description>.
        Example: 1: [X] Do laundry
        :return: List of string descriptions of items
        """
        list_of_strings = []
        for message in self.list_of_to_dos.values():
            status_mark = "X" if message["done"] else " "
            represent = f"{message['index']}:[{status_mark}]{message['description']}"
            list_of_strings.append(represent)
        return list_of_strings

    def remove_from_list(self, index: str) -> None:
        indexing = int(index)
        if indexing not in self.list_of_to_dos:
            raise ToDoListError('Cannot remove todo: no todo with index=0')
        del self.list_of_to_dos[indexing]

    def done(self, index: str) -> None:
        indexing = int(index)
        if indexing not in self.list_of_to_dos:
            raise ToDoListError(f'Cannot mark done todo: no todo with index= {index}')
        self.list_of_to_dos[indexing]['done'] = True

    # serializacja
    def save_to_file(self, filename: str) -> None:
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump({"i": self.i, "tasks": self.list_of_to_dos}, f, ensure_ascii=False, indent=2)

    # deserializacja
    def load_from_file(self, filename: str) -> None:
        try:
            with open(filename, 'r', encoding="utf-8") as f:
                data = json.load(f)
                self.i = data.get("i", 0)
                self.list_of_to_dos = {}
                for k, v in data.get("tasks", {}).items():
                    self.list_of_to_dos[int(k)] =  v
        except (FileNotFoundError, json.JSONDecodeError):
            print("File not found, starting from scratch...")
            self.list_of_to_dos = {}
            self.i = 0


# Returns:
# { "name": "ADD", "description": "<parsed-description>" }
# { "name": "REMOVE", "index": <parsed-index>" }
# etc.
def parse_command(input_string):  # ADD XD
    two_information = input_string.split(" ", 1)
    name = two_information[0].upper()

    if (name == "ADD"):
        if len(two_information) < 2:
            raise ToDoListError("ADD requires a description")
        argument = two_information[1]
        return {"name": name, "description": argument}
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


if __name__ == '__main__':
    filename = sys.argv[1]
    print("Loaded database file:", filename)

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
