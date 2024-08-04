from enum import Enum


class Connector(str, Enum):
    kubernetes = "kubernetes"
    # docker = "docker"
    # aws = "aws"


def list_connectors():
    connectors = [connector.value for connector in Connector]
    return connectors


if __name__ == "__main__":
    print(list_connectors())
