import unittest
from console import HBNBCommand, parse
from unittest.mock import patch, MagicMock
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import io
from io import StringIO
import os


class TestParseFunction(unittest.TestCase):

    def test_parse_without_braces_or_brackets(self):
        result = parse("command arg1 arg2")
        expected = ["command", "arg1", "arg2"]
        self.assertEqual(result, expected)

    def test_parse_with_brackets(self):
        result = parse("command [arg1,arg2]")
        expected = ["command", "[arg1,arg2]"]
        self.assertEqual(result, expected)

    def test_parse_with_curly_braces(self):
        result = parse("command {arg1,arg2}")
        expected = ["command", "{arg1,arg2}"]
        self.assertEqual(result, expected)

    def test_parse_with_both_brackets_and_curly_braces(self):
        result = parse("command [arg1,arg2] {arg3,arg4}")
        expected = ["command", "[arg1,arg2]", "{arg3,arg4}"]
        self.assertEqual(result, expected)


class TestHBNBCommand_prompting(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommandClass(unittest.TestCase):

    def setUp(self):
        self.cmd = HBNBCommand()

    def test_help_quit(self):
        h = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_create(self):
        h = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_EOF(self):
        h = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(h, output.getvalue().strip())


class TestConsoleCommands(unittest.TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_output(self, expected_output, mock_stdout):
        self.console.onecmd(self.input_cmd)
        self.assertEqual(mock_stdout.
                         getvalue().strip(), expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_emptyline(self, mock_stdout):
        """Test emptyline behavior"""
        self.input_cmd = ""
        self.console.onecmd(self.input_cmd)
        self.assertEqual(mock_stdout.getvalue().strip(), "")

    def test_destroy_class_missing(self):
        """Test destroy with missing class name"""
        self.input_cmd = "destroy"
        expected_output = "** class name missing **"
        self.assert_output(expected_output)

    def test_destroy_class_does_not_exist(self):
        """Test destroy with non-existent class name"""
        self.input_cmd = "destroy MyModel"
        expected_output = "** class doesn't exist **"
        self.assert_output(expected_output)

    def test_destroy_instance_id_missing(self):
        """Test destroy with missing instance ID"""
        self.input_cmd = "destroy BaseModel"
        expected_output = "** instance id missing **"
        self.assert_output(expected_output)

    def test_destroy_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "destroy BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def test_create_class_missing(self):
        """Test create with missing class name"""
        self.input_cmd = "create"
        expected_output = "** class name missing **"
        self.assert_output(expected_output)

    def test_create_class_does_not_exist(self):
        """Test create with non-existent class name"""
        self.input_cmd = "create MyModel"
        expected_output = "** class doesn't exist **"
        self.assert_output(expected_output)

    def test_create_success(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            testKey = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    def test_do_show_class_missing(self):
        """Test show with missing class name"""
        self.input_cmd = "show"
        expected_output = "** class name missing **"
        self.assert_output(expected_output)

    def test_do_show_class_does_not_exist(self):
        """Test show with non-existent class name"""
        self.input_cmd = "show MyModel"
        expected_output = "** class doesn't exist **"
        self.assert_output(expected_output)

    def test_do_show_instance_id_missing(self):
        """Test show with missing instance id"""
        self.input_cmd = "show BaseModel"
        expected_output = "** instance id missing **"
        self.assert_output(expected_output)

    def test_do_show_success(self):
        """Test successful show"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def test_do_all_no_class(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())

    def test_do_all_class_exists(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())

    def test_do_all_class_does_not_exist(self):
        """Test all with non-existent class name"""
        self.input_cmd = "all MyModel"
        expected_output = "['MyModel']\n** class doesn't exist **"
        self.assert_output(expected_output)

    def test_update_valid_string_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        testCmd = "update BaseModel {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", output.getvalue().strip())

    def test_count_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", output.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
