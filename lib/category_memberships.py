import yaml
import collections


Assignment = collections.namedtuple("Assignment", ["reqs", "group", "subgroup"])


def load_assignments():
    data = _load_raw_data()
    assignments = []
    for group, subgroups in data.items():
        for subgroup, elems in subgroups.items():
            for elem in elems:
                assignment = Assignment(elem, group, subgroup)
                assignments.append(assignment)
    return assignments


def _load_raw_data():
    fp = "./data/category_memberships.yaml"
    with open(fp, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
