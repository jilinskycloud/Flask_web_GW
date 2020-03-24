def s32(value):
    return -(value & 0x80000000) | (value & 0x7fffffff)


a = "ce"
print(s32(a))

