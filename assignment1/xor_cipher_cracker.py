import binascii
import sys

# English letter frequency scoring (relative %)
ENGLISH_FREQ = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7, 's': 6.3,
    'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8, 'u': 2.8, 'm': 2.4,
    'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5, 'k': 0.8,
    'v': 1.0, 'x': 0.1, 'j': 0.1, 'q': 0.1, 'z': 0.1, ' ': 13.0
}

def hamming_distance(b1, b2):
    return sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))

def score_text(data):
    score = 0
    for b in data:
        char = chr(b).lower()
        if char in ENGLISH_FREQ:
            score += ENGLISH_FREQ[char]
        elif 32 <= b <= 126: # Other printable
            score += 0.5
        elif b in [10, 13, 9]: # newline, tab
            score += 1.0
        else: # non-printable
            score -= 100
    return score

def detect_key_length(data, min_len=1, max_len=13):
    lengths = []
    for k in range(min_len, max_len + 1):
        num_blocks = len(data) // k
        if num_blocks < 2: continue
        
        dists = []
        for i in range(min(4, num_blocks - 1)): # Compare up to 4 blocks for speed/accuracy
            b1 = data[i*k : (i+1)*k]
            b2 = data[(i+1)*k : (i+2)*k]
            dists.append(hamming_distance(b1, b2) / k)
        
        if dists:
            avg_dist = sum(dists) / len(dists)
            lengths.append((k, avg_dist))
    
    lengths.sort(key=lambda x: x[1])
    return lengths[0][0], lengths

def recover_key(data, key_len):
    key = []
    for i in range(key_len):
        stream = data[i::key_len]
        best_byte = 0
        best_score = -float('inf')
        for b in range(256):
            decrypted = bytes([x ^ b for x in stream])
            s = score_text(decrypted)
            if s > best_score:
                best_score = s
                best_byte = b
        key.append(best_byte)
    return bytes(key)

def main():
    try:
        with open("ciphertext.txt", "r") as f:
            ciphertext_hex = f.read().strip()
        data = bytes.fromhex(ciphertext_hex)
    except Exception as e:
        print(f"Error reading ciphertext: {e}")
        return

    print(f"Cracking ciphertext ({len(data)} bytes)...")
    key_len, all_lens = detect_key_length(data)
    print(f"Detected key length: {key_len}")
    
    key = recover_key(data, key_len)
    print(f"Recovered key: {key.hex().upper()} ({repr(key.decode('ascii', errors='replace'))})")
    
    plaintext = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
    decoded = plaintext.decode('ascii', errors='replace')
    
    print("\n--- Decrypted Plaintext ---")
    print(decoded)
    print("---------------------------\n")
    
    with open("output/plaintext.txt", "w") as f:
        f.write(decoded)
    print("Result saved to output/plaintext.txt")

if __name__ == "__main__":
    main()
