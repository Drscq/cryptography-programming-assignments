# Cryptography Programming Assignments

This repository contains solutions and implementations for various cryptography programming assignments.

## Assignments

### [Assignment 1: XOR Vigenere Cipher Cracking](./assignment1)

**Goal:** Decrypt a hex-encoded ciphertext encrypted with a repeating-key XOR cipher.

**Key Features:**
- **Key Length Detection**: Uses Normalized Hamming Distance to estimate the likely key length.
- **Frequency Analysis**: Breaks each byte of the key independently by scoring against English letter frequencies.
- **Decryption**: Recovers the original English text.

**Location:** [`assignment1/`](./assignment1/)