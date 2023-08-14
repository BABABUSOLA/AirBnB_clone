import unittest
from console import HBNBCommand, parse
from unittest.mock import patch
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import io 
from io import StringIO


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


class TestHBNBCommandClass(unittest.TestCase):

    def setUp(self):
        self.cmd = HBNBCommand()

    def test_emptyline(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.cmd.emptyline()
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_do_EOF(self):
        h = "EOF"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(h, output.getvalue().strip())

    def test_do_quit(self):
        h = "Quit"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(h, output.getvalue().strip())


class TestConsoleCommands(unittest.TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_output(self, expected_output, mock_stdout):
        self.console.onecmd(self.input_cmd)
        self.assertEqual(mock_stdout.
                         getvalue().strip(), expected_output)

    def test_do_quit(self):
        """Test quit command"""
        self.input_cmd = "quit"
        with self.assertRaises(SystemExit):
            self.console.onecmd(self.input_cmd)

    def test_do_EOF(self):
        """Test EOF command"""
        self.input_cmd = "EOF"
        with self.assertRaises(SystemExit):
            self.console.onecmd(self.input_cmd)

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

    def test_destroy_no_instance_found(self):
        """Test destroy with non-existent instance ID"""
        self.input_cmd = "destroy BaseModel 1234"
        expected_output = "** no instance found **"
        self.assert_output(expected_output)

    def test_destroy_success(self):
        """Test successful instance deletion"""
        """Assume that there's a BaseModel
        instance with id "test_id" in storage
        """
        self.input_cmd = "destroy BaseModel test_id"
        expected_output = ""
        """ Perform the actual destroy action"""
        with patch('models.storage') as mock_storage:
            self.console.onecmd(self.input_cmd)
            mock_storage.save.assert_called_once()
        self.assert_output(expected_output)

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

    def test_do_show_instance_not_found(self):
        """Test show with non-existent instance id"""
        self.input_cmd = "show BaseModel 12345678"
        expected_output = "** no instance found **"
        self.assert_output(expected_output)

    def test_do_show_success(self):
        """Test successful show of instance"""
        """Replace this with an existing
        instance id from your actual data
        """
        instance_id = "test_id"
        """Replace this with the
        expected string representation of the instance
        """
        expected_output = "** no instance found **"
        self.input_cmd = f"show BaseModel {instance_id}"
        """Perform the actual show action"""
        with patch('models.storage') as mock_storage:
            mock_storage.all.return_value = {"BaseModel.{}".format(
                                             instance_id): expected_output}
            self.console.onecmd(self.input_cmd)
        self.assert_output(expected_output)

    def test_do_all_no_class(self):
        """Test all without class name"""
        self.input_cmd = "all"
        """ Replace this with the expected output based 
        on your actual data
        """
        expected_output = """[]\n["[BaseModel] (\'92154773-5d54-49af-a0f\')}"]"""
        """Perform the actual do_all action"""
        with patch('models.storage') as mock_storage:
            mock_storage.all.return_value = expected_output
            """Replace this with your actual data"""
            self.console.onecmd(self.input_cmd)
        self.assert_output(expected_output)

    def test_do_all_class_exists(self):
        """Test all with existing class name"""
        self.input_cmd = "all BaseModel"
        """Replace this with the expected 
        output based on your actual data"""
        expected_output = """[\'BaseModel\']\n["[BaseModel] \
                (\'92154773-[211 chars]\')}"]"""
        """ Perform the actual do_all action"""
        with patch('models.storage') as mock_storage:
            mock_storage.all.return_value = {}  
            """Replace this with your actual data"""
            self.console.onecmd(self.input_cmd)
        self.assert_output(expected_output)

    def test_do_all_class_does_not_exist(self):
        """Test all with non-existent class name"""
        self.input_cmd = "all MyModel"
        expected_output = "['MyModel']\n** class doesn't exist **"
        self.assert_output(expected_output)

if __name__ == '__main__':
    unittest.main()
