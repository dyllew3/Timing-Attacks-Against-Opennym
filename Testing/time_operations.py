NUM_TESTS = 10
import requests

def main():
    with requests.Session() as s:
        for _ in range(NUM_TESTS):
            s.get('https://localhost:4400/nym', verify=False)
    return 0

if __name__ == "__main__":
    main()