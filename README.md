# flutter_localization_converter
A simple python script, that converts android native localization .xml files to the JSON file

### What it can do:
  1. Finds many input files in subdirectories and merges into one json file
  2. Finds and parse tags, attributes and parse it to json key-value format
  3. Sorts keys by alphabetical order
  4. Finds same keys (collisions) and renames it by adding underscore ('_')
  5. Finds arguments in values and convert it to json-format arguments (example: from "%1$s" to "$s1")
  
### Usage
  1. Place converter.py in directory that contains localization files or subdirectories with them.
  2. Type ```python converter.py strings``` (or any file names that contains xml to parse). Look at strings.json for a result.
  
  You can use optional ```-o``` parameter to set output file name (before input file names).
  You can use optional ```-v``` parameter to print all information about parsing process
  
  Please type ```pyhton converter.py -h``` for additional info
  
