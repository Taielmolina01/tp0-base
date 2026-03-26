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
        "      - LOGGING_LEVEL=DEBUG\n",
        "    networks:\n",
        "      - testing_net\n\n",
    ]


def get_client_lines(client_number: int) -> list[str]:
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
        "    depends_on:\n",
        "      - server\n\n",
    ]


def get_network_lines() -> list[str]:
    return [
        "networks:\n",
        "  testing_net:\n",
        "    ipam:\n",
        "      driver: default\n",
        "      config:\n",
        "        - subnet: 172.25.125.0/24\n",
    ]
