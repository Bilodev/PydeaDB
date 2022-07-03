import os
import pandas as pd
import csv  
from rich.console import Console
from rich.table import Table


class Folder:
    
    def __init__(self,path_to_mother_file: str) -> None:
        self.mother_folder = path_to_mother_file
        
        try:
            os.mkdir(path_to_mother_file)
            print("Let's get work done")
            
        except FileExistsError:
            pass
          
    def add_folder(self,collection_name: list)-> None:
        for i in collection_name:
            try:
                os.mkdir(f'{self.mother_folder}\\{i}')
            except FileExistsError:
                pass
    
    def create_file(self,file_name: list) -> None:
        
            for i in file_name:
                if not os.path.exists(f'{self.mother_folder}\\{i}.csv'):
                    f = open(f'{self.mother_folder}\\{i}.csv','a') 
                    f.write('#')
            
    @staticmethod
    def remove(path_to_content:str) -> None:
        os.remove(path_to_content)
    
    def view_content(self) -> None:
        print(os.listdir(self.mother_folder))
        
    def __repr__(self) -> str:
        self.view_content()
        return f'\nPath: {self.mother_folder}'



class File:    
    
    def __init__(self, file: str) -> None:
        if os.path.exists(f'{file}.csv'): self.file = file+'.csv'
        else: raise FileNotFoundError
    
    def add_column(self,col_name: str):
        '''remove added column from row or it could create some issues'''
        df = pd.read_csv(self.file)
        if str(col_name) in df.columns: return
        df[str(col_name)] = ""
        os.remove(self.file)
        df.to_csv(self.file, index=False)
        
    def add_columns(self,cols: list):
        for i in cols:
            self.add_column(i)
        
    def add_row(self, row: list):
        df = pd.read_csv(self.file)
        
        if len(df.columns) <= len(row): raise ValueError('It seems like you have passed too many arguments')
        
        row.insert(0,len(df)+1)
        with open(self.file, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(row) 
    
    
    def delete_byindex(self, pos: int, failed='Position Not Found'):
        
        df = pd.read_csv(self.file)
        for i in pos:
            try:        
                df.drop(i-1, inplace=True) 
            except:
                return failed

            df.loc[i-1:,'#'] -=1
            os.remove(self.file)
            df.to_csv(self.file, index=False)
        return 'Ok'
    
        
    
    def show_table(self):
        
        table = Table(show_header=True, header_style='bold blue')
        console = Console()
        
        df = pd.read_csv(self.file)
        
        [table.add_column(i,style='dim') for i in df.columns]
            
        for i in range(len(df)):
            
            t = (list(df.iloc[i])) # converto in lista ogni riga
            
            t = tuple([str(i) for i in t]) # converto la riga in stringa perche non posso fare l'unpack di una lista (per inserire la row)
            
            table.add_row(*(t), style='bold #6be9ff') # insert finale
    
        console.print(table)
    
        
       
    def search(self, filter: dict):
        return filter

    def set_column(self,column: str, attribute):
        '''Update a column  for all rows and creates it if its not exist'''
        df = pd.read_csv(self.file)
        df[column] = attribute
        os.remove(self.file)
        df.to_csv(self.file, index=False)
        
    def remove_column(self,column: str):
        df = pd.read_csv(self.file)
        try:
            df.drop(column, axis=1, inplace=True)
        except:
            print('column not found')
            return
        os.remove(self.file)
        df.to_csv(self.file, index=False)
        
    def __repr__(self) -> str:
        self.show_table()
        return ''
        
        
    def search_and_delete():
        pass
    
   
    def search_and_update():
        pass
    
    