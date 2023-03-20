# Created by Anthony Brinkhuis
import struct
import lxml.etree as et
import pandas as pd


class SysmacData:
    def __init__(self, file_name):
        self.file_name = file_name

    @staticmethod
    def hex_to_real(hex_val):
        binary_data = bytes.fromhex(hex_val)
        FLOAT = 'f'
        fmt = '<' + FLOAT * (len(binary_data) // struct.calcsize(FLOAT))
        numbers = struct.unpack(fmt, binary_data)
        return numbers[0]
    
    @staticmethod
    def real_to_hex(real_number):
        binary_data = struct.pack('f', real_number)
        hex_data = binary_data.hex()
        return hex_data

    def parse_xml(self):
        xml_data = et.parse(f'{self.file_name}.xml')
        data_root = xml_data.find('Body')
        ret_vars = data_root.find('RetainVariable')

        lst_tag = []
        lst_data = []
        lst_type = []

        for item in ret_vars:
            tag = item.items()[0][1][6:]
            data_type = item.items()[1][1]
            data = item.find('Data')
            data_text = data.text

            if ('REAL' in data_type) or ('real' in data_type):
                lst_tag.append(tag)
                lst_data.append(self.hex_to_real(data_text))
                lst_type.append(data_type)
            elif ('STRING' in data_type) or ('string' in data_type):
                lst_tag.append(tag)
                if data_text is not None:
                    lst_data.append(bytearray.fromhex(data_text).decode())
                else:
                    lst_data.append('')
                lst_type.append(data_type)
            else:
                lst_tag.append(tag)
                lst_data.append(data.text)
                lst_type.append(data_type)

        data_dict = {'Tag': lst_tag, 'Data': lst_data, 'Type': lst_type}
        return data_dict

    def save_to_csv(self):
        data_dict = self.parse_xml()
        df = pd.DataFrame(data_dict)
        df.to_csv(f'{self.file_name}.csv', index=False)

    def csv_to_xml(self):
        df = pd.read_csv(f'{self.file_name}.csv')

        # Create the root element
        root = et.Element("Root")

        # Create the body element
        body = et.SubElement(root, "Body")

        # Create the RetainVariable element
        retain_vars = et.SubElement(body, "RetainVariable")

        # Iterate through the dataframe rows and build XML elements
        for index, row in df.iterrows():
            item = et.SubElement(retain_vars, "Item", Name=f"AT%s" % row["Tag"], Type=row["Type"])
            data = et.SubElement(item, "Data")

            if "REAL" in row["Type"] or "real" in row["Type"]:
                data.text = self.real_to_hex(float(row["Data"]))
            elif "STRING" in row["Type"] or "string" in row["Type"]:
                data_value = row["Data"]
                if isinstance(data_value, str):
                    data.text = bytearray(data_value, 'utf-8').hex()
                else:
                    data.text = ''
            else:
                data.text = str(row["Data"])
            print(index)

        # Generate the XML string with lxml.etree.tostring and include the XML declaration
        xml_string = et.tostring(root, encoding='utf-8', pretty_print=True, xml_declaration=True).decode('utf-8')

        # Save the XML string to a file
        with open(f'{self.file_name}_new_file.xml', 'w', encoding='utf-8') as xml_file:
            xml_file.write(xml_string)


if __name__ == '__main__':
    file_name = r'examples\controller_1__XY_RI90_01_CT90_03_042122'
    sysmac_data = SysmacData(file_name)
    sysmac_data.save_to_csv()
    sysmac_data.csv_to_xml()
