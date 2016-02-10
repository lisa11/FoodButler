### CS122 W16: Course search engine: search
###
### Lisa Li
### Gary Song

from math import radians, cos, sin, asin, sqrt
import sqlite3
import json
import re
import os


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'course-info.db')


def get_terms(args_from_ui):
    """
    If term(s) is included in the search criteria, forms a string that will create a 
    temporary table in the query containing results that have the specified term(s).

    Inputs: 
        args_from_ui: dictionary containing search criteria

    Outputs:
        temp: a string that creates the temporary table
        terms: list of terms that will be passed on as arguments into the query
    """
    temp = ""
    word = [" word=? "]
    if "terms" in args_from_ui:
        temp1 = " JOIN (SELECT course_id, count(course_id) as count FROM catalog_index WHERE"                
        temp2 = "GROUP BY course_id HAVING count={})"
        terms = args_from_ui["terms"].split()
        temp = temp1 + "OR".join(word*len(terms)) + temp2.format(len(terms))
    return temp, terms


def get_variables(args_from_ui):
    '''
    Return a list of required output variables given arguments from ui

    Inputs: 
        args_from_ui: dictionary containing search criteria

    Outputs: 
        rv: list of required output variables
        string: a string that allows the query to select the required output
    '''
    rv = []
    if args_from_ui != {}:
        rv += ["dept", "course_num"]
    if "day" in args_from_ui or "time_start"  in args_from_ui or "time_end"  in args_from_ui or "walking_time"  in args_from_ui or "building"  in args_from_ui or "enroll_lower"  in args_from_ui or "enroll_upper" in args_from_ui:
        rv += ["section_num", "day", "time_start", "time_end"]
    if "walking_time" in args_from_ui or "building" in args_from_ui:
        rv += ["sections.building_code"]
    if "enroll_lower" in args_from_ui or "enroll_upper" in args_from_ui:
        rv += ["enrollment"]
    if "terms" in args_from_ui or "dept" in args_from_ui:
        rv += ["title"]
    string = "SELECT " + ", ".join(rv)
    return rv, string


def get_path(variables, args_from_ui):
    """
    Given list of required output variables, creates strings that allows 
    query to look at specific tables and join those tables together

    Inputs: 
        variables: list of required output variables

    Outputs: 
        from_string: a string that allows the query to select specific tables
        on_string: a string that allows the query to join specified tables
    """
    tables = []
    join_conditions = []
    if variables != []:
        tables += ["courses"]
    if "section_num" in variables or "enrollment" in variables or "day" in variables or "time_end" in variables or "time_start" in variables:
        tables += ["sections"]
        join_conditions += ["courses.course_id=sections.course_id"]
    if "day" in variables or "time_start" in variables or "time_end" in variables:
        tables += ["meeting_patterns"]
        join_conditions += ["sections.meeting_pattern_id=meeting_patterns.meeting_pattern_id"]

    from_string = "FROM " + " JOIN ".join(tables)
    if join_conditions != [] or "terms" in args_from_ui:
        on_string = "ON " + " AND ".join(join_conditions)
    else:
        on_string = ""

    return from_string, on_string
    

def find_eligible_buildings(args_from_ui):
    '''
    Given args_from_ui, return the command for creating the TEMP2 table for
    building and a list containing the building name and maximum walking_time
    requested.
    '''

    temp = ""
    arg_list = []
    if "building" in args_from_ui:
        arg_list = [args_from_ui["building"], args_from_ui["walking_time"]]
        temp = " JOIN (SELECT a.building_code, compute_time_between(a.lon, a.lat, b.lon, b.lat) as walking_time FROM gps as a JOIN (SELECT lon, lat, building_code FROM gps WHERE building_code = ?) as b WHERE walking_time <= ?)" 
    return temp, arg_list


