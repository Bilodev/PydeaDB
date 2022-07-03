import os
import typer

# py .\build.py 'Amongus' 'C:\Users\UTENTE\Desktop\Programmazione\python\'

app = typer.Typer()

@app.command(short_help='Build Project folder by given name and path')
def build(name: str, path: str):
    
    path = path+name
    os.mkdir(path)
    main = open(path+'\\main','w')
    os.mkdir(path+'\\'+name+'Db')
    open(path+'\\.gitignore','w').write('.env')
    open(path+'\\.env','w')
    open(path+'\\README.md','w').write('----------------------------------------------\nThis is a project built with PydeaDB\nWhich is A simple in-local database, built on top of pandas, with a small ecosystem and also is open source\nSource:  https://github.com/Bilodev/PydeaDB')
    
    
    main.write('from pydea import PydeaDB\n')
    main.write('\n\ndef main() -> None :')
    main.write(f"\n\tMainFolder = PydeaDB.Folder('{name}Db')")

    main.write('\n \n')
    main.write("if __name__ == '__main__':\n\tmain()\n")

    print('Built Successfully')
    

if __name__ == '__main__':
    app()
