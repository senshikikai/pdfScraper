#PDF SCRAPER   - by @ senshikikai
#gets the job done but still needs a lot of work

import tabula
import pandas as pd


input_file = "PACKING.pdf"
output_file = "PACKING.xlsx"

#scrap data from pdf
dfs = tabula.read_pdf(input_file,pages = 'all',stream=True,guess=False,relative_area=True,area=(40,5,95,60),columns=[160,330],encoding='utf-8-sig')


i=0
for df in dfs:
	dfs[i].columns = ["sku", "description", "quantity" ]
	i=i+1


output_df = pd.concat(dfs)
output_df = output_df.groupby(['sku','description'], as_index=False).sum()

#save data of xlsx file
output_df.to_excel(output_file,index=False)

