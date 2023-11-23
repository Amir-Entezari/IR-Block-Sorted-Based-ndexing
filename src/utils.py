def dec_to_bin(dec_num: int):
    """
    This function converts a decimal number to binary number
    """
    binary_string = bin(dec_num)[2:]
    return binary_string


def bin_to_dec(binary_string: str):
    """
    This function converts a binary number to decimal number
    """
    if not all(bit in '01' for bit in binary_string):
        raise ValueError("Input must be a binary string")

    decimal_number = int(binary_string, 2)
    return decimal_number


def dec_to_gamma(dec_num: int):
    """
    This function convert a decimal number to gamma code.
    :param dec_num: int
        The number you want to encode
    :return:
        return Gamma code of the number
    """
    bin_num = dec_to_bin(dec_num)
    n = len(bin_num)
    unary = (n) * '1'
    binary = bin_num[1:]
    gamma_code = unary + '0' + binary
    return gamma_code


def list_to_gamma_code(ls):
    """
    This function convert list of differences of numbers to gamma code using dec_to_gamma() function.
    :param ls:
        The list you want to encode
    :return:
        Gamma code of the list
    """
    curr_diff = ls[0]
    result = dec_to_gamma(curr_diff)
    for i in range(1, len(ls)):
        curr_diff = ls[i] - ls[i - 1]
        result += dec_to_gamma(curr_diff)
    return result


def gamma_code_to_list(gamma_code_list):
    """
    This function decoded a gamma code of a list. In this function, we simply loop over the gamma code, and count 1s until
    reaching a 0. Then, we decode the substring of the gamma code such that the beginning of the string is the index that
    we reach when counting 1s, here it's i, and the end of the substring which is i+counted 1s.
    :param gamma_code_list:
        The gamma code of a list
    :return:
        Return the decoded list
    """
    result = []
    i = 0
    while i < len(gamma_code_list):
        j = 0
        while gamma_code_list[i] == '1':
            j += 1
            i += 1
        dec_num = bin_to_dec('1' + gamma_code_list[i + 1: i + j])
        result.append(dec_num)
        i += j
    for i in range(1, len(result)):
        result[i] = result[i - 1] + result[i]
    return result
