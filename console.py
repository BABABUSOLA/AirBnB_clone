#!/usr/bin/python3

import cmd

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

if __name__ == "__main__":
    HBNBCommand().cmdloop()
