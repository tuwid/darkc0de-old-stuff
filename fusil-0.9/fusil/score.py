from fusil.tools import minmax

def scoreLogFunc(object, score):
    if score in (None, 0):
        return object.info
    elif 0.50 <= abs(score):
        return object.error
    else:
        return object.warning

def normalizeScore(score):
    score = minmax(-1.0, score, 1.0)
    return round(score, 2)

