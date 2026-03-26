import sys
from aux import generate_compose_file

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

    generate_compose_file(output_file, amount_of_clients)


if __name__ == "__main__":
    main()
