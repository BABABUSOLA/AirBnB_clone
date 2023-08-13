#!/usr/bin/python3

import sys
import re
from shlex import split
import cmd
import json
import os.path
from models import storage


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """
        Empty line
        """
        pass

    def do_quit(self, line):
        """
        Quit
        """
        print(line)
        return True

    def do_EOF(self, line):
        """
        EOF
        """
        return True

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """
        Create a new instance of BaseModel,
        save it (to the JSON file), and print the id.
        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
            return

        try:
            class_name = arg.split()[0]
            if class_name in HBNBCommand.__classes:
                instance = storage.classes()[class_name]()
                storage.new(instance)
                print(instance.id)
            else:
                print("** class doesn't exist **")
        except ImportError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Print the string representation of an
        instance based on the class name and id.
        Usage: show <class name> <id>
        """
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        instance_key = f"{class_name}.{instance_id}"
        print(instance_key)

        if instance_key not in storage.all():
            print("** no instance found **")
            return

        instance = storage.all()[instance_key]
        print(instance)

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name
        and id (save the change into the JSON file).
        Usage: destroy <class name> <id>
        """
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        instance_key = f"{class_name}.{instance_id}"

        if instance_key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[instance_key]
        storage.save()

        if not any(key.startswith(class_name + ".") for key in storage.all()):
            storage.reload()

        print("Instance deleted successfully.")

    def do_all(self, arg):
        """Check if the input is in the format <class name>,all()"""
        """Split the command to check for the "all" method"""
        parts = parse(arg)

        print(parts)
        if len(parts) > 0 and parts[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(parts) > 0 and parts[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(parts) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute.
        Usage: update <class name> <id> <attribute name>
        "<attribute value>"
        """

        args = arg.split()

        if len(args) < 2:
            print("** class name missing **")
            return

        class_name = args[1]

        if len(args) < 3:
            print("** instance id missing **")
            return

        instance_id = args[2]
        instance_key = f"{class_name}.{instance_id}"

        if instance_key not in storage.all():
            print("** no instance found **")
            return

        if len(args) < 4:
            print("** attribute name missing **")
            return

        attribute_name = args[3]
        if attribute_name not in storage.all()[instance_key].to_dict():
            print("** attribute name missing **")
            return

        if len(args) < 5:
            print("** value missing **")
            return

        attribute_value = " ".join(args[4:])
        if not (attribute_value.startswith('"') and
                attribute_value.endswith('"')):
            print("** attribute value must be enclosed in double quotes **")
            return

        attribute_value = attribute_value[1:-1]

        try:
            if isinstance(getattr(storage.all()[instance_key],
                                  attribute_name), int):
                attribute_value = int(attribute_value)
            elif isinstance(getattr(storage.all()[instance_key],
                                    attribute_name), float):
                attribute_value = float(attribute_value)
            """ Update the instance attribute and save to the JSON file"""
            setattr(storage.all()[instance_key],
                    attribute_name, attribute_value)
            storage.save()
        except (ValueError, TypeError):
            print("** invalid value **")
            return

        print("Instance updated successfully.")

    def do_count(self, line):
        '''Usage: 1. count <class name> | 2. <class name>.count()
            Function: Counts all the instances  of the class
        '''
        count = 0
        arg = parse(line)
        for key in storage.all().values():
            if arg[0] == key.__class__.__name__:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
