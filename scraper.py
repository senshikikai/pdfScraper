import tabula
import pandas as pd




input_file = "PACKING.pdf"
df = tabula.read_pdf(input_file,pages = 'all',stream=True,guess=False,relative_area=True,area=(40,5,95,60),columns=[160,330],encoding='utf-8-sig')    #area=(20,5,95,92))

print(df)
