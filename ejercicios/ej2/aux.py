def get_server_lines() -> [str]:
    return [
        "name: tp0\n",
        "services:\n",
        "  server:\n",
        "    container_name: server\n",
        "    image: server:latest\n",
        "    entrypoint: python3 /main.py\n",
        "    environment:\n",
        "      - PYTHONUNBUFFERED=1\n",
        "      - LOGGING_LEVEL=DEBUG\n",
        "    networks:\n",
        "      - testing_net\n",
        "    volumes:\n",
        "      - ./server/config.ini:/config\n\n"
    ]

def get_client_lines(
    client_number: int
    ) -> [str]:
    return [
        f"  client{client_number}:\n",
        f"    container_name: client{client_number}\n",
        "    image: client:latest\n",
        "    entrypoint: /client\n",
        "    environment:\n",
        f"      - CLI_ID={client_number}\n",
        "      - CLI_LOG_LEVEL=DEBUG\n",
        "    networks:\n",
        "      - testing_net\n",
        "    volumes:\n",
        "      - ./client/config.yaml:/config\n",
        "    depends_on:\n",
        "      - server\n\n"
    ]

def get_network_lines() -> [str]:
    return [
        "networks:\n",
        "  testing_net:\n",
        "    ipam:\n",
        "      driver: default\n",
        "      config:\n",
        "        - subnet: 172.25.125.0/24\n\n"
    ]

def get_volumes_lines() -> [str]:
    return [
        "volumes:\n",
        "  server_config:\n",
        "  client_config:\n"
    ]

def generate_compose_file(output_file: str, amount_of_clients: int):
    with open(output_file, 'w') as f:
        for line in get_server_lines():
            f.write(line)
        for i in range (1, amount_of_clients + 1):
            for line in get_client_lines(i):
                f.write(line)
        for line in get_network_lines():
            f.write(line)        
        for line in get_volumes_lines():
            f.write(line)