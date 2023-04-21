from main import get_input_file_paths, DataFile

files = get_input_file_paths()

arq = DataFile(files[0])

df = arq.sites_df

df.set_index(df.columns[0], inplace=True)

#print(df.index)

arq.process_sites_df()

ret = arq.final_df

print(ret.head())