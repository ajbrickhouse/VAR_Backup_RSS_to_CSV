# Created by Anthony Brinkhuis
import struct
import xml.etree.ElementTree as et
import pandas as pd 


# The filename with NO EXTENSION
file_name = r'examples\controller_1_ALL_DATA_041622'

# Convert Sysmac hex values to real number
def hex_to_real(hex_val):
    # Convert the hex val to binary
    binary_data = bytes.fromhex(hex_val)
    # define the format code: 'e' (16bit), 'f' (32 bit), and 'd' (64 bit)
    FLOAT = 'f'
    # Create format string
    fmt = '<' + FLOAT * (len(binary_data) // struct.calcsize(FLOAT))
    # Unpack from the buffer
    numbers = struct.unpack(fmt, binary_data)
    # Return the real number
    return numbers[0]

# Parse the XML file
xml_data = et.parse(f'{file_name}.xml')

# Select the body tree
data_root = xml_data.find('Body')

# Select RetainVariable branch
ret_vars = data_root.find('RetainVariable')

# Defined list for items that will be save to CSV
lst_tag = []
lst_data = []
lst_type = []

# Cycle through all items in the RetainVariable branch
for item in ret_vars:
    # Get data from items
    tag = item.items()[0][1][6:]
    data_type = item.items()[1][1]
    # get the data sub branch
    data = item.find('Data')
    data_text = data.text
    # if the data type is real
    if ('REAL' in data_type) or ('real' in data_type):
        # append info into our lists
        lst_tag.append(tag)
        # convert the hex value to something readable
        lst_data.append(hex_to_real(data_text))
        lst_type.append(data_type)
    # if the data type is a string
    elif ('STRING' in data_type) or ('string' in data_type):
        if data_text != None:
            lst_tag.append(tag)
            # Convert the hex value to something readable
            lst_data.append(bytearray.fromhex(data_text).decode())
            lst_type.append(data_type)
        else:
            lst_tag.append(tag)
            # Convert the hex value to something readable
            lst_data.append('')
            lst_type.append(data_type)
    # if nothing needs to be decoded then this
    else:
        lst_tag.append(tag)
        lst_data.append(data.text)
        lst_type.append(data_type)

# Place all of the accumulated list data into a dictionary
# This makes it more easy to save as a CSV
data_dict = {'Tag': lst_tag, 'Data': lst_data, 'Type': lst_type}  

# Convert the dictionary to a dataframe
df = pd.DataFrame(data_dict)

# Save the dataframe as a CSV
df.to_csv(f'{file_name}.csv')