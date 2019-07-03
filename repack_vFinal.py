#!/usr/bin/env python
# /home/oracle/Documentos/SeteoIzzi/WEB-INF/lib
import os, sys
from os import walk
import subprocess
import shutil
import string

def empaquetar(array):
    for line in array[::-1]:
	tmpFile = line.split(",")
	sourcePath = tmpFile[0]
	sourceFileName = tmpFile[1]
        sourceDir = tmpFile[2] 
        #Ejecucion de metodo de empaquetado
        os.chdir(sourceDir)
        print("###################Compresion####################")
	compressCommand= 'jar', 'cvM0f', sourceFileName , '-C', sourcePath + '/', '.'
        print(compressCommand) 
        bash_exec(compressCommand)
        repacked_file_size = os.path.getsize(sourceFileName)
        shutil.rmtree(sourcePath)
	print ("Tamano compresion: "+ sourceFileName+ " "+ str(repacked_file_size))

#funcion para reemplazar
def sed(finalCommand):
    print (finalCommand)
    os.system(finalCommand)

def ejecutarsed(archivo,path,name):
    #lee archivo y lo itera
    print (archivo)
    fileReaded = open(archivo)
    for line in fileReaded:
        lineInfo = line.split(",")
        urlOrg = lineInfo[0].strip()
        urlDes = lineInfo[1].strip()
        connStringSourceInfo = urlOrg.split("/")
        hostpuertoSource = connStringSourceInfo[2].strip()
        servicesidSource = connStringSourceInfo[3].strip()
        print (hostpuertoSource)
        print (servicesidSource)
        print ("separando hostpuerto")
     
        hostpuertoSInfo = hostpuertoSource.split(":")
        hostSource=hostpuertoSInfo[0].strip()
        portSource=hostpuertoSInfo[1].strip()
        print (hostSource)
        print (portSource)
        print ("--------------endejecutarSed Origen----------------")
        print ("--------------ejecutarSed Destino-------------------")
        connStringInfoTarget = urlDes.split("/")
        hostpuertoTarget = connStringInfoTarget[2].strip()
        servicesidTarget = connStringInfoTarget[3].strip()
        print (hostpuertoTarget)
        print (servicesidTarget)
        print ("separando hostpuerto")
        hostpuertoTInfo = hostpuertoTarget.split(":")
        hostTarget=hostpuertoTInfo[0].strip()
        portTarget=hostpuertoTInfo[1].strip()
        print (hostTarget)
        print (portTarget)
        print ("--------------endejecutarSed Destino----------------")
        print("......path......",path)
        print("......name......",name)
        finalCommandHost = 'sed -i \'s/'+hostSource+'/'+hostTarget+'/g\' ' + path + '/'+ name
        finalCommandServSid = 'sed -i \'s/'+servicesidSource+'/'+servicesidTarget+'/g\' ' + path+ '/'+ name
        finalCommandPort = 'sed -i \'s/'+portSource+'/'+portTarget+'/g\' ' + path+ '/'+ name
        print('...ejecuta el sed...')
        sed(finalCommandHost)
        print("......finalCommandHost......",finalCommandHost)
        sed(finalCommandServSid)
        print("......finalCommandServSid......",finalCommandServSid)
        sed(finalCommandPort)
        print("......finalCommandPort......",finalCommandHost)

     
#funcion comprimir y descomprimir     
def uncompressAndRepackWar(source_path,tmp_dir_name,archivo,listaArchivos):
    abs_source_path = os.path.abspath(source_path+"/"+tmp_dir_name)
        
    listSplit = tmp_dir_name.split(".")
    tmp_dir_lastname = listSplit[0]
    tmp_ext_file = listSplit[1]
     
    print('--tmp_dir_name--', tmp_dir_lastname)
    print('--tmp_ext_file--', tmp_ext_file)
        
    source_dir, source_filename = os.path.split(abs_source_path)
    abs_tmp_dir = os.path.join(source_dir, tmp_dir_lastname)

        
    orig_file_size = os.path.getsize(abs_source_path)
    print('--source_dir--', source_dir)
    print('--ource_filename--', source_filename)
    print('--abs_tmp_dir--', abs_tmp_dir)
    print('--orig_file_size--', orig_file_size)
    
    if ("jar" == tmp_ext_file or "war"==tmp_ext_file or "ear"==tmp_ext_file or "rar"==tmp_ext_file or "tar"==tmp_ext_file or "zip" == tmp_ext_file):
        print ('entra a validacion==>')
        if os.path.exists(abs_tmp_dir):
        #valida ruta y elimina directorio
            shutil.rmtree(abs_tmp_dir)
        os.mkdir(abs_tmp_dir)
        os.chdir(abs_tmp_dir)
        listaArchivos.append(abs_tmp_dir+","+source_filename+","+source_dir)
        print (abs_source_path)
        bash_exec([
            'jar', 'xvf', abs_source_path
        ])     
     #aplica recursividad para las carpetas hijas
        os.chdir('..')
        name = ""
    for path, subdirs, files in os.walk(abs_tmp_dir,topdown=True):
        for name in files:
           asw = os.path.join(path, name)
           ejecutarsed(archivo, path, name)
           uncompressAndRepackWar(path, name, archivo, listaArchivos) 
           #no llamar al funcion directamente
           print("Archivo: ", name)
           
   

def bash_exec(command, printOut=True):
    def print_result(retcode, output=''):
        print('ERROR result code [%d] while calling: %s\n\n%s' % (retcode, ' '.join(command), output))

    def _bash_exec(command):        
        try:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while(True):
                retcode = p.poll() #returns None while subprocess is running
                line = p.stdout.readline()
                yield line.strip()
                if retcode is not None:
                    break
            if retcode != 0:
                print_result(retcode)
        except subprocess.CalledProcessError as CPE:
            print_result(CPE.returncode, CPE.output)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    for line in _bash_exec(command):
        if printOut:
            print(line)
        else:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("must provide path!")
    array = []
    uncompressAndRepackWar(sys.argv[1],sys.argv[2],sys.argv[3], array)
    print (array)
    empaquetar(array)

