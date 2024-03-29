def read_file(filename):
    """ Read file with filename
        Read one line of station code and station name
        At the end, each row in table contains 2 strings (code and name).
        Number of rows in table = number of stations

    :param filename: str
    :return: nested list of str
    """
    lines = open(filename).read().splitlines()
    table = [x.split(",") for x in lines if x != ""]
    return table


def create_station_names(table):
    """ ##The built-in dict() creates a dict from an existing object such as a list or a tuple.
    Receive nested list of station code and station name
            Convert to dictionary where station code is key, station name is value
            Return this dictionary

        :param table: nested list of str
        :return: dictionary
        >>> create_station_names([['E3', 'Nana'], ['E4','Asok'], ['E5', 'Phrom Phong']])
        {'E3': 'Nana', 'E4': 'Asok', 'E5': 'Phrom Phong'}
        >>> create_station_names([['N20','Saphan Mai'], ['N19','Sai Yud']])
        {'N20': 'Saphan Mai', 'N19': 'Sai Yud'}
        >>> create_station_names([[]])
        {}
        """
    _dict = {}
    if table == [[]]:
        return _dict
    else:
        return dict(table)


def extract_station_code(station_code):
    """ #return string and integer.If station_code = CEN return N and 0.
    Receive station code
            Return station line and station index
            For station code CEN.

        :param station_code: str
        :return: int and str
        >>> extract_station_code('N13')
        ('N', 13)
        >>> extract_station_code('E9')
        ('E', 9)
        >>> extract_station_code('CEN')
        ('N', 0)
        """
    if station_code != "CEN":
        return station_code[0], int(station_code[1:])
    else:
        return 'N', 0


def count_num_stations(base_stations, curr_station):
    """  ##This function find distance between base station and curr station.
    Receive a list of base stations and current station code
            Find number of stations between current station and each base station.
            Note that base_stations in this problem is fixed, unlike doctest cases.

            Return dictionary where key is station code,
                              value is number of stations between key station and current station code
            Example: number of stations between N2-N2 = 0
                     number of stations between N1-N2 = 1

        :param base_stations: a list of str
        :param curr_station: str
        :return: dictionary
        >>> count_num_stations(['N1', 'N2', 'N3', 'N4'], 'N2')
        {'N1': 1, 'N2': 0, 'N3': 1, 'N4': 2}
        >>> count_num_stations(['E9', 'E8', 'E7', 'E6', 'E5'], 'E7')
        {'E9': 2, 'E8': 1, 'E7': 0, 'E6': 1, 'E5': 2}
        >>> count_num_stations(['N2', 'N1', 'CEN', 'E1', 'E2', 'E3'], 'E1')
        {'N2': 3, 'N1': 2, 'CEN': 1, 'E1': 0, 'E2': 1, 'E3': 2}
        """
    dict_ = {}
    if curr_station == "CEN":
        c_stationcode, c_distance = extract_station_code(curr_station)
        for i in range(len(base_stations)):
            b_stationcode, b_distance = extract_station_code(base_stations[i])
            dict_.update({base_stations[i]: b_distance})
        dict_.update({'CEN': c_distance})
    else:
        for station_code in base_stations:
            if station_code != "CEN":
                if station_code[0] == curr_station[0]:
                    distance = abs(int(station_code[1:]) - int(curr_station[1:]))
                    dict_.update({station_code: distance})
                else:
                    distance = abs(int(station_code[1:]) + int(curr_station[1:]))
                    dict_.update({station_code: distance})
            else:
                distance = int(curr_station[1:])
                dict_.update({station_code: distance})
    return dict_


def get_num_station_grid(base_stations):
    """ ##find the distance to each station.
    Receive a list of base stations
            Create a nested dictionary grid such that
                grid[X][Y] = number of stations between stations X and Y
                X and Y are stations inside base_stations.
            Example: grid['N8']['N1'] = 7
                     grid['N8']['CEN'] = 8
                     grid['N8']['E2'] = 10

        :param base_stations: a list of str :return: nested dictionary >>> get_num_station_grid(['N2', 'N3']) {'N2':
        {'N2': 0, 'N3': 1}, 'N3': {'N2': 1, 'N3': 0}} >>> get_num_station_grid(['E9', 'E8', 'E7']) {'E9': {'E9': 0,
        'E8': 1, 'E7': 2}, 'E8': {'E9': 1, 'E8': 0, 'E7': 1}, 'E7': {'E9': 2, 'E8': 1, 'E7': 0}} >>>
        get_num_station_grid(['N2', 'N1', 'CEN', 'E1']) {'N2': {'N2': 0, 'N1': 1, 'CEN': 2, 'E1': 3}, 'N1': {'N2': 1,
        'N1': 0, 'CEN': 1, 'E1': 2}, 'CEN': {'N2': 2, 'N1': 1, 'CEN': 0, 'E1': 1}, 'E1': {'N2': 3, 'N1': 2, 'CEN': 1,
        'E1': 0}}
    """
    _dict = {}
    for i in range(len(base_stations)):
        _dict.update({base_stations[i]: count_num_stations(base_stations, base_stations[i])})
    return _dict


