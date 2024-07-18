import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timezone
from collections import defaultdict
import argparse
import zipfile
import gzip
import shutil
import matplotlib.pyplot as plt  # for charts

def parse_dmarc_report(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    report_metadata = root.find('report_metadata')
    org_name = report_metadata.find('org_name').text
    email = report_metadata.find('email').text
    report_id = report_metadata.find('report_id').text
    date_range = report_metadata.find('date_range')
    begin = datetime.fromtimestamp(int(date_range.find('begin').text), timezone.utc)
    end = datetime.fromtimestamp(int(date_range.find('end').text), timezone.utc)

    records = []
    for record in root.findall('record'):
        row = record.find('row')
        source_ip = row.find('source_ip').text
        count = int(row.find('count').text)
        policy_evaluated = row.find('policy_evaluated')
        disposition = policy_evaluated.find('disposition').text
        dkim = policy_evaluated.find('dkim').text
        spf = policy_evaluated.find('spf').text

        identifiers = record.find('identifiers')
        header_from = identifiers.find('header_from').text

        auth_results = record.find('auth_results')
        dkim_auth = auth_results.find('dkim')
        spf_auth = auth_results.find('spf')

        dkim_domain = dkim_result = spf_domain = spf_result = None
        if dkim_auth is not None:
            dkim_domain = dkim_auth.find('domain').text
            dkim_result = dkim_auth.find('result').text
        if spf_auth is not None:
            spf_domain = spf_auth.find('domain').text
            spf_result = spf_auth.find('result').text

        records.append({
            'source_ip': source_ip,
            'count': count,
            'disposition': disposition,
            'dkim': dkim,
            'spf': spf,
            'header_from': header_from,
            'dkim_domain': dkim_domain,
            'dkim_result': dkim_result,
            'spf_domain': spf_domain,
            'spf_result': spf_result,
            'begin': begin,
            'end': end,
            'org_name': org_name
        })

    return {
        'org_name': org_name,
        'email': email,
        'report_id': report_id,
        'begin': begin,
        'end': end,
        'records': records
    }


def read_dmarc_reports(directory, extract_folder):
    reports = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith('.xml'):
            report = parse_dmarc_report(file_path)
            reports.append(report)
        elif filename.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
                for extracted_file in os.listdir(extract_folder):
                    if extracted_file.endswith('.xml'):
                        extracted_file_path = os.path.join(extract_folder, extracted_file)
                        report = parse_dmarc_report(extracted_file_path)
                        reports.append(report)
        elif filename.endswith('.gz'):
            with gzip.open(file_path, 'rb') as f_in:
                extracted_file_path = os.path.join(extract_folder, filename[:-3])
                with open(extracted_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            if extracted_file_path.endswith('.xml'):
                report = parse_d
