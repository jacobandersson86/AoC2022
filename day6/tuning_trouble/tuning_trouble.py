import argparse

def readSignal(file) :
    signal = ''
    with open(file, 'r') as f :
        signal = f.read()
    return signal

def findStartOfPacket(signal : str, n : int) :
    for i, _ in enumerate(signal) :
        if i >= n :
            marker = signal[i-n:i]
            if len(set(marker)) == len(marker) :
                return i

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)

    args = parser.parse_args()

    signal = readSignal(args.file)

    n = findStartOfPacket(signal, 4)
    print(f"Solution 1: {n}")
    n = findStartOfPacket(signal, 14)
    print(f"Solution 2: {n}")
