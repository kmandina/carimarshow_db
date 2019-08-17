import os, sys
from subprocess import Popen, PIPE

########################################################################
# Repositorio de la bd
origin = 'https://github.com/kmandina/carimarshow_db.git'
branch = 'master'

# Tablas de la base de datos
tables = ('producto','tipo','categoria','configuracion','ayuda','contacto','upload_file')

# Plataforma en la que se ejecuta el archivo (puede ser linux2 o win32)
platform = sys.platform

# Ruta de este archivo
root = os.path.normpath(os.getcwd())

# Ruta relativa a la carpeta del api desde la ruta de este archivo
apiRoute = os.path.normpath(root+'/../carimarshowapi')
publicFolderApiRoute = os.path.normpath(apiRoute+'/public')

# Ruta relativa a la carpeta de la bd desde la ruta de este archivo
dbRoute = os.path.normpath(root+'/../carimarshow_db')
publicFolderDbRoute = os.path.normpath(dbRoute+'/public')

# Credenciales
user = 'carimarshowapk@gmail.com'
password = 'carimarshow123.com'
########################################################################

def main():
        message = '''Seleccione una opcion:
        0.- Terminar
        1.- Descargar base de datos desde git
        2.- Subir cambios al git
        3.- Iniciar API (en desarrollo)
        4.- Iniciar Administracion (en desarrollo)
        5.- Iniciar BD (en desarrollo)
        '''
        option = int(input(message))

        if option == 0:
                exit()
        elif option == 1:
                pullFromGit()
        elif option == 2:
                pushToGit()
        else:
        	print('Opcion incorrecta')
        	main()
        # elif option == 3:
                # exportdb()
                # copyFolder(os.path.normpath(root+'/t'),os.path.normpath(root+'/t1'))


def pullFromGit():
        # si no existe la carpeta de la bd clonar, sino actualizar
        cloneOrPull()
        # limpiar la bd carimarshow
        cleandb()
        # Importar los archivos .json hacia la bd
        importdb()
        # borrar carpeta public del api
        eraseFolder(publicFolderApiRoute)
        # copiar contenido de la carpeta public de la bd hacia la carpeta public del api
        copyFolder(publicFolderDbRoute,publicFolderApiRoute)

        main()

def pushToGit():
        if folderExist(dbRoute):
                # exportar las tablas de la bd
                exportdb()
                # borrar contenido de la carpeta public dentro de la carpeta de la bd
                eraseFolder(publicFolderDbRoute)
                # copiar el contenido de la carpeta public del api hacia la carpeta de la bd
                copyFolder(publicFolderApiRoute,publicFolderDbRoute)
                # subir cambios a github
                push()
        else:
                print('La carpeta de la bd no existe, debe primero clonarla desde github')

        main()

def folderExist(path):
        return os.access(path,0) == 1

def push():
        os.chdir(dbRoute)
        proceso = Popen(['git','push', '-f'], stderr=PIPE)
                
        error = proceso.stderr.read()
        proceso.stderr.close()
        os.chdir(root)
        if error:
                print(error)
                exit()
        else:
                print('Github actualizado satisfactoriamente')

def cloneOrPull():
        if folderExist(dbRoute):  # Si la carpeta de la bd existe hacer pull y actualizar
                os.chdir(dbRoute)
                proceso = Popen(['git','pull', '-f'], stderr=PIPE)
        else:   # Si la carpeta de la bd no existe entonces clonarla
                print('La carpeta de la bd no existe, clonando...')
                proceso = Popen(['git','clone', origin, dbRoute], stderr=PIPE)
                
        error = proceso.stderr.read()
        proceso.stderr.close()
        os.chdir(root)
        print(error)

def eraseFolder(path):
		if folderExist(publicFolderDbRoute):
		        if platform == 'win32':
		                proceso = Popen(['cmd.exe','/c','rmdir', '/q', '/s', path], stderr=PIPE)
		        elif platform == 'linux2':
		                proceso = Popen(['rm', '-r', path], stderr=PIPE)
		                
		        error = proceso.stderr.read()
		        proceso.stderr.close()

		        if error:
		                print(error)
		                exit()

    		print('Carpeta \"'+path+'\" eliminada satisfactoriamente')

def copyFolder(pathFrom, pathTo):
        if platform == 'win32':
                proceso = Popen(['cmd.exe','/c','xcopy', '/e', '/i', pathFrom, pathTo], stderr=PIPE)
        elif platform == 'linux2':
                proceso = Popen(['cp', '-rp', pathFrom, pathTo], stderr=PIPE)

        print('Copiando archivos')
        error = proceso.stderr.read()
        proceso.stderr.close()

        if error:
                print(error)
                exit()
        else:
                print('Copia terminada satisfactoriamente')

def importdb():
        os.chdir(dbRoute)
        for table in tables:
                if platform == 'win32':
                        proceso = Popen(['cmd.exe','/c',"C:\Program Files\MongoDB\Server\\3.5\\bin\mongoimport.exe",'--db','carimarshow','-c',table,'--file',table+'.json'], stderr=PIPE)
                elif platform == 'linux2':
                        proceso = Popen(['mongoimport','--db','carimarshow','-c',table,'--file',table+'.json'], stderr=PIPE)

                error = proceso.stderr.read()
                proceso.stderr.close()

                print(error)
        os.chdir(root)


def exportdb():
    os.chdir(dbRoute)
    for table in tables:
            if platform == 'win32':
                    proceso = Popen(['cmd.exe','/c',"C:\Program Files\MongoDB\Server\\3.5\\bin\mongoexport.exe",'--db','carimarshow','-c',table,'--out',table+'.json'], stderr=PIPE)
            elif platform == 'linux2':
                    proceso = Popen(['mongoexport','-d','carimarshow','-c',table,'--out',table+'.json'], stderr=PIPE)

            error = proceso.stderr.read()
            proceso.stderr.close()

            print(error)
    os.chdir(root)

def cleandb():
    os.chdir(dbRoute)
    for table in tables:
            if platform == 'win32':
                    proceso = Popen(['cmd.exe','/c',"C:\Program Files\MongoDB\Server\\3.5\\bin\mongo.exe",'carimarshow','--eval',"db."+table+".drop()"], stderr=PIPE)
            elif platform == 'linux2':
                    proceso = Popen(['mongo','carimarshow','--eval',"db."+table+".drop()"], stderr=PIPE)

            error = proceso.stderr.read()
            proceso.stderr.close()

            print(error)
    os.chdir(root)	

main()