def read_station(base_stations, extension_stations, text):
    """ ##If your input not in base_stations and extension_stations its will print does not exist
    Read station code from user
            The station code must be one of base stations or extension staitons.
            If the station is not one of base stations or extension staitons, continue reading.
            Note that text is a string that can be either 'origin' or 'destination'
            Return the valid station code.

        :param base_stations: a list of str
        :param extention_stations: a list of str
        :param text: str
        :return: str
        """
    if text in base_stations:
        return text
    elif text in extension_stations:
        return text
    else:
        print(f"Station {text} does not exist. Enter a station between N24-E9.")


def get_base_fee(num_station_grid, origin, dest):
    """ ##Find fee in base station.
    Compute fee inside the base station zone, given origin and destination station code
            Return the fee
        :param num_station_grid: nested dictionary
        :param origin: str
        :param dest: str
        :return: int
        >>> get_base_fee({'E9': {'E9': 0, 'E8': 1, 'E7': 2}, 'E8': {'E9': 1, 'E8': 0, 'E7': 1}, 'E7': {'E9': 2, 'E8': 1, 'E7': 0}}, 'E9', 'E8')
        16
        >>> get_base_fee({'E9': {'E9': 0, 'E8': 1, 'E7': 2}, 'E8': {'E9': 1, 'E8': 0, 'E7': 1}, 'E7': {'E9': 2, 'E8': 1, 'E7': 0}}, 'E9', 'E7')
        23
        >>> get_base_fee({'N2': {'N2': 0, 'N1': 1, 'CEN': 2, 'E1': 3}, 'N1': {'N2': 1, 'N1': 0, 'CEN': 1, 'E1': 2}, 'CEN': {'N2': 2, 'N1': 1, 'CEN': 0, 'E1': 1}, 'E1': {'N2': 3, 'N1': 2, 'CEN': 1, 'E1': 0}}, 'N2', 'E1')
        26
        """
    x = num_station_grid.get(origin)
    i = x.get(dest)
    if i == 1 or i == 0:
        return 16
    elif i == 2:
        return 23
    elif i == 3:
        return 26
    elif i == 4:
        return 30
    elif i == 5:
        return 33
    elif i == 6:
        return 37
    elif i == 7:
        return 40
    else:
        return 44


def get_extension_fee(origin, dest):
    """ ##Find fee in extension station.
    Compute fee inside the extension station zone, given origin and destination station code
            Return the fee

        :param origin: str
        :param dest: str
        :return: int
        >>> get_extension_fee('N9', 'N13')
        27
        >>> get_extension_fee('N20', 'N12')
        39
        >>> get_extension_fee('N10', 'N10')
        15
        """
    ori = extract_station_code(origin)
    des = extract_station_code(dest)
    return 15 + (3 * abs(ori[1] - des[1]))


def compute_fee(num_station_grid, base_stations, extension_stations, origin, dest):
    """ ##This function can find distance between base station and extension station
    Compute and return BTS fee from origin station code to destination station code

        :param num_station_grid: nested dictionary
        :param base_stations: a list of str
        :param extention_stations: a list of str
        :param origin: str
        :param destination: str
        :return: int
        """
    if origin in extension_stations and dest in base_stations:
        base_dest = get_base_fee(num_station_grid, dest, 'N8')
        exten_origin = get_extension_fee('N9', origin)
        return base_dest + exten_origin - 15
    elif origin in base_stations and dest in extension_stations:
        base_origin = get_base_fee(num_station_grid, origin, 'N8')
        exten_dest = get_extension_fee('N9', dest)
        return base_origin + exten_dest - 15
    elif origin and dest in base_stations:
        return get_base_fee(num_station_grid, origin, dest)
    else:
        return get_extension_fee(origin, dest)


# Main part

# Create and print a list of base stations N8-E9
base_stations = []
for i in range(8, 0, -1):
    base_stations.append('N' + str(i))
base_stations.append('CEN')
for i in range(1, 10):
    base_stations.append('E' + str(i))
# print(base_stations)  # Uncomment this to see what base_stations looks like

# Create and print a list of extension stations N24-N9
extension_stations = []
for i in range(24, 8, -1):
    extension_stations.append('N' + str(i))
# print(extension_stations)  # Uncomment this to see what extension_stations looks like

filename = 'bts_station_list.txt'
table = read_file(filename)
# print(table)           # Uncomment this to see what table looks like
station_names = create_station_names(table)
# print(station_names)  # Uncomment this to see what station_names looks like

num_station_grid = get_num_station_grid(base_stations)
# print(num_station_grid)  # Uncomment to see what num_station_grid looks like

# Fill your code for Main here
list_ticket = []
list_price = []
print(f"Ticket1")
origin = str(input("Enter origin station (N24-E9): "))
while origin != read_station(base_stations, extension_stations, origin):
    origin = str(input("Enter origin station (N24-E9): "))
dest = str(input("Enter destination station (N24-E9): "))
while dest != read_station(base_stations, extension_stations, dest):
    dest = str(input("Enter destination station (N24-E9): "))
