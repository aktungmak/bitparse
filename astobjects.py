import pdb

class Structure(object):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    def parse(self, bitstream):
        print "im going to parse the %s structure!" % self.name
        parsed = [field.parse(bitstream) for field in self.fields]
        return (self.name, [item for sublist in parsed for item in sublist])
    def __str__(self):
        return "a %s structure with %d fields" % (self.name, len(self.fields))

class Field(object):
    def __init__(self, name, width, typ, value=0):
        self.type = typ
        self.width = width
        self.name = name
        self.value = value
    def parse(self, bitstream):
        print "im going to parse the %s field!" % self.name
        # lul everything is interpreted as a uint... so the type does nothing (yet)
        self.value = bitstream.read(int(self.width())).uint
        return [(self.name, self.value)]
    def __call__(self):
        return self.value
    def __str__(self):
        return "a %s field %d bits wide called %s" % (self.type, self.width(), self.name)

class Value(object):
    def __init__(self, value):
        self.value = value
    def __call__(self):
        return self.value

class IfBlock(object):
    def __init__(self, condition, fields):
        self.condition = condition
        self.fields = fields
    def parse(self, bitstream):
        if self.condition():
            # process all the fields
            parsed = [f.parse(bitstream) for f in self.fields]

            #flatten and return
            return [item for sublist in parsed for item in sublist]
        else:
            return []
    def __str__(self):
        return "an ifblock on %s with %d fields" % (self.condition, len(self.fields))

class ForLoop(object):
    def __init__(self, count, fields):
        self.count = count
        self.fields = fields
    def parse(self, bitstream):
        # process all the fields
        parsed = [f.parse(bitstream) for f in (self.fields * self.count())]

        #flatten and return
        return [item for sublist in parsed for item in sublist]
    def __str__(self):
        return "a forloop %d times with %d fields" % (self.count(), len(self.fields))
