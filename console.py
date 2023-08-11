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
            return

        class_name = args[0]

        if class_name not in globals() or not issubclass(globals()[class_name], BaseModel):
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

        if class_name not in globals() or not issubclass(globals()[class_name], BaseModel):
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
        """
        Prints all string representation of instances based 
        on the class name or prints all instances.
        Usage: all <class name> or all.
        """
        if not arg:
            # Print all instances if no class name is provided
            instances = storage.all().values()
        else:
            class_name = arg
            if class_name not in globals() or not issubclass(globals()[class_name], BaseModel):
                print("** class doesn't exist **")
                return
            # Filter instances by the provided class name
            instances = [instance for instance in storage.all().values() 
                    if type(instance).__name__ == class_name]

        # Print the string representation of instances
        for instance in instances:
            print(instance)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or updating attribute.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
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
        if not (attribute_value.startswith('"') and attribute_value.endswith('"')):
            print("** attribute value must be enclosed in double quotes **")
            return

        attribute_value = attribute_value[1:-1]

        try:
            if isinstance(getattr(storage.all()[instance_key], attribute_name), int):
                attribute_value = int(attribute_value)
            elif isinstance(getattr(storage.all()[instance_key], attribute_name), float):
                attribute_value = float(attribute_value)
            """ Update the instance attribute and save to the JSON file"""
            setattr(storage.all()[instance_key], attribute_name, attribute_value)
            storage.save()
        except (ValueError, TypeError):
            print("** invalid value **")
            return

        print("Instance updated successfully.")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
