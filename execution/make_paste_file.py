import csv
import os

CSV_DIR = r'c:\Users\jonny\Desktop\Jai.OS 4.0 template\.tmp\haccp_sheets'
OUT = r'c:\Users\jonny\Desktop\HACCP_PASTE_DATA.txt'

files = [
    ('fridge_freezer_fill.csv', 'FRIDGE & FREEZER TEMP LOG'),
    ('cooking_temps_fill.csv', 'COOKING TEMPS'),
    ('cleaning_schedule_fill.csv', 'CLEANING SCHEDULE'),
    ('weekly_signoff_fill.csv', 'WEEKLY SIGN-OFF'),
    ('probe_calibration_fill.csv', 'PROBE CALIBRATION'),
]

with open(OUT, 'w', encoding='utf-8') as out:
    for fname, title in files:
        path = os.path.join(CSV_DIR, fname)
        out.write(f'===== {title} =====\n')
        out.write(f'(Paste below into the "{title}" tab in Google Sheets)\n\n')
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                out.write('\t'.join(row) + '\n')
        out.write('\n\n')

print(f'Created: {OUT}')
print(f'Size: {os.path.getsize(OUT):,} bytes')
