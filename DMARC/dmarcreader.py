import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timezone
from collections import defaultdict
from termcolor import colored
import argparse

def parse_dmarc_report(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    report_metadata = root.find('report_metadata')
    org_name = report_metadata.find('org_name').text
    email = report_metadata.find('email').text
    report_id = report_metadata.find('report_id').text
    date_range = report_metadata.find('date_range')
    begin = int(date_range.find('begin').text)
    end = int(date_range.find('end').text)

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

        if dkim_auth is not None:
            dkim_domain = dkim_auth.find('domain').text
            dkim_result = dkim_auth.find('result').text
        else:
            dkim_domain = dkim_result = None

        if spf_auth is not None:
            spf_domain = spf_auth.find('domain').text
            spf_result = spf_auth.find('result').text
        else:
            spf_domain = spf_result = None

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
            'begin': datetime.fromtimestamp(begin, timezone.utc),
            'end': datetime.fromtimestamp(end, timezone.utc),
            'org_name': org_name
        })

    return {
        'org_name': org_name,
        'email': email,
        'report_id': report_id,
        'begin': datetime.fromtimestamp(begin, timezone.utc),
        'end': datetime.fromtimestamp(end, timezone.utc),
        'records': records
    }

def read_dmarc_reports(directory):
    reports = []
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            report = parse_dmarc_report(file_path)
            reports.append(report)
    return reports

def group_by(reports, group_by_option):
    grouped_data = defaultdict(list)
    for report in reports:
        for record in report['records']:
            if group_by_option == 'week':
                week_start = record['begin'] - pd.Timedelta(days=record['begin'].weekday())
                week_key = week_start.strftime('%Y-%m-%d')
                grouped_data[week_key].append(record)
            elif group_by_option == 'month':
                month_start = record['begin'].replace(day=1)
                month_key = month_start.strftime('%Y-%m')
                grouped_data[month_key].append(record)
            elif group_by_option == 'org':
                org_key = record['org_name']
                grouped_data[org_key].append(record)
    
    return grouped_data

def display_grouped_data(grouped_data, group_by_option):
    for group, records in grouped_data.items():
        print(f"{group_by_option.capitalize()}: {group}")
        df = pd.DataFrame(records)
        aggregated_data = df.groupby(['org_name', 'header_from', 'source_ip', 'disposition', 'dkim', 'spf']).agg({
            'count': 'sum',
            'dkim_domain': 'first',
            'dkim_result': 'first',
            'spf_domain': 'first',
            'spf_result': 'first'
        }).reset_index()

        for index, row in aggregated_data.iterrows():
            row_str = f"Org: {row['org_name']}, From: {row['header_from']}, IP: {row['source_ip']}, Count: {row['count']}, " \
                      f"Disposition: {row['disposition']}, DKIM: {row['dkim']} ({row['dkim_domain']} - {row['dkim_result']}), " \
                      f"SPF: {row['spf']} ({row['spf_domain']} - {row['spf_result']})"
            if row['disposition'] == 'quarantine':
                print(colored(row_str, 'red'))
            else:
                print(row_str)

        print("\n")

def save_grouped_data_to_csv(grouped_data, output_file):
    all_records = []
    for group, records in grouped_data.items():
        for record in records:
            record['group'] = group
            all_records.append(record)

    df = pd.DataFrame(all_records)
    df.to_csv(output_file, index=False)

def main():
    parser = argparse.ArgumentParser(description='DMARC report parser and aggregator.')
    parser.add_argument('directory', help='Directory containing DMARC reports')
    parser.add_argument('output_csv', help='Output CSV file path')
    parser.add_argument('--group_by', choices=['week', 'month', 'org'], default='month', help='Grouping option: week, month, or org')

    args = parser.parse_args()

    # Read DMARC reports
    reports = read_dmarc_reports(args.directory)

    # Group records based on the selected option
    grouped_data = group_by(reports, args.group_by)

    # Display grouped data with color coding
    display_grouped_data(grouped_data, args.group_by)

    # Save grouped data to CSV
    save_grouped_data_to_csv(grouped_data, args.output_csv)

    print(f"Grouped DMARC data saved to {args.output_csv}")

if __name__ == '__main__':
    main()
