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

S = {"terms": ["dept", "course_num", "title"], 
    "dept": ["dept", "course_num", "title"], 
    "day": ["dept", "course_num", "section_num", "day", "time_start", "time_end"],
    "time_start": ["dept", "course_num", "section_num", "day", "time_start", "time_end"],
    "time_end": ["dept", "course_num", "section_num", "day", "time_start", "time_end"],
    "walking_time": ["dept", "course_num", "section_num", "day", "time_start", "time_end", "building_code", 
    "walking_time"],
    "building": ["dept", "course_num", "section_num", "day", "time_start", "time_end", "building_code", 
    "walking_time"],
    "enroll_lower": ["dept", "course_num", "section_num", "day", "time_start", "time_end", "enrollment"],
    "enroll_upper": ["dept", "course_num", "section_num", "day", "time_start", "time_end", "enrollment"]}

F = {"course_num": ["courses"], 
    "dept": ["courses"],
    "section_num": ["courses", "sections"],
    "day": ["courses", "sections", "meeting_patterns"],
    "time_start":["courses", "sections", "meeting_patterns"],
    "time_end": ["courses", "sections", "meeting_patterns"],
    "building_code": ["courses", "sections"],
    "enrollment": ["courses", "sections"],
    "title": ["courses"]}

O = {"sections": ["courses.course_id=section.section_id"],
    "meeting_patterns": ["courses.course_id=section.section_id", 
    "section.meeting_pattern_id=meeting_patterns.meeting_pattern_id"]}

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
    return rv

def terms(dictionary):
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

##temp, words = terms(example_1)
##print(temp)
##print(words)
"""
def select(dictionary, S):
    print(dictionary)
    output = []
    selects = []
    for i in dictionary:
        for j in S[i]:
            if j not in output:
                output.append(j)
    return ", ".join(output), output

def fr(output, F, O):
    from_ = []
    on_ = []
    for i in output:
        if i != "terms" and i != "walking_time":
            for j in F[i]:
                if j not in from_:
                    from_.append(j)
                if j == "sections" or j == "meeting_patterns":
                    for k in O[j]:
                        if k not in on_:
                            on_.append(k)
    return " JOIN ".join(from_), " AND ".join(on_)
"""
def fr2(output):
    from_ = []
    on_ = []
    if output != []:
        from_ += ["courses"]
    if ("section_num" or "building_code" or "enrollment" or "day" or "time_end" or "time_start") in output:
        from_ += ["sections"]
        on_ += ["courses.course_id=section.section_id"]
    if ("day" or "time_start" or "time_end") in output:
        from_ += ["meeting_patterns"]
        on_ += ["section.meeting_pattern_id=meeting_patterns.meeting_pattern_id"]
    return " AND ".join(from_), " ON ".join(on_)


print("method using if___in___")
print("")
output_list = get_variables(example_1)
output_string = ", ".join(output_list) 
print("SELECT", output_string)
from_string, on_string = fr2(output_list)
print("FROM", from_string)
print("ON", on_string)
"""
print("")
print("")
print("")
print("method using dictionary")
print("")
output_string, output_list = select(example_1, S)
print("SELECT", output_string)
from_string, on_string = fr(output_list, F, O)
print("FROM", from_string)
print("ON", on_string)
"""
