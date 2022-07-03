import os
from typing import Any
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
    
    def add_column(self,col_name: str) -> None:
        '''remove added column from row or it could create some issues'''
        df = pd.read_csv(self.file)
        if str(col_name) in df.columns: return
        df[str(col_name)] = ""
        os.remove(self.file)
        df.to_csv(self.file, index=False)
        
    def add_columns(self,cols: list) -> None:
        for i in cols:
            self.add_column(i)
        
    def add_row(self, row: list) -> None:
        df = pd.read_csv(self.file)
        
        if len(df.columns) <= len(row): raise ValueError('It seems like you have passed too many arguments')
        
        row.insert(0,len(df)+1)
        with open(self.file, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(row) 
    
    def delete_byindex(self, pos: int | list[int], failed='Position Not Found') ->  None | Any:
        
        df = pd.read_csv(self.file)
        
        if isinstance(pos,int):
            try:        
                df.drop(pos-1, inplace=True) 
            except:
                return failed
            df.loc[pos-1:,'#'] -=1
            os.remove(self.file)
            df.to_csv(self.file, index=False)
            return
        
        for i in pos:
            try:        
                df.drop(i-1, inplace=True) 
            except:
                return failed

            df.loc[i-1:,'#'] -=1
            os.remove(self.file)
            df.to_csv(self.file, index=False)
            
    def update_byindex(self,pos: int, newRow: dict) -> None:
        df = pd.read_csv(self.file)
        
        temp = {}
        temp['#'] = pos
        temp.update(newRow)
        newRow = temp
        
        df.loc[pos-1] = newRow
        
        os.remove(self.file)
        df.to_csv(self.file, index=False)
        
    
    def show_table(self) -> None:
        
        table = Table(show_header=True, header_style='bold blue')
        console = Console()
        
        df = pd.read_csv(self.file)
        
        [table.add_column(i,style='dim') for i in df.columns]
            
        for i in range(len(df)):
            
            t = (list(df.iloc[i])) # converto in lista ogni riga
            
            t = tuple([str(i) for i in t]) # converto la riga in stringa perche non posso fare l'unpack di una lista (per inserire la row)
            
            table.add_row(*(t), style='bold #6be9ff') # insert finale
    
        console.print(table)

    def set_column(self,column: str, attribute) -> None:
        '''Update a column  for all rows and creates it if its not exist'''
        df = pd.read_csv(self.file)
        df[column] = attribute
        os.remove(self.file)
        df.to_csv(self.file, index=False)
        
    def remove_column(self,column: str) -> None:
        df = pd.read_csv(self.file)
        try:
            df.drop(column, axis=1, inplace=True)
        except:
            return None
        os.remove(self.file)
        df.to_csv(self.file, index=False)
        
    def __repr__(self) -> str:
        self.show_table()
        return ''
        
    def query(self, query: str) -> dict | None:
        data = pd.read_csv(self.file)
        ris = data.query(query)
        if not ris.empty:
            return ris.to_dict('records')
        return None
        
    def search(self, filter: dict)-> list[dict] | None:
        data = pd.read_csv(self.file)
        for key,value in filter.items():            
                ris = data[data[key] == value]
                if ris.empty:
                    return None
                data = ris
        return ris.to_dict('records')
    
    
    def delete(self, query: str) -> None:
        ris = self.query(query)
        f = [i['#'] for i in ris]
        self.delete_byindex(f)
        
    
   
    def update(self, query: str, newRow: dict) -> None:
        ris = self.query(query)
        for i in ris:
            self.update_byindex(i['#'],newRow)
       
