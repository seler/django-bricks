

def inheritors(klass):
    """
    Returns all inheritors of `klass`.

    source: `http://stackoverflow.com/a/5883218/708764`
    """
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses
