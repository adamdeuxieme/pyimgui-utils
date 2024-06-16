# Pyimgui Utils
Provide utils to help you create imgui windows and elements using pyimgui.  
It provides custom buttons, drag buttons, tree node and so on.

## Installation
Python 3.7+ is required for the project to work. 

You can use `pip` to install the module with this command. 

```bash
pip install pyimgui_utils
```

## Usage
Find examples in examples folder.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to 
discuss what you would like to change.  
Please make sure to update tests as appropriate.

## Tests
Two approach are followed to test the project: unit testing, interactive testing.  
Unit testing for fully automatable tests; interactive test for non fully 
automatable tests.  

As suggested by the name, interactive tests requires operator interaction.  
It takes the form of a window that describe the test and other windows under test.  
To mark a test as validate, hit test passes; hit test fails otherwise. 