if origin in extension_stations and dest in base_stations:
    print(f"Base Station Zone: Fee = {get_base_fee(num_station_grid, dest, 'N8')} Baht")
    print(f"Extension Station Zone: Fee = {get_extension_fee('N9', origin)} Baht")
    print(f"Origin = {origin} = {station_names.get(origin)}, Destination = {dest} = {station_names.get(dest)}: "
          f"Fee = {compute_fee(num_station_grid, base_stations, extension_stations, origin, dest)}")
    print()
    list_price.append(compute_fee(num_station_grid, base_stations, extension_stations, origin, dest))
elif origin in base_stations and dest in extension_stations:
    print(f"Base Station Zone: Fee = {get_base_fee(num_station_grid, origin, 'N8')} Baht")
    print(f"Extension Station Zone: Fee = {get_extension_fee('N9', dest)} Baht")
    print(f"Origin = {origin} = {station_names.get(origin)}, Destination = {dest} = {station_names.get(dest)}: "
          f"Fee = {compute_fee(num_station_grid, base_stations, extension_stations, origin, dest)}")
    list_price.append(compute_fee(num_station_grid, base_stations, extension_stations, origin, dest))
    print()
elif origin and dest in base_stations:
    print(f"Base Station Zone: Fee = {get_base_fee(num_station_grid, origin, dest)} Baht")
    print(f"Origin = {origin} = {station_names.get(origin)}, Destination = {dest} = {station_names.get(dest)}: "
          f"Fee = {compute_fee(num_station_grid, base_stations, extension_stations, origin, dest)}")
    list_price.append(compute_fee(num_station_grid, base_stations, extension_stations, origin, dest))
    print()
else:
    print(f"Extension Station Zone: Fee = {get_extension_fee(origin, dest)} Baht")
    print(f"Origin = {origin} = {station_names.get(origin)}, Destination = {dest} = {station_names.get(dest)}: "
          f"Fee = {compute_fee(num_station_grid, base_stations, extension_stations, origin, dest)}")
    list_price.append(compute_fee(num_station_grid, base_stations, extension_stations, origin, dest))
    print()

con = str(input("Do you want to continue (Y/N)? "))
i = 2
while con != "N":
    print()
    print(f"Ticket{i}")
    i = i + 1
    list_ticket.append(i)
    origin = str(input("Enter origin station (N24-E9): "))
    while origin != read_station(base_stations, extension_stations, origin):
        origin = str(input("Enter origin station (N24-E9): "))
    dest = str(input("Enter destination station (N24-E9): "))
    while dest != read_station(base_stations, extension_stations, dest):
        dest = str(input("Enter destination station (N24-E9): "))
    if origin in extension_stations and dest in base_stations:
        print(f"Base Station Zone: Fee = {get_base_fee(num_station_grid, dest, 'N8')} Baht")
        print(f"Extension Station Zone: Fee = {get_extension_fee('N9', origin)} Baht")
        print(f"Origin = {origin} = {station_names.get(origin)}, Destination = {dest} = {station_names.get(dest)}: "
              f"Fee = {compute_fee(num_station_grid, base_stations, extension_stations, origin, dest)}")
        print()
        list_price.append(compute_fee(num_station_grid, base_stations, extension_stations, origin, dest))
    elif origin in base_stations and dest in extension_stations:
        print(f"Base Station Zone: Fee = {get_base_fee(num_station_grid, origin, 'N8')} Baht")
        print(f"Extension Station Zone: Fee = {get_extension_fee('N9', dest)} Baht")
        print(f"Origin = {origin} = {station_names.get(origin)}, Destination = {dest} = {station_names.get(dest)}: "
              f"Fee = {compute_fee(num_station_grid, base_stations, extension_stations, origin, dest)}")
        print()
        list_price.append(compute_fee(num_station_grid, base_stations, extension_stations, origin, dest))
    elif origin and dest in base_stations:
        print(f"Base Station Zone: Fee = {get_base_fee(num_station_grid, origin, dest)} Baht")
        print(f"Origin = {origin} = {station_names.get(origin)}, Destination = {dest} = {station_names.get(dest)}: "
              f"Fee = {compute_fee(num_station_grid, base_stations, extension_stations, origin, dest)}")
        print()
        list_price.append(compute_fee(num_station_grid, base_stations, extension_stations, origin, dest))
    else:
        print(f"Extension Station Zone: Fee = {get_extension_fee(origin, dest)} Baht")
        print(f"Origin = {origin} = {station_names.get(origin)}, Destination = {dest} = {station_names.get(dest)}: "
              f"Fee = {compute_fee(num_station_grid, base_stations, extension_stations, origin, dest)}")
        print()
        list_price.append(compute_fee(num_station_grid, base_stations, extension_stations, origin, dest))

    con = str(input("Do you want to continue (Y/N)? "))
    print()

print(f"{len(list_ticket) + 1} tickets are sold.")
print(f"{sum(list_price)} Baht is collected.")

if __name__ == "__main__":
    import doctest

    doctest.testmod()
