import os
import csv

def appendData(Name = 'Null', E_List = [], E_correct_List = [], VA_left = '', VA_right = '',
             E_Lt_List = [], E_correct_Lt_List = [], E_Rt_List = [], E_correct_Rt_List = [],
             Response_time_left = [], Response_time_right = [], total_time = 0.0):

    with open('VA_Data.csv', 'a', newline='') as f:
        file_is_empty = os.stat('VA_Data.csv').st_size == 0

        fieldnames = ['Name', 'E List', 'E Correctness List', 'VA left eye', 'VA right eye',
             'E List Left', 'E List: Correctness Lt. Eye', 'E List Right', 'E List: Correctness Rt. Eye',
             'Response time Lt. Eye', 'Response time Rt. Eye', 'Total Test time']
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if file_is_empty:
            writer.writeheader()

        writer.writerow({'Name' : Name, 'E List' : E_List, 'E Correctness List' : E_correct_List,
             'VA left eye' : VA_left, 'VA right eye' : VA_right,
             'E List Left' : E_Lt_List, 'E List: Correctness Lt. Eye' : E_correct_Lt_List, 
             'E List Right' : E_Rt_List, 'E List: Correctness Rt. Eye' : E_correct_Rt_List,
             'Response time Lt. Eye' : Response_time_left, 'Response time Rt. Eye' : Response_time_right,
             'Total Test time' : total_time})