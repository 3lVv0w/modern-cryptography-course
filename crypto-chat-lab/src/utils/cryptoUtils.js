// Standard English Letter Frequencies (%)
const ENGLISH_FREQUENCIES = {
  'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
  'S': 6.33, 'H': 6.09, 'R': 5.98, 'D': 4.25, 'L': 4.03, 'C': 2.78,
  'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.01, 'Y': 1.97,
  'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
  'Q': 0.10, 'Z': 0.07
};

// ==============================================================================
// SYMMETRIC CIPHERS
// ==============================================================================

export function caesarEncrypt(plaintext, shift) {
  const k = parseInt(shift, 10) || 0;
  return plaintext.split('').map(char => {
    if (/[a-zA-Z]/.test(char)) {
      const base = char === char.toUpperCase() ? 65 : 97;
      return String.fromCharCode((char.charCodeAt(0) - base + k + 26) % 26 + base);
    }
    return char;
  }).join('');
}

export function caesarDecrypt(ciphertext, shift) {
  const k = parseInt(shift, 10) || 0;
  return caesarEncrypt(ciphertext, -k);
}

export function rot13(plaintext) {
  return caesarEncrypt(plaintext, 13);
}

export function vigenereEncrypt(plaintext, keyword) {
  if (!keyword) return plaintext;
  const kw = keyword.toUpperCase().replace(/[^A-Z]/g, '');
  if (kw.length === 0) return plaintext;
  
  let keyIdx = 0;
  return plaintext.split('').map(char => {
    if (/[a-zA-Z]/.test(char)) {
      const base = char === char.toUpperCase() ? 65 : 97;
      const kShift = kw.charCodeAt(keyIdx % kw.length) - 65;
      keyIdx++;
      return String.fromCharCode((char.charCodeAt(0) - base + kShift) % 26 + base);
    }
    return char;
  }).join('');
}

export function vigenereDecrypt(ciphertext, keyword) {
  if (!keyword) return ciphertext;
  const kw = keyword.toUpperCase().replace(/[^A-Z]/g, '');
  if (kw.length === 0) return ciphertext;

  let keyIdx = 0;
  return ciphertext.split('').map(char => {
    if (/[a-zA-Z]/.test(char)) {
      const base = char === char.toUpperCase() ? 65 : 97;
      const kShift = kw.charCodeAt(keyIdx % kw.length) - 65;
      keyIdx++;
      return String.fromCharCode((char.charCodeAt(0) - base - kShift + 26) % 26 + base);
    }
    return char;
  }).join('');
}

// ==============================================================================
// ASYMMETRIC PUBLIC KEY / PRIVATE KEY CRYPTOGRAPHY (RSA)
// ==============================================================================

// Helper BigInt Modular Exponentiation: (base^exp) % mod
function modPowBigInt(base, exp, mod) {
  let res = 1n;
  let b = base % mod;
  let e = exp;
  while (e > 0n) {
    if (e % 2n === 1n) res = (res * b) % mod;
    b = (b * b) % mod;
    e = e / 2n;
  }
  return res;
}

// Extended Euclidean Algorithm for BigInt
function extGCD(a, b) {
  if (a === 0n) return { g: b, x: 0n, y: 1n };
  const { g, x: x1, y: y1 } = extGCD(b % a, a);
  const x = y1 - (b / a) * x1;
  const y = x1;
  return { g, x, y };
}

function modInvBigInt(a, m) {
  const { g, x } = extGCD(a, m);
  if (g !== 1n) return null;
  return (x % m + m) % m;
}

// Generate RSA Key Pair (Demonstration Primes & Standard Public Key)
export function generateRSAKeyPair(smallDemo = true) {
  // Demo primes for educational clarity (e.g. p=61, q=53 => N=3233)
  // or medium primes (p=1009, q=1013 => N=1022117)
  const p = smallDemo ? 1009n : 61n;
  const q = smallDemo ? 1013n : 53n;
  const N = p * q;
  const phi = (p - 1n) * (q - 1n);
  const e = 65537n < phi ? 65537n : 3n;
  const d = modInvBigInt(e, phi);

  return {
    publicKey: { N: N.toString(16), e: e.toString(16) },
    privateKey: { N: N.toString(16), d: d.toString(16) },
    p: p.toString(10),
    q: q.toString(10)
  };
}

export function rsaEncrypt(plaintext, publicKey) {
  if (!publicKey || !publicKey.N || !publicKey.e) return plaintext;
  const N = BigInt('0x' + publicKey.N);
  const e = BigInt('0x' + publicKey.e);

  // Convert string to BigInt
  const encoder = new TextEncoder();
  const bytes = encoder.encode(plaintext);
  let hexStr = '0x';
  for (let b of bytes) {
    hexStr += b.toString(16).padStart(2, '0');
  }
  const mInt = BigInt(hexStr);

  if (mInt >= N) {
    // If message is too large for modulus, fallback chunking or simple error
    throw new Error(`Message integer exceeds RSA modulus N (${N})! Try a shorter message.`);
  }

  const cInt = modPowBigInt(mInt, e, N);
  return `RSA-CIPHER:${cInt.toString(16)}`;
}

