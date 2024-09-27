from PIL import Image
import os
import random

# generate a number based on seed input
def random_num_gen(seed_value, max_num):
    random.seed(seed_value)
    random_number = random.randint(0, max_num)
    return random_number

def encrypt(bits, key, file, message, name):
    bits = 8 if bits == "8-bit" else 7

    message_binary = ""  # variable to hold binary

    # convert message to binary
    for x in range(len(message)):
        if bits == 7:
            bin_number = bin(ord(message[x]))[2:]  # convert character to binary number

            # check if it needs padding for encoding
            if len(bin_number) == 6:
                bin_number = f"0{bin_number}"

            message_binary += bin_number  # append the binary string to the message
        elif bits == 8:
            bin_number = bin(ord(message[x]))[2:]  # convert character to binary number

            # check if it needs padding for encoding
            if len(bin_number) == 6:
                bin_number = f"00{bin_number}"
            elif len(bin_number) == 7:
                bin_number = f"0{bin_number}"

            message_binary += bin_number  # append the binary string to the message

    # open image
    image = Image.open(file)

    # set dimensions and load pixels
    width, height = image.size
    pixels = image.load()

    # count how far we are in message
    message_counter = 0

    position_list = []  # initialize list to hold pixel coordinates
    position_tracker = {(-1, -1): 3}  # initialize dictionary to track number of times coordinate is used
    sequence_counter = 0  # hold sequence number to ensure new numbers are generated
    num_of_coords = len(message_binary)  # specify number of pixel coordinates needed
    # set max numbers for each coordinate plane
    max_num_x = width - 1
    max_num_y = height - 1

    # generate pixel coordinates
    for coord in range(num_of_coords):
        temp_coords = (-1, -1)

        # while loop serves to regenerate coords if they appear 3 times
        while position_tracker[temp_coords] >= 3:
            random_x = random_num_gen(f"{key}{sequence_counter}", max_num_x)
            sequence_counter += 1
            random_y = random_num_gen(f"{key}{sequence_counter}", max_num_y)
            sequence_counter += 1
            temp_coords = (random_x, random_y)

            # check if coordinates are in position tracker, if not then add them, if they are then increment the count
            if temp_coords not in position_tracker:
                position_tracker[temp_coords] = 0
            else:
                position_tracker[temp_coords] += 1

        position_list.append([temp_coords[0], temp_coords[1]])  # add coords to position_list after checks

    # reset position tracker values to 0
    for count in position_tracker:
        position_tracker[count] = 0

    # encode the pixels of the image
    for element in range(len(position_list)):
        x_pos = position_list[element][0]
        y_pos = position_list[element][1]
        z_pos = position_tracker[(x_pos, y_pos)]

        pixel_list = list(pixels[x_pos, y_pos])
        if message_binary[message_counter] == "0":  # if number is zero, set pixel to nearest even number
            pixel_list[z_pos] -= pixel_list[z_pos] % 2
        elif message_binary[message_counter] == "1":  # if number is one, set pixel to nearest odd number
            if pixel_list[z_pos] % 2 == 0:
                if pixel_list[z_pos] == 0:
                    pixel_list[z_pos] += 1
                else:
                    pixel_list[z_pos] -= 1

        message_counter += 1
        position_tracker[(x_pos, y_pos)] += 1  # increment the position_tracker count
        pixels[x_pos, y_pos] = tuple(pixel_list)

    # save the image
    if "\\" in file:
        path_name = os.path.dirname(file)
        image.save(path_name + "\\" + name + ".png")
    else:
        image.save(name + ".png")

def decrypt(bits, key, file, char):
    bits = 8 if bits == "8-bit" else 7

    # open image
    image = Image.open(file)

    # set dimensions and read pixels
    width, height = image.size
    pixels = image.load()

    # set variables to hold message binary and converted plaintext
    message_binary = ""
    message_plaintext = ""

    position_list = []  # initialize list to hold pixel coordinates
    position_tracker = {(-1, -1): 3}  # initialize dictionary to track number of times coordinate is used
    sequence_counter = 0  # hold sequence number to ensure new numbers are generated
    num_of_coords = int(char) * bits  # specify number of pixel coordinates needed
    # set max numbers for each coordinate plane
    max_num_x = width - 1
    max_num_y = height - 1

    # generate pixel coordinates
    for coord in range(num_of_coords):
        temp_coords = (-1, -1)

        # while loop serves to regenerate coords if they appear 3 times
        while position_tracker[temp_coords] >= 3:
            random_x = random_num_gen(f"{key}{sequence_counter}", max_num_x)
            sequence_counter += 1
            random_y = random_num_gen(f"{key}{sequence_counter}", max_num_y)
            sequence_counter += 1
            temp_coords = (random_x, random_y)

            # check if coordinates are in position tracker, if not then add them, if they are then increment the count
            if temp_coords not in position_tracker:
                position_tracker[temp_coords] = 0
            else:
                position_tracker[temp_coords] += 1

        position_list.append([temp_coords[0], temp_coords[1]])  # add coords to position_list after checks

    # reset position tracker values to 0
    for count in position_tracker:
        position_tracker[count] = 0

    # loop through image reading pixels
    for element in range(len(position_list)):
        x_pos = position_list[element][0]
        y_pos = position_list[element][1]
        z_pos = position_tracker[(x_pos, y_pos)]

        if pixels[x_pos, y_pos][z_pos] % 2 == 0:
            message_binary += "0"
        else:
            message_binary += "1"

        position_tracker[(x_pos, y_pos)] += 1  # increment the position tracker

    # variables to temporarily hold the individual binary numbers and count how many are being held
    bin_holder = ""
    bin_counter = 0

    # translate the message from binary back into text
    for x in range(len(message_binary)):
        bin_holder += message_binary[x]
        bin_counter += 1
        if bin_counter % bits == 0:
            bin_holder = int(bin_holder, 2)  # convert to decimal
            message_plaintext += chr(bin_holder)  # convert to letter
            bin_holder = ""

    return message_plaintext
