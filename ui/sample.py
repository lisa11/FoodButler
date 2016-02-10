example_1 = {"building":"RY",
             "walking_time": 10,
             "dept":"CMSC",
             "day":["MWF", "TR"],
             "time_start":1030,
             "time_end":1500,
             "enroll_lower":20,
             "terms":"computer science"}

example_0 = {"time_start":930,
             "time_end":1500,
             "day":["MWF"]}

def get_terms(dictionary):
    temp = ""
    count = 0
    words = []
    if "terms" in dictionary:
        temp1 = "(SELECT course_id, count(course_id) as count FROM catalog_index WHERE"                
        temp2 = " GROUP BY course_id HAVING count={}"
        words = dictionary["terms"].split()
        for i in words:
            temp1 += " word=? "
            temp1 += "or"
            count += 1
        temp = temp1[0:-3] + temp2.format(count) + ")"
    return temp, words


def get_variables(args_from_ui):
    '''
    Return a list of required output variables given arguments from ui
    '''
    rv = []
    if args_from_ui != {}:
        rv += ["dept", "course_num"]
    if ("day" or "time_start" or "time_end" or "walking_time" or "building" or "enroll_lower" or "enroll_upper") in args_from_ui:
        rv += ["section_num", "day", "time_start", "time_end"]
    if ("walking_time" or "building") in args_from_ui:
        rv += ["building_code", "walking_time"]
    if ("enroll_lower" or "enroll_upper") in args_from_ui:
        rv += ["enrollment"]
    if ("terms" or "dept") in args_from_ui:
        rv += ["title"]
    return rv, ", ".join(rv)

def get_path(variables):
    tables = []
    join_conditions = []
    if variables != []:
        tables += ["courses"]
    if ("section_num" or "building_code" or "enrollment" or "day" or "time_end" or "time_start") in variables:
        tables+= ["sections"]
        join_conditions += ["courses.course_id=section.section_id"]
    if ("day" or "time_start" or "time_end") in variables:
        tables += ["meeting_patterns"]
        join_conditions += ["section.meeting_pattern_id=meeting_patterns.meeting_pattern_id"]
    return " AND ".join(tables), " ON ".join(join_conditions)


temp, words = get_terms(example_1)
print(temp)
print(words)


print("")
var, var_string = get_variables(example_1) 
print("SELECT", var_string)
from_string, on_string = get_path(var)
print("FROM", from_string)
print("ON", on_string)




'''
SELECT dept, course_num, title
FROM courses as c JOIN 
    sections as s JOIN 
    meeting_patterns as mp JOIN
        (SELECT course_id, count(course_id) as count
        FROM catalog_index
        WHERE word="abstraction" or word="programming"
        GROUP BY course_id
        HAVING count=2) as TEMP
ON c.course_id=s.course_id and 
    s.meeting_pattern_id=mp.meeting_pattern_id 
    and TEMP.course_id=c.course_id
WHERE day="MWF" and time_start=930
'''