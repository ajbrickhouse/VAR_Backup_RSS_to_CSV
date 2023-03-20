# Created by Anthony Brinkhuis
import struct
import xml.etree.ElementTree as et
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
        original_xml = et.parse(f'{self.file_name}.xml')
        data_root = original_xml.find('Body')
        ret_vars = data_root.find('RetainVariable')

        for index, row in df.iterrows():
            tag = f"Symbol{row['Tag']}"
            data_type = row['Type']
            data_text = row['Data']

            item = ret_vars.find(f'./Item[@Name="{tag}"]')

            if item is not None:
                data_element = item.find('Data')

                if ('REAL' in data_type) or ('real' in data_type):
                    data_element.text = hex(struct.unpack('<I', struct.pack('<f', float(data_text)))[0])[2:]
                elif ('STRING' in data_type) or ('string' in data_type):
                    data_element.text = data_text.encode().hex()
                else:
                    data_element.text = data_text
            print(index)

        original_xml.write(f'{self.file_name}_reconstructed.xml', encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    file_name = r'examples\controller_1_ALL_DATA_041622'
    sysmac_data = SysmacData(file_name)
    sysmac_data.save_to_csv()
    sysmac_data.csv_to_xml()
