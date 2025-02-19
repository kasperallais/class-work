# Problem 1
- Shannon's S-P networks, or substitution-permutation networks, are a type of network used to create block ciphers. They use a series of mathematical operations to transform plaintext into ciphertext. S-P nets are based on the two primitive cryptographic operations: substitution (S-box) and permutation (P-box). They provide confusion and diffusion of message and key. Diffusion makes the statistical relationship between the plaintext and ciphertext as complex as possible. This is achieved by repeated permutation followed by a function. Confusion makes the statistical relationship between ciphertext and key as complex as possible, this is achieved using complex substitution

# Problem 2
- To decrypt a ciphertext c using a single encryption oracle query for the given Feistel Cipher, we exploit the symmetric key schedule. The key schedule for the cipher uses the first eight round keys k1, k2, ..., k3 and then mirrors them for the next eight rounds k9=k8, k10=k7, ..., k16=k1. This symmetry implies that the key schedule for encryption is a palindrome. In a Feistel cipher, decryption typically requires reversing the order of the round keys. However, due to the key schedule here, reversing the order of the round keys results in the same sequence as the original encryption key schedule. This means that the decryption process is identical to the decryption process. Therefore, decrypting the ciphertext c can be achieved by encrypting c using the same key. By submitting c to the encryption oracle, the oracle will perform the encryption process, which is equivalent to the decryption due to the symmetric key schedule. The result of this encryption query will be the original plaintext m.

# Problem 3
- K1: 099731CE9EF7
- L0: CC00CCFF
- R0: F0AAF0AA
- E[R0]: 011110 100001 010101 010101 011110 100001 010101 010101
- A: 0x1C 0x38 0x09 0x24 0x2D 0x08 0x2E 0x22
- S-box Outputs: 0000 1001 0011 1001 0010 1001 1110 1011
- B: 093929EB
- P(B): 961AC8E5
- R1: 5A1A041A
- Ciphertext: 5A1A041AF0AAF0AA

# Problem 4
- The paper "The Data Encryption Standard (DES) and its Strength Against Attacks" is authored by Dr. Don Coppersmith, a mathematician who was a key member of the IBM team that developed DES. The paper focuses on DES, detailing its structure, design considerations, and resilience against cryptographic attacks, particularly differential cryptanalysis. This method attempt to exploit predictable differences in plaintext-ciphertext pairs to deduce the encryption key. The paper emphasizes that DES was deliberately design with build-in defenses against such attacks, a fact not public disclosed during its initial release to preserve national security advantages. From the paper, I learned that DES's strength largely comes from it's complex design of S-boxes and permutation functions. These components introduce non-linearity and diffusion, crucial for resisting differential cryptanalysis. The term "S-box Sj is active on round i" refers to the situation where the input difference to the S-box in a particular encryption round is non-zero. An active S-box plays a role in propagating differences through the cipher, which is critical in analyzing the cipher's security against differential attacks. Key discussion in the paper include the importance of multiple encryption rounds, the role of active S-boxes in enhancing security, and the challenges posed by known plaintext and chosen plaintext attacks. The paper also touches on linear cryptanalysis, highlighting the continual evolution of cryptographic attack methods and the corresponding need for robust cipher designs.
