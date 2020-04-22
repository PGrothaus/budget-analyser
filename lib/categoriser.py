from lib.category_memberships import load_assignments


def categorise_transactions(transactions):
    assignments = load_assignments()
    return [categorise_transaction(trans, assignments) for trans in transactions]


def categorise_transaction(transaction, assignments):
    group, subgroup = _match_assignment(transaction, assignments)
    return (transaction, group, subgroup)


def _match_assignment(transaction, assignments):
    for assignment in assignments:
        if _match_assignment_deep(transaction, assignment):
            return assignment.group, assignment.subgroup
    _log_unassigned_transaction(transaction)
    return None, None


def _match_assignment_deep(transaction, assignment):
    reqs = assignment.reqs
    for key, val in reqs.items():
        if key == "threshold":
            if not _eval_threshold_condition(reqs, key, transaction):
                return False
        elif getattr(transaction, key) != val:
            return False
        else:
            pass
    return True


def _eval_threshold_condition(elems, key, transaction):
    prop, comp, val = elems[key].split(",")
    val_trans = getattr(transaction, prop)
    cond = "{} {} {}".format(val_trans, comp, val)
    return eval(cond)


def _log_unassigned_transaction(transaction):
    print("INFO: Unassigned Transaction - {}: {}".format(
        transaction.descripcion, transaction.monto))
