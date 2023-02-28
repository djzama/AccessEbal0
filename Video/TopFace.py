import glob
import os
for i in range(1, 100):
    list_of_files = glob.glob(
        'D:\Python\AccessEbal0\Docker\db\DataSet\*')  # * means all if need specific format then *.csv
    # please don't hit me for this shitcode
    latest_file = max(list_of_files, key=os.path.getctime)
    flag = 0
    bufer = ''
    for i in latest_file:
        if i == '.':
            flag += 1
            if flag == 3:
                break
        if flag >= 2:
            bufer += i
    buferiter = bufer[1:]
    print(buferiter)
    print(latest_file)
