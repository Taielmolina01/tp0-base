import sys
from aux import generate_compose_file

EXPECTED_AMOUNT_OF_ARGUMENTS = 7
MSG_WRONG_AMOUNT_OF_ARGUMENTS = f"""Bad amount of arguments. 
        This program must be called with {EXPECTED_AMOUNT_OF_ARGUMENTS} arguments.
        Example: 'python3 generate_compose.py ${{output_file}} ${{amount_of_clients}} ${{client_name}} ${{client_last_name}} ${{client_dni}} ${{client_birthday}} ${{client_bet_number}}'"""


def main():
    if len(sys.argv) != EXPECTED_AMOUNT_OF_ARGUMENTS + 1:
        print(MSG_WRONG_AMOUNT_OF_ARGUMENTS)
        return

    output_file = sys.argv[1]
    amount_of_clients = int(sys.argv[2])
    client_config = {
        "name": sys.argv[3],
        "last_name": sys.argv[4],
        "dni": sys.argv[5],
        "birthday": sys.argv[6],
        "bet_number": sys.argv[7],
    }

    # chequear estos valores

    generate_compose_file(output_file, amount_of_clients, client_config)


if __name__ == "__main__":
    main()
