import os
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

TERMINALS = ['TERMINAL 1A', 'TERMINAL 1B', 'TERMINAL 1C', 'TERMINAL 1D', 'MARINA']
SHOPS = [
    'LAOMAI JKIA', 'LAOMAI MOMBASA',
    'CRAYSON PHARMACY JKIA', 'CRAYSON PHARMACY KIAMBU ROAD', 'CRAYSON PHARMACY MOMBASA'
]

# Standard 30-min time blocks for a full shift (07:00 to 23:30)
SHIFT_BLOCKS = []
for h in range(7, 24):
    for m in [0, 30]:
        start = f"{h:02d}:{m:02d}"
        end_m = m + 30
        end_h = h
        if end_m >= 60:
            end_m -= 60
            end_h += 1
        end = f"{end_h:02d}:{end_m:02d}"
        SHIFT_BLOCKS.append(f"{start} – {end}")


def thin_border():
    thin = Side(style='thin')
    return Border(left=thin, right=thin, top=thin, bottom=thin)


def write_cell(ws, row, col, value, bold=False, bg=None, font_color="000000",
               align="center", wrap=False, font_size=10, border=True):
    cell = ws.cell(row=row, column=col, value=value)
    cell.font = Font(bold=bold, color=font_color, size=font_size, name='Arial')
    if bg:
        cell.fill = PatternFill("solid", fgColor=bg)
    cell.alignment = Alignment(horizontal=align, vertical='center', wrap_text=wrap)
    if border:
        cell.border = thin_border()
    return cell


def generate_excel_report(events: list, shift_date: str) -> str:
    wb = openpyxl.Workbook()

    # ── Sheet 1: Terminal Wraps ───────────────────────────────────────────────
    ws1 = wb.active
    ws1.title = "Terminal Wraps"
    _build_terminal_sheet(ws1, events, shift_date)

    # ── Sheet 2: Shop Activity ────────────────────────────────────────────────
    ws2 = wb.create_sheet("Shop Activity")
    _build_shop_sheet(ws2, events, shift_date)

    # ── Sheet 3: Raw Event Log ────────────────────────────────────────────────
    ws3 = wb.create_sheet("Raw Event Log")
    _build_raw_log(ws3, events)

    # ── Save to reports/output/ inside our project structure ─────────────────
    output_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'output')
)
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f'CCTV_Report_{shift_date}.xlsx')
    wb.save(filepath)
    return filepath


