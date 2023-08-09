#!/usr/bin/python3

import cmd
import json
import os.path
from models.base_model import BaseModel
from models import storage

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

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

    def cmdloop(self, intro=None):
        try:
            super().cmdloop(intro)
        except KeyboardInterrupt:
            print("\nQuit command to exit the program")
            self.cmdloop()

    def do_create(self, arg):
        """
        Create a new instance of BaseModel, save it (to the JSON file), and print the id.
        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
            return

        try:
            class_name = arg.split()[0]
            if class_name in globals() and issubclass(globals()[class_name], BaseModel):
                instance = globals()[class_name]()
                storage.new(instance)
                storage.save()
                print(instance.id)
            else:
                print("** class doesn't exist **")
        except ImportError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Print the string representation of an instance based on the class name and id.
        Usage: show <class name> <id>
        """
        args = arg.split()

        if not args:
            print("** class name missing **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            class_name, instance_id = args[0], args[1]
            instance_key = f"{class_name}.{instance_id}"
            if class_name not in storage.all():
                print("** class doesn't exist **")
            elif instance_key not in storage.all()[class_name]:
                print("** no instance found **")
            else:
                instance = self.storage.all()[class_name][instance_key]
                print(instance)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
