#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def validate(arg):
    """this function bulids custom commands line arguments"""
    return arg.split()


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """
    prompt = "(hbnb)"
    classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
            ]

    def default(self, line):
        """
        Handles cases where user commands are not recognized by HBNBConsole.

        This method is invoked when the user enters a command
        that doesn't match any of the defined functionalities in HBNBConsole.
        It checks for a pattern matching "<class_name>.<method>(<args>)"
        and attempts to call the corresponding do_* method if valid.
        Otherwise, it prints an error message.

        Args:
        -   line (str): The user input command string.
        """
        commands = {
            "create": self.do_create,
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }

        pattern = r"^(\w+)\.(\w+)\((.*)\)$"
        matched = re.match(pattern, line)

        if not matched:
            super().default(line)
            return

        cmd = matched.groups()
        args = ""
        method = cmd[1]
        cls_name = cmd[0]

        if method not in commands:
            print(error_messages["no_method"])
            return

        if method in ("all", "create", "count"):
            commands[method](cls_name)
            return
        
        obj_id = cmd[2]
        args = f"{cls_name} {obj_id}"
        if method in ("show", "destroy"):
            commands[method](args)
            return

        obj_id = cmd[2].split(',')[0]
        attr_name = cmd[2].split(',')[1] if len(cmd[2].split(',')) > 1 else ""
        attr_value = cmd[2].split(',')[2] if len(cmd[2].split(',')) > 2 else ""
        args = f"{cls_name} {obj_id} {attr_name} {attr_value}"
        if method == "update":
            commands[method](args)
            return

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def emptyline(self):
        """DO nothing upon receving an empty line."""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel
        saves it (to the JSON file) and prints the id"""
        args = validate(arg)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            print(eval(args[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id"""
        args = validate(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[f"{args[0]}.{args[1]}"])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        (save the change into the JSON file)"""
        args = validate(arg)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[f"{args[0]}.{args[1]}"]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances
        based or not on the class name"""
        args = validate(arg)

        if len(args) > 0 and args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(args) > 0 and args[0] == type(obj).__name__:
                    obj_list.append(obj.__str__())
                elif len(args) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file)"""
        args = validate(arg)
        obj_dict = storage.all()

        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args) == 4:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = valtype(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            for k, v in eval(args[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """retrieve the number of instances of a class"""
        args = validate(arg)
        if not args:
            return

        num_instances = 0
        for instance in storage.all().values():
            if validate(arg)[0] == type(instance).__name__:
                num_instances += 1

        print(num_instances)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