def _build_terminal_sheet(ws, events, shift_date):
    terminal_events = [e for e in events if e['location_category'] == 'terminal']

    # Aggregate: block -> terminal -> subtype -> count
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for e in terminal_events:
        data[e['time_block']][e['location']][e['subtype']] += 1

    # ── Title row ─────────────────────────────────────────────────────────────
    ws.merge_cells('A1:R1')
    ws['A1'].value = "CCTV DAILY REPORT – TERMINAL WRAPS & FOOT TRAFFIC"
    ws['A1'].font = Font(bold=True, size=14, color='FFFFFF', name='Arial')
    ws['A1'].fill = PatternFill("solid", fgColor='1B2B5A')
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30

    ws.merge_cells('A2:R2')
    ws['A2'].value = f"Date: {shift_date}"
    ws['A2'].font = Font(bold=True, size=11, name='Arial')
    ws['A2'].alignment = Alignment(horizontal='center')
    ws.row_dimensions[2].height = 18

    # ── Column headers (row 3 = terminal group, row 4 = subtype) ─────────────
    row = 3
    ws.merge_cells(start_row=row, start_column=1, end_row=row+1, end_column=1)
    write_cell(ws, row, 1, 'Time Block', bold=True, bg='1B2B5A', font_color='FFFFFF')

    terminal_colors = ['2563EB', '7C3AED', '059669', 'DC2626', 'D97706']
    col = 2
    for i, t in enumerate(TERMINALS):
        short = t.replace('TERMINAL ', 'T')
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+2)
        write_cell(ws, row, col, short, bold=True, bg=terminal_colors[i], font_color='FFFFFF')
        write_cell(ws, row+1, col,   'Bag Wraps',    bold=True, bg='DBEAFE', font_size=9)
        write_cell(ws, row+1, col+1, 'Box Wraps',    bold=True, bg='EDE9FE', font_size=9)
        write_cell(ws, row+1, col+2, 'Foot Traffic', bold=True, bg='D1FAE5', font_size=9)
        col += 3

    # Totals headers
    ws.merge_cells(start_row=row, start_column=col, end_row=row+1, end_column=col)
    write_cell(ws, row, col,   'Total Bags',  bold=True, bg='1E3A5F', font_color='FFFFFF')
    ws.merge_cells(start_row=row, start_column=col+1, end_row=row+1, end_column=col+1)
    write_cell(ws, row, col+1, 'Total Boxes', bold=True, bg='1E3A5F', font_color='FFFFFF')
    ws.merge_cells(start_row=row, start_column=col+2, end_row=row+1, end_column=col+2)
    write_cell(ws, row, col+2, 'Total Foot',  bold=True, bg='1E3A5F', font_color='FFFFFF')

    ws.row_dimensions[row].height   = 20
    ws.row_dimensions[row+1].height = 16

    # ── Data rows ─────────────────────────────────────────────────────────────
    data_start = row + 2
    blocks_with_data = sorted(data.keys()) if data.keys() else SHIFT_BLOCKS[:6]

    for i, block in enumerate(blocks_with_data):
        r  = data_start + i
        bg = 'F8FAFF' if i % 2 == 0 else 'FFFFFF'
        write_cell(ws, r, 1, block, bg=bg, font_size=9)

        col = 2
        row_bags = row_boxes = row_foot = 0
        for t in TERMINALS:
            bags  = data[block][t].get('bag_wrap', 0)
            boxes = data[block][t].get('box_wrap', 0)
            foot  = data[block][t].get('foot_traffic', 0)
            row_bags  += bags
            row_boxes += boxes
            row_foot  += foot
            write_cell(ws, r, col,   bags  or '', bg=bg, font_size=9)
            write_cell(ws, r, col+1, boxes or '', bg=bg, font_size=9)
            write_cell(ws, r, col+2, foot  or '', bg=bg, font_size=9)
            col += 3

        write_cell(ws, r, col,   row_bags  or '', bold=True, bg='EFF6FF', font_size=9)
        write_cell(ws, r, col+1, row_boxes or '', bold=True, bg='F5F3FF', font_size=9)
        write_cell(ws, r, col+2, row_foot  or '', bold=True, bg='ECFDF5', font_size=9)

    # ── Totals row ────────────────────────────────────────────────────────────
    total_row = data_start + len(blocks_with_data)
    write_cell(ws, total_row, 1, 'TOTAL', bold=True, bg='1B2B5A', font_color='FFFFFF')
    col = 2
    grand_bags = grand_boxes = grand_foot = 0
    for t in TERMINALS:
        t_bags  = sum(data[b][t].get('bag_wrap', 0)    for b in blocks_with_data)
        t_boxes = sum(data[b][t].get('box_wrap', 0)    for b in blocks_with_data)
        t_foot  = sum(data[b][t].get('foot_traffic', 0) for b in blocks_with_data)
        grand_bags  += t_bags
        grand_boxes += t_boxes
        grand_foot  += t_foot
        write_cell(ws, total_row, col,   t_bags  or '', bold=True, bg='DBEAFE')
        write_cell(ws, total_row, col+1, t_boxes or '', bold=True, bg='EDE9FE')
        write_cell(ws, total_row, col+2, t_foot  or '', bold=True, bg='D1FAE5')
        col += 3

    write_cell(ws, total_row, col,   grand_bags,  bold=True, bg='1E3A5F', font_color='FFFFFF')
    write_cell(ws, total_row, col+1, grand_boxes, bold=True, bg='1E3A5F', font_color='FFFFFF')
    write_cell(ws, total_row, col+2, grand_foot,  bold=True, bg='1E3A5F', font_color='FFFFFF')
    ws.row_dimensions[total_row].height = 18

    # ── Column widths ─────────────────────────────────────────────────────────
    ws.column_dimensions['A'].width = 16
    for c in range(2, col+3):
        ws.column_dimensions[get_column_letter(c)].width = 11


