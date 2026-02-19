from fpdf import FPDF

class YamahaManualPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'YAMAHA DRAG STAR XVS 650 - SERVICE MANUAL (ENGLISH TRANSLATION)', border=False, ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_manual():
    pdf = YamahaManualPDF()
    pdf.add_page()
    
    # Title Page
    pdf.set_font('helvetica', 'B', 24)
    pdf.ln(50)
    pdf.cell(0, 20, 'YAMAHA', ln=True, align='C')
    pdf.set_font('helvetica', 'B', 32)
    pdf.cell(0, 20, 'DRAG STAR', ln=True, align='C')
    pdf.cell(0, 20, 'XVS 650', ln=True, align='C')
    pdf.ln(20)
    pdf.set_font('helvetica', 'B', 18)
    pdf.cell(0, 10, 'SERVICE MANUAL', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, 'December 2002', ln=True, align='C')
    pdf.cell(0, 10, 'Yamaha Motor da Amazonia Ltda.', ln=True, align='C')
    
    pdf.add_page()
    
    # Preface
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, 'PREFACE', ln=True)
    pdf.set_font('helvetica', '', 10)
    pdf.ln(5)
    preface_text = (
        "This manual was prepared by YAMAHA MOTOR DA AMAZÔNIA LTDA., exclusively for use by authorized "
        "Yamaha dealers and their qualified mechanics. As it is not possible to introduce all mechanical "
        "information in a single manual, it is assumed that persons reading this manual for the purpose "
        "of performing maintenance and repairs on Yamaha motorcycles possess a basic knowledge of the "
        "concepts and procedures inherent to motorcycle repair technology. Without this knowledge, any "
        "attempt at repair or service on this model may result in difficulties in its use and/or safety.\n\n"
        "YAMAHA MOTOR DA AMAZÔNIA LTDA. strives to continually improve all products in its line. "
        "Significant modifications and changes in specifications or procedures will be reported to all "
        "YAMAHA dealers and will appear in the corresponding locations in future editions of this manual."
    )
    pdf.multi_cell(0, 6, preface_text)
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'IMPORTANT INFORMATION', ln=True)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, 'WARNING: Significant alert! Your safety is involved!', ln=True)
    pdf.cell(0, 6, 'CAUTION: Special precautions to avoid damage to the vehicle.', ln=True)
    pdf.cell(0, 6, 'NOTE: Provides information to make procedures clearer or easier.', ln=True)

    pdf.add_page()
    
    # Table of Contents
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, 'INDEX', ln=True)
    pdf.ln(5)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, '1. GENERAL INFORMATION ................................................................ 1-1', ln=True)
    pdf.cell(0, 10, '2. SPECIFICATIONS ................................................................................ 2-1', ln=True)
    pdf.cell(0, 10, '3. PERIODIC INSPECTION AND ADJUSTMENTS ............................ 3-1', ln=True)
    pdf.cell(0, 10, '4. ENGINE OVERHAUL ........................................................................ 4-1', ln=True)
    pdf.cell(0, 10, '5. CARBURATION ................................................................................... 5-1', ln=True)
    pdf.cell(0, 10, '6. CHASSIS ............................................................................................. 6-1', ln=True)
    pdf.cell(0, 10, '7. ELECTRICAL SYSTEM ................................................................... 7-1', ln=True)
    pdf.cell(0, 10, '8. TROUBLESHOOTING ....................................................................... 8-1', ln=True)

    pdf.add_page()
    
    # Section 2: Specifications
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, 'CHAPTER 2: SPECIFICATIONS', ln=True)
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'GENERAL SPECIFICATIONS', ln=True)
    pdf.set_font('helvetica', '', 10)
    
    specs = [
        ("Model", "XVS650"),
        ("Model Code", "5WD1"),
        ("Dimensions:", ""),
        ("  Total Length", "2,340 mm"),
        ("  Total Width", "880 mm"),
        ("  Total Height", "1,065 mm"),
        ("  Seat Height", "695 mm"),
        ("  Wheelbase", "1,610 mm"),
        ("  Ground Clearance", "140 mm"),
        ("  Turning Radius", "3,100 mm"),
        ("Weight (Wet)", "242 kg"),
        ("Engine:", ""),
        ("  Type", "Air-cooled, 4-stroke, SOHC"),
        ("  Cylinder Arrangement", "V-twin (V2)"),
        ("  Displacement", "649 cm3"),
        ("  Bore x Stroke", "81 x 63 mm"),
        ("  Compression Ratio", "9:1"),
        ("  Starting System", "Electric Start"),
        ("  Lubrication", "Wet Sump"),
        ("Oil Capacities:", ""),
        ("  Total Capacity", "3.2 Liters"),
        ("  Periodic Change", "2.6 Liters"),
        ("  With Filter Change", "2.8 Liters"),
        ("Final Drive Oil (Cardan)", "SAE80API GL-4 (0.190 L)"),
        ("Fuel Tank", "16 Liters (3L Reserve)"),
        ("Spark Plug", "DPR7EA-9 (NGK)"),
        ("Gap", "0.8 ~ 0.9 mm"),
        ("Clutch Type", "Wet Multi-plate"),
        ("Transmission", "5-speed Constant Mesh")
    ]
    
    for label, val in specs:
        pdf.cell(60, 6, label, border=0)
        pdf.cell(0, 6, val, border=0, ln=True)

    pdf.add_page()
    
    # Section 3: Maintenance Intervals
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, 'PERIODIC MAINTENANCE CHART', ln=True)
    pdf.ln(5)
    pdf.set_font('helvetica', '', 9)
    # Simple table for maintenance
    pdf.cell(60, 7, 'Item', 1)
    pdf.cell(40, 7, '1,000 km', 1)
    pdf.cell(40, 7, '6,000 km', 1)
    pdf.cell(40, 7, '12,000 km', ln=True, border=1)
    
    maint_items = [
        ("Fuel Line", "Check", "Check", "Check/Replace"),
        ("Spark Plugs", "Check", "Check", "Replace"),
        ("Valves", "Check/Adjust", "Check/Adjust", "Check/Adjust"),
        ("Air Filter", "-", "Clean", "Replace"),
        ("Battery", "Check", "Check", "Check"),
        ("Brakes", "Check", "Check", "Check"),
        ("Engine Oil", "Replace", "Replace", "Replace"),
        ("Engine Oil Filter", "Replace", "-", "Replace"),
        ("Final Drive Oil", "Replace", "-", "Replace")
    ]
    
    for item, i1, i2, i3 in maint_items:
        pdf.cell(60, 7, item, 1)
        pdf.cell(40, 7, i1, 1)
        pdf.cell(40, 7, i2, 1)
        pdf.cell(40, 7, i3, ln=True, border=1)

    pdf.add_page()
    
    # Section 7: Electrical
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, 'CHAPTER 7: ELECTRICAL SYSTEM', ln=True)
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Bulb Wattage:', ln=True)
    pdf.set_font('helvetica', '', 10)
    
    bulbs = [
        ("Headlight", "12V 60W/55W (Halogen)"),
        ("Tail/Brake Light", "12V 5W/21W x 2"),
        ("Turn Signals", "12V 21W x 4"),
        ("Instrument Light", "12V 1.7W x 1"),
        ("Neutral Indicator", "12V 3W x 1"),
        ("High Beam Indicator", "12V 1.7W x 1"),
        ("Engine Trouble Indicator", "12V 1.7W x 1")
    ]
    
    for label, val in bulbs:
        pdf.cell(70, 6, label, border=0)
        pdf.cell(0, 6, val, border=0, ln=True)

    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'T.C.I. Igniton System', ln=True)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, 'Ignition Timing: 12 deg at 1,200 rpm', ln=True)
    pdf.cell(0, 6, 'Pulse Coil Resistance: 182 ~ 222 Ohm at 20C', ln=True)
    pdf.cell(0, 6, 'Ignition Coil Primary: 3.8 ~ 4.6 Ohm', ln=True)
    pdf.cell(0, 6, 'Ignition Coil Secondary: 10.1 ~ 15.1 kOhm', ln=True)

    output_path = r"C:\Users\Dell\OneDrive\Desktop\YAMAHA_XVS650_Service_Manual_English.pdf"
    pdf.output(output_path)
    print(f"PDF generated at: {output_path}")

if __name__ == "__main__":
    create_manual()
