import json


def get_lists(path: str):
    data = parse_json(path)
    vehicles = parse_to_dict(data['vehicles'])
    jobs = parse_to_dict(data['jobs'])
    matrix = data['matrix']

    return vehicles, jobs, matrix

def parse_json(path: str):
    
    with open(path, 'r') as file:
        data = json.load(file)

    return data

def parse_to_dict(inner_list):
    parsed_data = {}
    for item in inner_list:
        for key, value in item.items():
            if key not in parsed_data:
                parsed_data[key] = []
            parsed_data[key].append(value)
    return parsed_data


def parse_routes(bestRoute, bestDurations, vehicles, jobs):

    routes = {}
    durationIndex = 0
    currentVehicle = bestRoute[0]
    jobs_route = []

    for i in range(1,len(bestRoute)-1):
        if bestRoute[i] in vehicles['start_index']:
            
            routes[str(currentVehicle)] = {
            "jobs": jobs_route,
            "delivery_duration": bestDurations[durationIndex]
            }
            jobs_route = []
            currentVehicle = bestRoute[i]
            durationIndex += 1
        else: 
            jid = get_id(jobs, 'location_index', bestRoute[i])
            jobs_route.append(jid)
            
    vid = get_id(vehicles, 'start_index', currentVehicle)
    routes[str(vid)] = {
            "jobs": jobs_route,
            "delivery_duration": bestDurations[durationIndex]
            }

    result = {'total_delivery_duration': sum(bestDurations), 'routes': routes}
    return result

def get_id(l, field,  elem):
    currentIndex = l[field].index(elem)
    return l['id'][currentIndex]