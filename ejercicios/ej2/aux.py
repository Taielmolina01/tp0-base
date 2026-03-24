def get_server_lines() -> list[str]:
    return [
        "name: tp0\n",
        "services:\n",
        "  server:\n",
        "    container_name: server\n",
        "    image: server:latest\n",
        "    entrypoint: python3 /main.py\n",
        "    environment:\n",
        "      - PYTHONUNBUFFERED=1\n",
        "    networks:\n",
        "      - testing_net\n",
        "    volumes:\n",
        "      - ./server/config.ini:/config/config.ini\n\n"
    ]

def get_client_lines(
    client_number: int,
    ) -> list[str]:
    return [
        f"  client{client_number}:\n",
        f"    container_name: client{client_number}\n",
        "    image: client:latest\n",
        "    entrypoint: /client\n",
        "    environment:\n",
        f"      - CLI_ID={client_number}\n",
        "    networks:\n",
        "      - testing_net\n",
        "    volumes:\n",
        "      - ./client/config.yaml:/config/config.yaml\n",
        f"      - ./.data/agency-{client_number}.csv:/.data/agency-{client_number}\n",
        "    depends_on:\n",
        "      - server\n\n"
    ]

def get_network_lines() -> list[str]:
    return [
        "networks:\n",
        "  testing_net:\n",
        "    ipam:\n",
        "      driver: default\n",
        "      config:\n",
        "        - subnet: 172.25.125.0/24\n\n"
    ]

def get_volumes_lines() -> list[str]:
    return [
        "volumes:\n",
        "  server_config:\n",
        "  client_config:\n"
    ]

def generate_compose_file(
        output_file: str, 
        amount_of_clients: int,
        client_config: dict[str, str]
        ):
    with open(output_file, 'w') as f:
        for line in get_server_lines():
            f.write(line)
        for i in range (1, amount_of_clients + 1):
            for line in get_client_lines(i, client_config):
                f.write(line)
        for line in get_network_lines():
            f.write(line)        
        for line in get_volumes_lines():
            f.write(line)