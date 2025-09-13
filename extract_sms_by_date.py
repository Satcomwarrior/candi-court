#!/usr/bin/env python3
"""
Extract SMS messages from large XML files by date range
Specifically targeting August 5-7, 2025 timeframe around Callahan's filings
"""

import xml.etree.ElementTree as ET
import os
import glob
from datetime import datetime
import sys

def timestamp_to_date(timestamp):
    """Convert timestamp to readable date"""
    try:
        # Convert timestamp (milliseconds) to seconds
        ts_seconds = int(timestamp) / 1000
        return datetime.fromtimestamp(ts_seconds)
    except:
        return None

def extract_messages_by_date_range(xml_file, start_date, end_date, output_file):
    """Extract messages within date range"""
    print(f"Processing {xml_file}...")
    
    # Parse XML incrementally to handle large files
    context = ET.iterparse(xml_file, events=('start', 'end'))
    context = iter(context)
    event, root = next(context)
    
    messages_found = []
    
    for event, elem in context:
        if event == 'end' and elem.tag == 'sms':
            # Get message data
            date_attr = elem.get('date')
            readable_date = elem.get('readable_date', '')
            contact_name = elem.get('contact_name', 'Unknown')
            body = elem.get('body', '')
            msg_type = elem.get('type', '')
            
            if date_attr:
                msg_date = timestamp_to_date(date_attr)
                if msg_date and start_date <= msg_date <= end_date:
                    messages_found.append({
                        'date': msg_date,
                        'readable_date': readable_date,
                        'contact': contact_name,
                        'type': 'Sent' if msg_type == '2' else 'Received',
                        'body': body
                    })
            
            # Clear element to save memory
            elem.clear()
    
    # Sort by date
    messages_found.sort(key=lambda x: x['date'])
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"SMS Messages from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\\n")
        f.write("="*80 + "\\n\\n")
        
        for msg in messages_found:
            f.write(f"Date: {msg['readable_date']}\\n")
            f.write(f"Contact: {msg['contact']}\\n")
            f.write(f"Type: {msg['type']}\\n")
            f.write(f"Message: {msg['body']}\\n")
            f.write("-"*60 + "\\n\\n")
    
    print(f"Found {len(messages_found)} messages in date range")
    return len(messages_found)

def main():
    # Define date ranges of interest
    date_ranges = [
        # August 5-7, 2025 (Callahan filing period)
        (datetime(2025, 8, 5), datetime(2025, 8, 7), "callahan_filing_period"),
        # April 13-15, 2025 (Medical emergency period)  
        (datetime(2025, 4, 13), datetime(2025, 4, 15), "medical_emergency_period"),
        # November 2024 (Brain surgery period)
        (datetime(2024, 11, 1), datetime(2024, 11, 30), "brain_surgery_period"),
    ]
    
    # Find all SMS XML files
    xml_files = glob.glob("sms-*.xml")
    
    if not xml_files:
        print("No SMS XML files found in current directory")
        return
    
    print(f"Found {len(xml_files)} SMS XML files")
    
    for xml_file in xml_files:
        print(f"\\nProcessing {xml_file}...")
        file_size_mb = os.path.getsize(xml_file) / (1024 * 1024)
        print(f"File size: {file_size_mb:.1f} MB")
        
        for start_date, end_date, period_name in date_ranges:
            output_file = f"{period_name}_{os.path.basename(xml_file).replace('.xml', '.txt')}"
            
            try:
                count = extract_messages_by_date_range(xml_file, start_date, end_date, output_file)
                if count > 0:
                    print(f"  → {period_name}: {count} messages saved to {output_file}")
                else:
                    print(f"  → {period_name}: No messages found")
                    # Remove empty file
                    if os.path.exists(output_file):
                        os.remove(output_file)
            except Exception as e:
                print(f"  → Error processing {period_name}: {e}")

if __name__ == "__main__":
    main()
