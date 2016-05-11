def generateSpecialValues():
    values = (
        # Special values in big endian
        # SPECIAL_VALUES will contains value in big endian and little endian
        "\x00",
        "\x00\x00",
        "\x01",
        "\x00\x01",
        "\x7f",
        "\x7f\xff",
        "\x7f\xff\xff\xff",
        "\x80",
        "\x80\x00",
        "\x80\x00\x00\x00",
        "\xfe",
        "\xfe\xff",
        "\xfe\xff\xff\xff",
        "\xff",
        "\xff\xff",
        "\xff\xff\xff\xff",
    )
    result = []
    for item in values:
        result.append(item)
        itemb = item[::-1]
        if item != itemb:
            result.append(itemb)
    return result

SPECIAL_VALUES = generateSpecialValues()

