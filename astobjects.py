class Structure(object):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    def __call__(self, bitstream):
        print "im going to parse the %s structure!" % self.name
        return (self.name, [field(bitstream) for field in self.fields])
    def __str__(self):
        return "a %s structure with %d fields" % (self.name, len(self.fields))

class Field(object):
    def __init__(self, name, width, typ, value=0):
        self.type = typ
        self.width = int(width)
        self.name = name
        self.value = value
    def __call__(self, bitstream):
        print "im going to parse the %s field!" % self.name
        # lul everything is interpreted as a uint... so the type does nothing (yet)
        self.value = bitstream.read(self.width).uint
        return (self.name, self.value)
    def __str__(self):
        return "a %s field %d bits wide called %s" % (self.type, self.width, self.name)

# class IfBlock(object):
#     def __init__(self, condition, fields):
#         self.scope = scope
#         self.condition = condition
#         self.fields = fields
#     def __call__(self, bitstream):
#         print "im going to check the if condition now!"
#         if self.condition:
#             return self.fields
#         else:
#             return []
#     def __str__(self):
#         return "an ifblock on %s with %d fields" % (self.condition, len(self.fields))
