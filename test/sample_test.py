from src.main import ToDoList, ToDoListError, parse_command

import unittest

class TestParseCommand(unittest.TestCase):
    def test_parse_add_with_spaced_description(self):
        komenda = parse_command("ADD dodaj testy dla parse_command")
        assert komenda["name"] == "ADD"
        assert komenda["description"] == "dodaj testy dla parse_command"

    def test_parse_add(self):
        komenda = parse_command("ADD XD")
        assert komenda["name"]=="ADD"
        assert komenda["description"] == "XD"

    def test_remove(self):
        komenda = parse_command("REMOVE 0")
        assert komenda["name"]=="REMOVE"

        assert komenda["index"] == 0

    def test_done_test(self):
        komenda = parse_command("DONE 0")
        assert komenda["name"]=="DONE"
        assert komenda["index"] == 0

    def  test_list(self):
        komenda = parse_command("LIST")
        assert komenda["name"]=="LIST"
        assert not "index" in komenda
        assert not "description" in komenda

    def test_exists(self):
        komenda = parse_command("EXIT")
        assert komenda["name"]=="EXIT"
        assert not "index" in komenda
        assert not "description" in komenda


# def parse_command(input_string):  # ADD XD
#       two_information = input_string.split(" ")
#      name = two_information[0]
#     description = two_information[1]
#    return {"name": name, "description": description}


class TestToDo(unittest.TestCase):
    def test_add_to_do(self):
        todos = ToDoList()
        todos.dodaj("XD")
        assert todos.list_of_to_dos[0]["description"] == "XD"
        assert todos.list_of_to_dos[0]["done"] == False

    def test_add_to_do2(self):
        todos = ToDoList()
        todos.dodaj("XDD")
        assert todos.list_of_to_dos[0]["description"] == "XDD"
        assert todos.list_of_to_dos[0]["done"] == False

    def test_remove_non_existing(self):
        todos = ToDoList()
        with self.assertRaises(ToDoListError) as context:
            todos.remove_from_list(0)

        self.assertTrue('Cannot remove todo: no todo with index=0' in str(context.exception))

    def test_done_non_exiting(self):
        todos = ToDoList()
        with self.assertRaises(ToDoListError) as context:
            todos.done(0)
        self.assertTrue('Cannot mark done todo: no todo with index=0' in str(context.exception))



    def test_full_todo_flow(self):
        todos = ToDoList()
        todos.dodaj("LOL")
        todos.done(0)
        assert todos.list_of_to_dos[0]["done"] == True
        todos.remove_from_list(0)
        assert todos.list_of_to_dos == {}
        todos.dodaj("LOL")#INDEKS1
        todos.dodaj("XD")
        todos.dodaj("LOL2")
        assert len(todos.list_of_to_dos) == 3

        assert todos.list_of_to_dos[1]["description"] == "LOL"
        assert todos.list_of_to_dos[2]["description"] == "XD"
        assert todos.list_of_to_dos[3]["description"] == "LOL2"

        x = todos.list_of_things()
        print(x[0])
        assert len(todos.list_of_to_dos) == 3
        assert x[0] == "1:[ ]LOL"
        assert x[1] == "2:[ ]XD"
        assert x[2] == "3:[ ]LOL2"

        todos.done(2)
        assert todos.list_of_to_dos[2]["done"] == True

        y = todos.list_of_things()
        assert y[0] == "1:[ ]LOL"
        assert y[1] == "2:[X]XD"
        assert y[2] == "3:[ ]LOL2"