def write_where_string_and_args(args_from_ui):
    '''
    Write the where string in SQL and the args list needed for cursor execute
    for all variables except terms and building/walking_time, which are dealt
    with separately in write_sql_code function.
    '''

    where_string_list = []
    args = []
    if "dept" in args_from_ui:
        args.append(args_from_ui["dept"])
        where_string_list.append(" dept = ?")
    if "day" in args_from_ui:
        s_list = []
        for day in args_from_ui["day"]:
            args.append(day)
            s_list.append(" day = ?")
        where_string_list.append(" (" + " OR".join(s_list) + ")")
    if "time_start" in args_from_ui:
        args.append(args_from_ui["time_start"])
        where_string_list.append(" time_start >= ?")
    if "time_end" in args_from_ui:
        args.append(args_from_ui["time_end"])
        where_string_list.append(" time_end <= ?")
    if "enroll_lower" in args_from_ui:
        args.append(args_from_ui["enroll_lower"])
        where_string_list.append(" enrollment >= ?")
    if "enroll_upper" in args_from_ui:
        args.append(args_from_ui["enroll_upper"])
        where_string_list.append(" enrollment <= ?")
    if where_string_list != []:
        where_string = "WHERE" + " AND".join(where_string_list)
    else: 
        where_string = ""
    return where_string, args


def write_sql_code(args_from_ui):
    '''
    Preparing code for cursor execute given arguments from ui
    '''
    args = []
    select_list, select_string = get_variables(args_from_ui)
    from_string, on_string = get_path(select_list, args_from_ui)
    if "terms" in args_from_ui:
        temp_table, keywords = get_terms(args_from_ui)
        from_string = from_string + temp_table + " as TEMP"
        if on_string == "":
            on_string += "ON "
        else:
            on_string += " AND "
        on_string += "TEMP.course_id=courses.course_id"
        args += keywords
    if "building" in args_from_ui:
        temp_table2, arg_list = find_eligible_buildings(args_from_ui)
        from_string = from_string + temp_table2 + " as TEMP2"
        if on_string == "":
            on_string += "ON "
        else:
            on_string += " AND "
        on_string += "TEMP2.building_code=sections.building_code"
        args += arg_list
    where_string, arg = write_where_string_and_args(args_from_ui)
    args += arg
    
    return select_string+" "+from_string+" "+on_string+" "+where_string+" ORDER BY dept, course_num", args


def find_courses(args_from_ui):
    '''
    Takes a dictionary containing search criteria and returns courses
    that match the criteria.  The dictionary will contain some of the
    following fields:

      - dept a string
      - day is array with variable number of elements  
           -> ["'MWF'", "'TR'", etc.]
      - time_start is an integer in the range 0-2359
      - time_end is an integer an integer in the range 0-2359
      - enroll is an integer
      - walking_time is an integer
      - building ia string
      - terms is a string: "quantum plato"]

    Returns a pair: list of attribute names in order and a list
    containing query results.
    '''

    if args_from_ui == {}:
        return ([], [])
        
    db = sqlite3.connect(DATABASE_FILENAME)
    if ("walking_time" or "building") in args_from_ui:
        db.create_function("compute_time_between", 4, compute_time_between)
    c = db.cursor()
    s, args = write_sql_code(args_from_ui)
    r = c.execute(s, args)
    header = get_header(c)
    result = []
    for entry in r.fetchall():
        result.append(list(entry))
    db.close()

    return header, result
        

########### auxiliary functions #################
########### do not change this code #############

def compute_time_between(lon1, lat1, lon2, lat2):
    '''
    Converts the output of the haversine formula to walking time in minutes
    '''
    meters = haversine(lon1, lat1, lon2, lat2)

    #adjusted downwards to account for manhattan distance
    walk_speed_m_per_sec = 1.1 
    mins = meters / (walk_speed_m_per_sec * 60)

    return mins


def haversine(lon1, lat1, lon2, lat2):
    '''
    Calculate the circle distance between two points 
    on the earth (specified in decimal degrees)
    '''
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    m = km * 1000
    return m 



def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i in range(len(s)):
        if s[i] == ".":
            s = s[i+1:]
            break

    return s



########### some sample inputs #################

example_0 = {"time_start":930,
             "time_end":1500,
             "day":["MWF"]}

example_1 = {"building":"RY",
             "walking_time": 10,
             "dept":"CMSC",
             "day":["MWF", "TR"],
             "time_start":1030,
             "time_end":1500,
             "enroll_lower":20,
             "terms":"computer science"}

