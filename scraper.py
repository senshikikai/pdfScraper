#PDF SCRAPER   - by @ senshikikai
#gets the job done but still needs a lot of work


import tabula
import pandas as pd


input_file = "PACKING.pdf"
output_file = "PACKING.xlsx"

#scrap data from pdf
dfs = tabula.read_pdf(input_file,pages = 'all',stream=True,guess=False,relative_area=True,area=(40,5,95,60),columns=[160,330],encoding='utf-8-sig')



for df in dfs:
	df.columns = ["sku","description","quantity"]
	
	##remove not needed rows
	i_len = len(df)-1	
	for ind in range(i_len,-1,-1):
		s_input  = df.iat[ind,0]
		if ("EAN:" in str(s_input)) or  (pd.isna(df.iat[ind,2]) and (not(pd.isna(s_input)))):
			df.drop(ind, inplace = True)
	
	
	#get the description text needed
	i_len = len(df)-1
	for ind in range(i_len,-1,-1):
		i = ind-1
		if pd.isna(df.iat[ind,2]):
			s_desc = df.iat[i,1] + " " + df.iat[ind,1]
			df.iat[i,1] = s_desc
			df.drop(df.index[ind], inplace=True)
	

output_df = pd.concat(dfs)
output_df = output_df.groupby(['sku','description'], as_index=False).sum()

#save data of xlsx file
output_df.to_excel(output_file,index=False)
