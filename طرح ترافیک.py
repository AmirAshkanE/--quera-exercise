
is_running = True
startin_year = 1400
starting_month = 1
starting_day = 1

class User:
    def __init__(self, name):
        self.user_name = name
        self.car_list = []
        self.penalty_amount = 0
        self.balance_amount = 0       

def day_counter(date):
    weekdays = ["Sat", "Sun", "Mon", "Tues", "Wed", "Thurs", "Fri"]
    year, month, day = date.split("/")
    a = int(year) - startin_year
    b = int(month)+a*12-starting_month
    c = int(day)+b*30 - starting_day
    i = 0
    j = 0
    day = ""
    while j <= c:
        day = weekdays[i]
        i += 1
        if i == len(weekdays):
            i = 0
        j += 1
    return day

def day_checker(day):
    if day in ["Sat", "Mon", "Wed"]:
        return "even_day"
    elif day in ["Sun", "Tues", "Thurs"]:
        return "odd_day"
    else:
        return "friday"


def car_number_checker(car_number):
    if int(car_number) % 2 == 0:
        return "is_even"
    else:
        return "is_odd"

def license_expiry_calc(days,date):
    _date = []
    for d in date.split("/"):
        _date.append(int(d))
    _year,_month,_day = _date[0],_date[1],_date[2]
    _day += (days)

    if _day <= 30:
        expiry_date = f"{_year}/{_month:02}/{_day:02}"
        return expiry_date
    else:
        while _day > 30:
                _day -= 30
                _month += 1
                if _month > 12:
                    _month -= 12
                    _year += 1
        expiry_date = f"{_year}/{_month:02}/{_day:02}"
        return expiry_date


def expiry_checker(date1,date2):
    d1 = date1.replace("/","")
    d2 = date2.replace("/","")
    
    return int(d1) > int(d2)
    
    

def date_operator(date,num):
    _date = []
    for d in date.split("/"):
        _date.append(int(d))
    _year,_month,_day = _date[0],_date[1],_date[2]
    _day += num
    if _day > 30:
        _day -= 30
        _month +=1
    if _month > 12:
        _month -= 12
        _year += 1
    show_date = f"{_year}/{_month:02}/{_day:02}"
    return show_date

user_list = []
username_list = []
car_number_list = []
car_dict = {}
license_day_count = 1
expiry_dir = {}
hist_dir = {}

while is_running:
    command, *data = input().split()
        
    if command == "REGISTER":   
        for user in user_list:
            if data[0] == user.user_name:
                print("INVALID USERNAME")
                break
        else:
            print("REGISTER DONE")
            user_list.append(User(data[0]))
            for user in user_list:
                    if user.user_name not in username_list:
                        username_list.append(user.user_name)
    
    elif command == "REGISTER_CAR":
        for user in user_list:
            car_dict.update({user.user_name: user.car_list})
            
        if data[0] not in username_list:
            print("INVALID USERNAME")
        elif data[1] in car_number_list or len(data[1]) != 10:
            print("INVALID CAR PLATE")
        else:
            for user in user_list:
                if user.user_name == data[0]:
                    user.car_list.append(data[1])
                    car_number_list.append(data[1])
                    print("REGISTER CAR DONE")
                    break
                

    elif command == "NEW_RECORD":
        if data[0] not in car_number_list:
            print("INVALID CAR PLATE")
        else:
            day = day_checker(day_counter(data[1]))
            number = car_number_checker(data[0])
            has_license = False
            
            if data[0] in expiry_dir.keys():
                has_license = False if expiry_checker(data[1], expiry_dir.get(data[0])) else True
            if data[0] in hist_dir.keys():
                if data[1] == hist_dir.get(data[0]):
                    has_license = False
                     
            
            if day == "friday":
                print("NORMAL RECORDED")
            elif (number == "is_even" and day == "even_day" ):
                print("NORMAL RECORDED")
            elif (number == "is_odd" and day == "odd_day"):
                print("NORMAL RECORDED")
            elif has_license:
                print("NORMAL RECORDED")
            else:
                for user in user_list:
                    if data[0] in user.car_list:
                        print("PENALTY RECORDED")
                        user.penalty_amount += 100
                        

    elif command == "BUY_LICENSE":
        
        if data[0] not in username_list:
                print("INVALID USERNAME")
        elif data[1] not in car_number_list:
            print("INVALID CAR PLATE")
        else:  
            for user in user_list:
                if user.user_name != data[0]:
                    continue
                elif data[1] not in user.car_list:
                    print("INVALID CAR PLATE")
                    break
                elif user.balance_amount < 70:
                    print("NO ENOUGH MONEY")
                    break
                elif user.balance_amount < int(data[2])*70:
                        print("NO ENOUGH MONEY")
                        break
                else:
                    user.balance_amount -= (int(data[2])*70)
                    expiry_dir.update({data[1] : license_expiry_calc(int(data [2]), data[3])})
                    hist_dir.update({data[1]: data[3]})
                    print("BUY LICENSE DONE")
                    break
                
    elif command == "ADD_BALANCE":
        if data[0] not in username_list:
            print("INVALID USERNAME")
        else:
            for user in user_list:
                if data[0] == user.user_name:
                    user.balance_amount += int(data[1])
                    print("ADD BALANCE DONE")
                    break
    elif command == "GET_BALANCE":
        if data[0] not in username_list:
            print("INVALID USERNAME")
        else:
            for user in user_list:
                if data[0] == user.user_name:
                    print(user.balance_amount)
                    break
    elif command == "GET_PENALTY":
        if data[0] not in username_list:
            print("INVALID USERNAME")
        else:
            for user in user_list:
                if data[0] == user.user_name:
                    print(user.penalty_amount)
                    break
    elif command == "GET_LICENSE_DEADLINE":
        if data[0] not in car_number_list:
            print("INVALID CAR PLATE")
        else:
            if hist_dir != {}:
                if not expiry_checker(data[1], hist_dir.get(data[0])):
                    print(date_operator(data[1], 1))
                else:
                    temp_date = expiry_dir.get(data[0]) if data[0] in expiry_dir.keys() else "1400/01/01"
                    has_expired = expiry_checker(data[1], temp_date)
                    if has_expired:
                        print(date_operator(data[1], 1))
                    else:
                        print(temp_date)
            else:
                temp_date = expiry_dir.get(data[0]) if data[0] in expiry_dir.keys() else "1400/01/01"
                has_expired = expiry_checker(data[1], temp_date)
                if has_expired:
                    print(date_operator(data[1], 1))
                else:
                    print(temp_date)
            

    elif command.upper() == "END":
        is_running = False
