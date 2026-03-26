import sys
from aux import *

EXPECTED_AMOUNT_OF_ARGUMENTS = 2
MSG_WRONG_AMOUNT_OF_ARGUMENTS = f"""Bad amount of arguments. 
        This program must be called with {EXPECTED_AMOUNT_OF_ARGUMENTS} arguments.
        Example: 'python3 generate_compose.py ${{output_file}} ${{amount_of_clients}}'"""


def main():
    if len(sys.argv) != EXPECTED_AMOUNT_OF_ARGUMENTS + 1:
        print(MSG_WRONG_AMOUNT_OF_ARGUMENTS)
        return

    output_file = sys.argv[1]
    amount_of_clients = int(sys.argv[2])

    with open(output_file, "w") as f:
        for line in get_server_lines():
            f.write(line)
        for i in range(1, amount_of_clients + 1):
            for line in get_client_lines(i):
                f.write(line)
        for line in get_network_lines():
            f.write(line)


if __name__ == "__main__":
    main()