export function rsaDecrypt(ciphertextPayload, privateKey) {
  if (!ciphertextPayload || !ciphertextPayload.startsWith('RSA-CIPHER:')) return ciphertextPayload;
  if (!privateKey || !privateKey.N || !privateKey.d) return '[INVALID PRIVATE KEY]';

  const hexCipher = ciphertextPayload.replace('RSA-CIPHER:', '');
  const cInt = BigInt('0x' + hexCipher);
  const N = BigInt('0x' + privateKey.N);
  const d = BigInt('0x' + privateKey.d);

  const mInt = modPowBigInt(cInt, d, N);
  
  // Convert BigInt back to String
  let hexStr = mInt.toString(16);
  if (hexStr.length % 2 !== 0) hexStr = '0' + hexStr;
  
  const bytes = [];
  for (let i = 0; i < hexStr.length; i += 2) {
    bytes.push(parseInt(hexStr.substr(i, 2), 16));
  }
  const decoder = new TextDecoder();
  return decoder.decode(new Uint8Array(bytes));
}

// Crack RSA Modulus for Instructor Dashboard via Fermat / Trial Factorization
export function crackRSAModulus(N_hex, e_hex, ciphertextPayload) {
  if (!N_hex || !ciphertextPayload) return { bestText: '[NO PAYLOAD]', score: Infinity };
  
  try {
    const N = BigInt('0x' + N_hex);
    const e = BigInt('0x' + (e_hex || '10001'));
    
    // Trial factor small/medium N
    let p = 0n;
    let q = 0n;
    for (let i = 3n; i * i <= N; i += 2n) {
      if (N % i === 0n) {
        p = i;
        q = N / i;
        break;
      }
    }

    if (p === 0n) {
      return { bestText: '[RSA MODULUS TOO LARGE TO FACTOR ON CLIENT]', bestKey: `N=${N_hex}`, score: 999 };
    }

    const phi = (p - 1n) * (q - 1n);
    const d = modInvBigInt(e, phi);

    const decrypted = rsaDecrypt(ciphertextPayload, { N: N.toString(16), d: d.toString(16) });
    return {
      bestText: decrypted,
      bestKey: `Fermat RSA Cracked (p=${p}, q=${q}, d=0x${d.toString(16)})`,
      score: 0
    };
  } catch (err) {
    return { bestText: `[RSA CRACK ERROR: ${err.message}]`, bestKey: 'N/A', score: 999 };
  }
}

// ==============================================================================
// AUTOMATED CRYPTANALYSIS SUITE
// ==============================================================================

export function computeChiSquared(text) {
  const clean = text.toUpperCase().replace(/[^A-Z]/g, '');
  const N = clean.length;
  if (N === 0) return Infinity;

  const counts = {};
  for (let char of clean) {
    counts[char] = (counts[char] || 0) + 1;
  }

  let chiSq = 0.0;
  for (let [letter, expectedPct] of Object.entries(ENGLISH_FREQUENCIES)) {
    const expectedCount = N * (expectedPct / 100.0);
    const observedCount = counts[letter] || 0;
    chiSq += Math.pow(observedCount - expectedCount, 2) / (expectedCount + 1e-6);
  }
  return chiSq;
}

export function autoBreakCipher(ciphertext, hintType = 'Caesar', hintKey = '', publicKeyObj = null) {
  if (!ciphertext) return { bestText: '', bestKey: 'N/A', score: Infinity };

  // Handle Asymmetric RSA Cryptanalysis
  if (ciphertext.startsWith('RSA-CIPHER:')) {
    if (publicKeyObj && publicKeyObj.N) {
      return crackRSAModulus(publicKeyObj.N, publicKeyObj.e, ciphertext);
    }
    return {
      bestText: '[RSA ASYMMETRIC PAYLOAD - REQUIRED PRIVATE KEY OR FACTORING N]',
      bestKey: 'RSA (Public Key Encrypted)',
      score: 999
    };
  }

  if (hintType === 'Vigenère' && hintKey) {
    const text = vigenereDecrypt(ciphertext, hintKey);
    return { bestText: text, bestKey: `Vigenère('${hintKey}')`, score: computeChiSquared(text) };
  }

  if (hintType === 'ROT13') {
    const text = rot13(ciphertext);
    return { bestText: text, bestKey: 'ROT13 (Shift 13)', score: computeChiSquared(text) };
  }

  // Default: Automated Chi-Squared Caesar Breaker across shifts 0..25
  let bestShift = 0;
  let minScore = Infinity;
  let bestPlaintext = ciphertext;

  for (let shift = 0; shift < 26; shift++) {
    const candidate = caesarDecrypt(ciphertext, shift);
    const score = computeChiSquared(candidate);
    if (score < minScore) {
      minScore = score;
      bestShift = shift;
      bestPlaintext = candidate;
    }
  }

  return {
    bestText: bestPlaintext,
    bestKey: `Caesar (Shift ${bestShift})`,
    score: Math.round(minScore * 100) / 100
  };
}
