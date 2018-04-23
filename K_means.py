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

def distance(arr_x, arr_y):
    arr = numpy.subtract(arr_x, arr_y)
    sum_arr = 0
    for i in arr:
        sum_arr += math.pow(i, 2)
    return math.sqrt(sum_arr)

def error(arr_point_x,arr_point_y):
    min_distance = distance(arr_point_x[0], arr_point_y[0])

    for index in range(1, len(arr_point_x)):
        temp = distance(arr_point_x[index], arr_point_y[index])
        if min_distance > temp:
            min_distance = temp

    return min_distance

def k_means(num_cluster, threshold):
    table = read_exel("dataset2.xls", "cr")
    invert_table = read_exel("dataset2.xls", "rc") #pull row

    print("set point part")
    point = []
    temp_point = []
    for i in range(num_cluster):
        arr = []
        for j in range(len(table)):
            arr.append(random.triangular(min(table[j]), max(table[j])))
        point.append(arr)
        temp_point.append([0]*len(table))
        print(point[i])
        print(temp_point[i])

    print("calculate part")
    cluster_group = null_list(num_cluster)
    pre_error = 0
    count = 0
    while error(point, temp_point) > threshold and count < 10:
        cluster_group = null_list(num_cluster)
        if pre_error == error(point, temp_point):
            count += 1
        pre_error = error(point, temp_point)
        print(error(point, temp_point))
        print(count)
        # group data
        for data_row in invert_table:
            distance_min = distance(data_row, point[0])
            index = 0
            for j in range(1, len(point)):
                temp = distance(data_row, point[j])
                if distance_min > temp:
                    distance_min = temp
                    index = j
            cluster_group[index].append(data_row)

        # adjust point
        for index_point in range(len(point)):
            point[index_point] = numpy.mean(cluster_group[index_point], axis=0)
    return cluster_group
