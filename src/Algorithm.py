import numpy as np

# 1.3 compare which one is the earlier one
def compare(active_time, passive_time):
    if active_time[0] > passive_time[0]:    
        print(f'Active management fund is later, so we use its time as the whole period, the begining time is {active_time[1]} {active_time[2]} in {active_time[0]} year')
        return active_time
    elif active_time[0] == passive_time[0]:
        if active_time[1] > passive_time[1]:
            print(f'Active management fund is later, so we use its time as the whole period, the begining time is {active_time[1]} {active_time[2]} in {active_time[0]} year')
            return active_time
        elif active_time[1] == passive_time[1]:
            if active_time[2] > passive_time[2]:
                print(f'Active management fund is later, so we use its time as the whole period, the begining time is {active_time[1]} {active_time[2]} in {active_time[0]} year')
                return active_time
            elif active_time[2] == passive_time[2]:
                print(f'Two funds started at the same time and we use this time as the whole period, the begining time is {active_time[1]} {active_time[2]} in {active_time[0]} year')
                return active_time
    else:
        print(f'Passive management fund is later, so we use its time as the whole period, the begining time is {passive_time[1]} {passive_time[2]} in {passive_time[0]} year')
        return passive_time

# 3.1 compare which frame has the longest column and combine the two frames of funds
def compare2(active_frame, passive_frame):
    a = active_frame.shape[0]
    p = passive_frame.shape[0]
    if a >= p:
        return active_frame
    else:
        return passive_frame
    
def combine(frame1, frame2, treasury):
    frame = compare2(frame1, frame2)
    list1 = []
    list2 = []
    list3 = []
    if frame.shape == frame1.shape:
        dic2 = {}
        for day in range(0, len(frame2['Date'])):
            if frame2['Date'][day] in list(frame1['Date']):
                dic2[frame2['Date'][day]] = frame2['Price'][day]
        for day in range(0, len(frame1['Date'])):
            if  frame1['Date'][day] in list(dic2.keys()):
                list2.append(dic2[frame1['Date'][day]])
            else:
                list2.append('NA')
        dic3 = {}
        for day in range(0, len(treasury['Date'])):
            if treasury['Date'][day] in list(frame1['Date']):
                dic3[treasury['Date'][day]] = treasury['Rate'][day]
        for day in range(0, len(frame1['Date'])):
            if  frame1['Date'][day] in list(dic3.keys()):
                list3.append(dic3[frame1['Date'][day]])
            else:
                list3.append('NA')
        frame.insert(2, 'New_Price', list2)
        frame.insert(3, 'Treasury_Rate', list3)
        return frame
    else:
        dic1 = {}
        for day in range(0, len(frame1['Date'])):
            if frame1['Date'][day] in list(frame2['Date']):
                dic1[frame1['Date'][day]] = frame1['Price'][day]
        for day in range(0, len(frame2['Date'])):
            if  frame2['Date'][day] in list(dic1.keys()):
                list1.append(dic1[frame2['Date'][day]])
            else:
                list1.append('NA')
        dic3 = {}
        for day in range(0, len(treasury['Date'])):
            if treasury['Date'][day] in list(frame2['Date']):
                dic3[treasury['Date'][day]] = treasury['Rate'][day]
        for day in range(0, len(frame2['Date'])):
            if  frame2['Date'][day] in list(dic3.keys()):
                list3.append(dic3[frame2['Date'][day]])
            else:
                list3.append('NA')
        frame.insert(2, 'New_Price', list1)
        frame.insert(3, 'Treasury_Rate', list3)
        return frame


# set the weight mechanism so that the weight can be adjusted every 5 days according to their return            
def update(list_in):
    update = []
    for i in range(0, len(list_in)):
        if list_in[i] == 'NA':
            list_in[i] = list_in[i-1]
        update.append(list_in[i])
    return update

def weight(rate1, rate2, rate3, together):    
    weight1 = []
    weight2 = []
    weight3 = []
    for i in range(0, len(together)):
        if rate1[i] > 0:
            if rate2[i] > 0:
                if rate2[i] > 0:
                    weight_1 = rate1[i] / together[i]
                    weight_2 = rate2[i] / together[i]
                    weight_3 = rate3[i] / together[i]
                    weight1.append(weight_1)
                    weight2.append(weight_2)
                    weight3.append(weight_3)
                else:
                    weight_1 = rate1[i] / (rate1[i] + rate2[i])
                    weight_2 = rate2[i] / (rate1[i] + rate2[i])
                    weight1.append(weight_1)
                    weight2.append(weight_2)
                    weight3.append(0)
            elif rate3[i] > 0:
                weight_1 = rate1[i] / (rate1[i] + rate3[i])
                weight_3 = rate3[i] / (rate1[i] + rate3[i])
                weight1.append(weight_1)
                weight3.append(weight_3)
                weight2.append(0)
            else:
                weight1.append(1)
                weight2.append(0)
                weight3.append(0)
        elif rate2[i] > 0:
            if rate3[i] > 0:
                weight_3 = rate3[i] / (rate3[i] + rate2[i])
                weight_2 = rate2[i] / (rate1[i] + rate2[i])
                weight3.append(weight_3)
                weight2.append(weight_2)
                weight1.append(0)
            else:
                weight1.append(0)
                weight2.append(1)
                weight3.append(0)
        elif rate3[i] > 0:
            weight1.append(0)
            weight2.append(0)
            weight3.append(1)
        else:
            weight1.append(0)
            weight2.append(0)
            weight3.append(0)
    return (weight1, weight2, weight3)

if __name__=='__main__':
    print("It's testing")
else:
    print("It's importing Algorithm")