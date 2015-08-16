from xlrd import open_workbook,cellname
wb = open_workbook('Book1.xlsx')
values=[]
s1 = wb.sheet_by_index(2) # or: sheet_by_name(Sheet 1")
print s1.nrows
c=':'
j=-1
bits=[]
for row_index in xrange(s1.nrows):
	#for col_index in xrange(s1.ncols):
		col_index=1
		if(s1.cell(rowx=row_index,colx=col_index).value!="Bits"):
			values.append(s1.cell(rowx=row_index,colx=col_index).value)
			j=j+1
			try:
				if(values[j].find(c)):
					i=values[j].find(c)
					k=int(str(values[j])[i-1])-int(str(values[j])[i+1])+1
					bits.append(k)
			except:
				pass
print bits,len(bits)		    