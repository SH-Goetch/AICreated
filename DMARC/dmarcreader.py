import xmltodict
import pandas as pd
import os


def parse_dmarc_report(file_path):
        with open(file_path, 'r') as file:
                xml_data = file.read()

        report = xmltodict.parse(xml_data)
        records = report['feedback']['record']

        processed_records = []
        for record in records:
                row = {
                        'source_ip': record['row']['sourcce_ip'],
                        'count': record['row']['count'],
                        'disposition': record['row']['policy_evaluated']['disposition'],
                        'dkim': record['row']['policy_evaluated']['dkim'],
                        'spf': record['row']['policy_evaluated']['spf'],
                        'header_from': record['identifiers']['header_from'],
                        'envelope_from': record['identifiers']['envelope_from'],
                }
                processed_records.append(row)
        return processed_records

def process_folder(folder_path):
        all_records - []
        for file_name in os.listdir(folder_path):
                if file_name.endswith('.xml'):
                file_path = os.path.join(folder_path, file_name)
                records = parse_demarc_report(file_path)
                all_records.extend(records)

        df = pd.DataFrame(all_records)
        return df

folder_path = 'path_to_folder'
df = process_folder(folder_path)
print(df)
