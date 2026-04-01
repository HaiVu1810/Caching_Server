import argparse
from Socket_server import server_program
def main():
    parser = argparse.ArgumentParser(description='Caching Server')
    parser.add_argument('--port', type=int, help='Port to run the caching server on')
    parser.add_argument('--url', type=str, help='URL to fetch data from')
    args = parser.parse_args()

    print(f"Starting caching server on port {args.port}...")
    print(f"Fetching data from URL: {args.url}")
    server_program(args.port, args.url)
    # Here you would add the code to start the caching server
    # For example, you could use Flask or another web framework to handle requests
if __name__ == "__main__":
    main()