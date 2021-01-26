"""Module to hold all File I/O Functions"""
import time
import os


def readTXT(file_name):
    """Inputs a TXT file and outputs a list of lines"""
    lst = []
    f = open(file_name)
    for line in f:
        tmp = line.rstrip('\n')
        lst.append(tmp)
    # print 'Data read from: ' + file_name
    f.close()
    return lst


def readTAB(file_name):
    """Inputs a Tab Delimited File file and outputs a list of lines"""
    lst = []
    f = open(file_name)
    for line in f:
        tmp = line.rstrip('\n')
        tmp = tmp.replace('"', '')
        tmp = tmp.split('\t')
        lst.append(tmp)
    f.close()
    # print 'Data read from: ' + file_name
    return lst


def readCSV(file_name):
    '''Inputs a CSV file and outputs a list of lines'''
    lst = []
    f = open(file_name)
    for line in f:
        tmp = line.rstrip('\n')
        tmp = tmp.replace('"', '')
        tmp = tmp.split(',')
        lst.append(tmp)
    f.close()
    # print 'Data read from: ' + file_name
    return lst


def readCSV_fast(file_name):
    '''Inputs a CSV file and outputs a list of lines'''
    tmp_lst = []
    f = open(file_name)
    lst = f.read()
    lst = lst.split('\n')
    # print lst[0]
    for line in lst:
        # tmp = re.split(",+", line)
        # tmp = tmp.replace('"', '')
        tmp = line.split(',')
        tmp_lst.append(tmp)
    f.close()
    # print tmp_lst[1]
    # print 'Data read from: ' + file_name
    return tmp_lst

def readCSV_alpha(file_name):
    '''Inputs a CSV file and outputs a list of lines'''
    tmp_lst = []
    f = open(file_name)
    lst = f.read()
    lst = lst.split('\r')
    # print lst[0]
    for line in lst:
        # tmp = re.split(",+", line)
        # tmp = tmp.replace('"', '')
        tmp = line.split(',')
        tmp_lst.append(tmp)
    f.close()
    # print tmp_lst[1]
    # print 'Data read from: ' + file_name
    return tmp_lst


def writeCSV(file_name, lst):
    '''Inputs a list and then writes a CSV of file_name.csv'''
    f = open(file_name + '.csv', 'w')
    lst_tmp = []
    for i in range(0, len(lst)):
        if type(lst[i]) is str:
            tmp = lst[i]
        else:
            tmp = ''
            for j in range(0, len(lst[i])):
                tmp = tmp + str(lst[i][j]) + ','
        tmp = tmp.rstrip(",")
        tmp = tmp + '\n'
        lst_tmp.append(tmp)
    for i in range(0, len(lst_tmp)):
        f.write(lst_tmp[i])
    f.close()
    # print "Data written to: " + file_name + '.csv'


def writeCSVWithDate(file_name, lst):
    '''Inputs a list and then writes a CSV of file_name-YYYY-MM-DD.csv'''
    writeCSV(file_name + '-' + time.strftime('%Y-%m-%d-%H-%M-%S'), lst)


def writeTXT(file_name, lst):
    '''Inputs a list and then writes a CSV of file_name.txt'''
    f = open(file_name + ".txt", "w")
    for i in range(0, len(lst)):
        if type(lst[i]) is str:
            f.write(lst[i] + '\n')
        else:
            tmp = ''
            for j in range(0, len(lst[i])):
                tmp = tmp + str(lst[i][j]) + ', '
            tmp = tmp[:-2] + '\n'
            f.write(tmp)
    f.close()
    print('Data written to: ' + file_name + ".txt")


def writeTXTWithDate(file_name, lst):
    '''Inputs a list and then writes a TXT of file_name-YYYY-MM-DD.txt'''
    writeTXT(file_name + '-' + time.strftime('%Y-%m-%d'), lst)

def remove_files(dirPath):
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + '/' + fileName)
