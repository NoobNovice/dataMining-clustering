import math
import numpy
import xlrd
import random


def read_exel(file_name, word):
    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheets()

    table =[]
    if word == "cr":
        for col in range(worksheet[0].ncols): # read except header
            att = []

            for row in range(1, worksheet[0].nrows): # read except ID
                data = worksheet[0].cell_value(row, col) # Read the data in the current cell
                att.append(data)

            table.append(att)
    elif word == "rc":
        for row in range(1, worksheet[0].nrows): # read except header
            att = []

            for col in range(0, worksheet[0].ncols): # read except ID
                data = worksheet[0].cell_value(row, col) # Read the data in the current cell
                att.append(data)

            table.append(att)
    return table

def null_list(num_list):
    list = []
    for i in range(num_list):
        arr = []
        list.append(arr)
    return list

def metrix_list(num_list):
    list = []
    for i in range(num_list):
        arr = [0]*num_list
        list.append(arr)
    return list

def distance(arr_x, arr_y):
    arr = numpy.subtract(arr_x, arr_y)
    sum_arr = 0
    for i in arr:
        sum_arr += math.pow(i, 2)
    return math.sqrt(sum_arr)

def sample_pull(threshold_distance, num_cluster, table):
    arr_group = null_list(num_cluster * 2)
    # set point
    for sample_index in range(len(arr_group)):
        random_index = random.randint(0, len(table) - 1)
        arr_group[sample_index].append(table[random_index])
        table.pop(random_index)
    # find 5 member near neighbor
    for sample_index in range(len(arr_group)):
        count = 0
        for i in range(len(table)):
            temp = distance(table[i], numpy.mean(arr_group[sample_index]))
            if count > 3:
                break
            if temp < threshold_distance:
                arr_group[sample_index].append(table[i])
                table.pop(i)
                count += 1
    return arr_group

def k_neighbor(num_cluster):
    #read excel
    table = read_exel("dataset2.xls", "rc")

    # set 5 sample in arr
    cluster_group = sample_pull(2, num_cluster, table)

    # group each member in to arr_group
    for data_row in table:
        distance_min = distance(data_row, numpy.mean(cluster_group[0]))
        index_min = 0
        for j in range(1, len(cluster_group)):
            temp = distance(data_row, numpy.mean(cluster_group[j]))
            if distance_min > temp:
                distance_min = temp
                index_min = j
        cluster_group[index_min].append(data_row)

    # find neighbor
    while len(cluster_group) > num_cluster:
        metrix = metrix_list(len(cluster_group))
        for ri in range(len(metrix)):
            for rj in range(len(metrix[ri])):
                if ri == rj:
                    metrix[ri][rj] = 0
                    break
                x = rj
                metrix[ri][x] = distance(numpy.mean(cluster_group[ri]), numpy.mean(cluster_group[rj]))
        min_metrix = metrix[0][0]
        ii = 0
        jj = 0
        for i in range(len(metrix)):
            for j in range(len(metrix)):
                if i != j and min_metrix > metrix[i][j]:
                    min_metrix = metrix[i][j]
                    ii = i
                    jj = j
        for item in range(len(cluster_group[ii])):
            cluster_group[jj].append(item)
        cluster_group.pop(ii)
    return cluster_group
