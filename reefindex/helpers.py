def prettify(s):
    return s.replace('_', ' ').capitalize()


def abbreviate_latin(s):
    prefix, suffix = s.split()
    return "%s. %s" % (prefix[0].upper(), suffix)
