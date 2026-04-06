Creating an excel table:
using the pandas database library You can export charts into spreadsheets using;
`data_basebase_name .to_excel("name_of_excelsheet.xlsx", index=False)`
this creates a file
index=false removes the index number row 
to make multiple sheets use:
`with pd.ExcelWriter("name_of_sheet.xllsx") as writer:`
	`qb_data_frame.to_excel(writer, sheet_name="QB", index=False)`
	`rb_data_frame.to_excel(writer, sheet_name="RB", index=False)`
	`wr_data_frame.to_excel(writer, sheet_name="WR", index=False)`
	`te_data_frame.to_excel(writer, sheet_name="TE", index=False)`
ExcelWriter is a class for writing dataframes into excel sheets
allows for more advanced operations like making files across different sheets, wont create a new file if the file is missing
to append or edit you have to use engine = 'openpyxl'
mode ='a' to append
if sheet exists choose to 'replace' or overlay
`with pd.ExcelWriter('existing_file.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:`
	`data_frame.to_excel(writer, sheet_name='NewSheet')`
