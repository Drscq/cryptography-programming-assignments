# Assignment 1: XOR Vigenere Cipher Cracking

## Problem
Decrypt a hex-encoded ciphertext encrypted with a repeating-key XOR cipher.
The key length is between 1 and 13.
The original text is English.

## Files
- `ciphertext.txt`: The hex-encoded ciphertext.
- `xor_cipher_cracker.py`: Python script to crack the cipher.
- `output/plaintext.txt`: The decrypted plaintext result.

## Methodology
1. **Key Length Detection**: Uses **Normalized Hamming Distance**.
2. **Frequency Analysis**: Breaks each byte of the key independently by scoring against English letter frequencies.
3. **Decryption**: Recovers the original English text.

## Usage
```bash
python3 xor_cipher_cracker.py
```
