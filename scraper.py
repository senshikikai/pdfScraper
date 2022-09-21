#PDF SCRAPER   - by @ senshikikai
#gets the job done but still needs a lot of work

import tabula
import pandas as pd
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Progressbar
import os

ws = Tk()
ws.title('PDF scraper')
ws.geometry('400x100')

pb = Progressbar(ws, orient = HORIZONTAL, length = 300, mode = 'determinate')
pb.place(x=40, y=20)

txt = Label(ws, text = '0%', fg = '#fff')
txt.place(x=350 ,y=20 )

txt_status = Label(ws, text ='Open PDF file...')
txt_status.place(x=40, y = 50)

input_file = "PACKING.pdf"
output_file = "PACKING.xlsx"

input_file = filedialog.askopenfilename(filetypes=[("PDF files", ".pdf")])

if not input_file: quit()
 
f = os.path.basename(input_file)
f_name, fext = os.path.splitext(f)

output_file = filedialog.asksaveasfilename(initialfile=f_name, filetypes=[("Excel files", ".xlsx")])

if not output_file: quit()

txt_status['text'] = "Reading PDF File..."
ws.update_idletasks()

#scrap data from pdf
dfs = tabula.read_pdf(input_file,pages = 'all',stream=True,guess=False,relative_area=True,area=(40,5,95,60),columns=[160,330],encoding='utf-8-sig')
unit_prog = 100 / len(dfs)
a_prog = 0
txt_status['text'] = "Processing Data..."
ws.update_idletasks()
#work page by page
for df in dfs:
	a_prog = a_prog + 1
	pb['value'] = (a_prog * unit_prog)
	txt['text']=pb['value'],'%'
	ws.update_idletasks()
	df.columns = ["sku","description","quantity"]
	#remove rows not needed and order the info
	i_len = len(df)-1
	for ind in range(i_len,-1,-1):
		i = ind-1
		s_input  = df.iat[ind,0]
		if ("EAN:" in str(s_input)) or  (pd.isna(df.iat[ind,2]) and (not(pd.isna(s_input)))):
			df.drop(ind, inplace = True)
			continue
		if pd.isna(df.iat[ind,2]):
			s_desc = df.iat[i,1] + " " + df.iat[ind,1]
			df.iat[i,1] = s_desc
			df.drop(df.index[ind], inplace=True)
#put all pages together
output_df = pd.concat(dfs)
output_df = output_df.groupby(['sku','description'], as_index=False).sum()

txt_status['text'] = "Saving Data..."
ws.update_idletasks()

#save data of xlsx file
output_df.to_excel(output_file,index=False)
