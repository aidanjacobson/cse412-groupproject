import argparse
import os

from server import Server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, help="Path to data directory")
    args = parser.parse_args()

    if args.data_dir:
        os.environ["DATA_DIR"] = args.data_dir

    # Start the server
    print("Starting server on http://0.0.0.0:8080")
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