def _build_shop_sheet(ws, events, shift_date):
    shop_events = [e for e in events if e['location_category'] == 'shop']

    # Aggregate: block -> shop -> event_type -> count + receipt timestamps
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    receipts_by_block = defaultdict(lambda: defaultdict(list))

    for e in shop_events:
        data[e['time_block']][e['location']][e['event_type']] += 1
        if e['event_type'] == 'receipt':
            t = e['timestamp'].split(' ')[1][:5] if ' ' in e['timestamp'] else e['timestamp']
            receipts_by_block[e['time_block']][e['location']].append(t)

    # ── Title row ─────────────────────────────────────────────────────────────
    total_cols = 1 + len(SHOPS) * 3
    ws.merge_cells(f'A1:{get_column_letter(total_cols)}1')
    ws['A1'].value = "CCTV DAILY REPORT – SHOP INTERACTIONS"
    ws['A1'].font = Font(bold=True, size=14, color='FFFFFF', name='Arial')
    ws['A1'].fill = PatternFill("solid", fgColor='1B2B5A')
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30

    ws.merge_cells(f'A2:{get_column_letter(total_cols)}2')
    ws['A2'].value = f"Date: {shift_date}"
    ws['A2'].font = Font(bold=True, size=11, name='Arial')
    ws['A2'].alignment = Alignment(horizontal='center')

    # ── Column headers ────────────────────────────────────────────────────────
    row = 3
    ws.merge_cells(start_row=row, start_column=1, end_row=row+1, end_column=1)
    write_cell(ws, row, 1, 'Time Block', bold=True, bg='1B2B5A', font_color='FFFFFF')

    shop_colors = ['F59E0B', 'EF4444', '8B5CF6', '10B981', '3B82F6']
    col = 2
    for i, shop in enumerate(SHOPS):
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+2)
        write_cell(ws, row, col, shop, bold=True, bg=shop_colors[i],
                   font_color='FFFFFF', wrap=True)
        write_cell(ws, row+1, col,   'Interactions', bold=True, bg='FEF3C7', font_size=9)
        write_cell(ws, row+1, col+1, 'Walk-ins',     bold=True, bg='FEE2E2', font_size=9)
        write_cell(ws, row+1, col+2, 'Receipts',     bold=True, bg='D1FAE5', font_size=9)
        col += 3

    ws.row_dimensions[row].height   = 22
    ws.row_dimensions[row+1].height = 16

    # ── Data rows ─────────────────────────────────────────────────────────────
    blocks_with_data = sorted(data.keys()) if data.keys() else SHIFT_BLOCKS[:6]
    data_start = row + 2

    for i, block in enumerate(blocks_with_data):
        r  = data_start + i
        bg = 'FFFBF0' if i % 2 == 0 else 'FFFFFF'
        write_cell(ws, r, 1, block, bg=bg, font_size=9)

        col = 2
        for shop in SHOPS:
            interactions    = data[block][shop].get('interaction', 0)
            walkins         = data[block][shop].get('walkin', 0)
            receipt_times   = receipts_by_block[block][shop]
            receipt_display = ', '.join(receipt_times) if receipt_times else ''
            write_cell(ws, r, col,   interactions    or '',  bg=bg, font_size=9)
            write_cell(ws, r, col+1, walkins         or '',  bg=bg, font_size=9)
            write_cell(ws, r, col+2, receipt_display or '',  bg=bg, font_size=8,
                       align='left', wrap=True)
            col += 3

    # ── Totals row ────────────────────────────────────────────────────────────
    total_row = data_start + len(blocks_with_data)
    write_cell(ws, total_row, 1, 'TOTAL', bold=True, bg='1B2B5A', font_color='FFFFFF')
    col = 2
    for shop in SHOPS:
        t_inter = sum(data[b][shop].get('interaction', 0) for b in blocks_with_data)
        t_walk  = sum(data[b][shop].get('walkin', 0)      for b in blocks_with_data)
        t_rec   = sum(data[b][shop].get('receipt', 0)     for b in blocks_with_data)
        write_cell(ws, total_row, col,   t_inter, bold=True, bg='FEF3C7')
        write_cell(ws, total_row, col+1, t_walk,  bold=True, bg='FEE2E2')
        write_cell(ws, total_row, col+2, t_rec,   bold=True, bg='D1FAE5')
        col += 3
    ws.row_dimensions[total_row].height = 18

    # ── Column widths ─────────────────────────────────────────────────────────
    ws.column_dimensions['A'].width = 16
    for c in range(2, col+1):
        ws.column_dimensions[get_column_letter(c)].width = 13


def _build_raw_log(ws, events):
    ws.merge_cells('A1:G1')
    ws['A1'].value = "RAW EVENT LOG"
    ws['A1'].font = Font(bold=True, size=13, color='FFFFFF', name='Arial')
    ws['A1'].fill = PatternFill("solid", fgColor='1B2B5A')
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 25

    headers = ['#', 'Timestamp', 'Location', 'Category', 'Event Type', 'Subtype', 'Time Block']
    for col, h in enumerate(headers, 1):
        write_cell(ws, 2, col, h, bold=True, bg='2563EB', font_color='FFFFFF')

    for i, e in enumerate(events, 1):
        r  = i + 2
        bg = 'F8FAFF' if i % 2 == 0 else 'FFFFFF'
        write_cell(ws, r, 1, i,                                                  bg=bg, font_size=9)
        write_cell(ws, r, 2, e['timestamp'],                                     bg=bg, font_size=9, align='left')
        write_cell(ws, r, 3, e['location'],                                      bg=bg, font_size=9, align='left')
        write_cell(ws, r, 4, e['location_category'].upper(),                     bg=bg, font_size=9)
        write_cell(ws, r, 5, e['event_type'].upper(),                            bg=bg, font_size=9)
        write_cell(ws, r, 6, e.get('subtype', '').replace('_', ' ').title(),     bg=bg, font_size=9)
        write_cell(ws, r, 7, e['time_block'],                                    bg=bg, font_size=9)

    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 28
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 14
    ws.column_dimensions['F'].width = 14
    ws.column_dimensions['G'].width = 16