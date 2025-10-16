import time
am_pm = time.strftime('%p')
local_time = time.localtime()
curr_time = time.strftime ('%I : %M : %S %p')
print(local_time)

if am_pm == 'AM':
    print("It's morning : ",curr_time)

else :
    print("It's evening : ",curr_time)    