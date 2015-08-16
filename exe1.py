from xlrd import open_workbook,cellname
import xlsxwriter
wb = xlsxwriter.Workbook('Book2.xlsx')
ws1=wb.add_worksheet()
ws1.write('A1','Device Marking')
ws1.write_comment('A1','Aurix ',{'x_offset':1000,'y_offset':200,'start_cell':'K1'})
wb.close()
