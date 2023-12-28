import datetime
import random, sys 
import time
from gmpy2 import mpz, powmod, f_div, invert, is_prime, random_state, mpz_urandomb, rint_round, log2, gcd 
from termcolor import colored
import matplotlib.pyplot as plt


import sys
sys.path.append("..")
import HE.paillier as paillier

class Logger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None

    def open_log(self):
        self.file = open(self.file_path, 'a')  # 'a' mode appends to the file, creates if not exists
        current_time = datetime.datetime.now()
        # 将时间转换为字符串形式
        time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.writeline("\n New logging start at\t"+time_string)


    def writeline(self, message):
        log_line = f"{message}\n"
        self.file.write(log_line)

    def close_log(self):
        current_time = datetime.datetime.now()
        # 将时间转换为字符串形式
        time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.writeline("Logging end at\t"+time_string+'\n')
        self.file.close()

def enc(pub, plain):
    """Parameters: public key, plaintext"""

    def generate_r(n):
        """generate a random number s.t. gcd(r, n) = 1"""    
        while True:
            r = mpz(random.randint(1, n - 1))
            if gcd(r, n) == 1:
                return r
    
    # Mathematically:
    # (a * b) mod c = (a mod c * b mod c) mod c
    # c = (g^m * r^n) mod n^2 = (g^m mod n^2 * r^n mod n^2) mod n^2
    g, n, n_sq = pub.n +1, pub.n, pub.n_sq
    r = generate_r(n)
    cipher = powmod(powmod(g, plain, n_sq) * powmod(r, n, n_sq), 1, n_sq)
    return cipher

def dec(priv, pub, cipher):
    """Parameters: private key, public key, cipher"""
    n, n_sq = pub.n, pub.n_sq
    x = powmod(cipher, priv.l, n_sq)
    L = f_div(x - 1, n)
    plain = powmod(mpz(L * priv.m), 1, n)
    return plain

def enc_add(pub, m1, m2):
    """Add one encrypted integer to another"""
    return powmod(m1 * m2, 1, pub.n_sq)

def enc_add_const(pub, m, c):
    """Add a constant to an encrypted integer"""
    n_sq = pub.n_sq
    return powmod(powmod(m, 1, n_sq) * powmod(pub.g, c, n_sq), 1, n_sq)

def enc_mul_const(pub, m, c):
    """Multiply an encrypted integer by a constant"""
    return powmod(m, c, pub.n_sq)

def test(mode, bit_len, priv, pub, log:Logger):
    rand = random_state(random.randrange(sys.maxsize))

    def generate_num(bit_len):
        return mpz(2)**(bit_len - 1) + mpz_urandomb(rand, bit_len - 1)
    
    elapsed_times = {}
    log.writeline('=====TEST ' + mode + '=====')
    a = generate_num(bit_len)
    b = generate_num(bit_len)
    c = generate_num(bit_len)

    enc_start = time.time()
    m1 = enc(pub, a)
    m2 = enc(pub, b)
    if mode == 'enc_add':
        enc_plain = enc_add(pub, m1, m2)
        enc_end = time.time()
        ground_truth = powmod(a + b, 1, pub.n)
        log.writeline('a:'+ str(a) + '\tb:' + str(b)+'\tground_truth(a+b mod n):' + str(ground_truth))
    elif mode == 'enc_add_const':
        enc_plain = enc_add_const(pub, m1, c)
        enc_end = time.time()
        ground_truth = powmod(a + c, 1, pub.n)
        log.writeline('a:'+ str(a) + '\tc:' + str(c)+'\tground_truth(a+c mod n):' + str(ground_truth))
    elif mode == 'enc_mul_const':
        enc_plain = enc_mul_const(pub, m1, c)
        enc_end = time.time()
        ground_truth = powmod(a * c, 1, pub.n)
        log.writeline('a:'+ str(a) + '\tc:' + str(c)+'\tground_truth(a+c mod n):' + str(ground_truth))
    else:
        raise NotImplementedError

    dec_start = time.time()
    dec_cipher = dec(priv, pub, enc_plain)
    dec_end = time.time()
    log.writeline('dec_cipher:' + str(dec_cipher))

    if dec_cipher == ground_truth:
        log.writeline('=====PASS=====\n')
    else:
        log.writeline('=====FAIL=====\n')
    
    elapsed_times['enc'] = enc_end - enc_start
    elapsed_times['dec'] = dec_end - dec_start
    return elapsed_times


def integrated_testing():
    pub, priv = paillier.keyGen_Pai()
    add_enc_times = []
    add_dec_times = []
    add_const_enc_times = []
    add_const_dec_times = []
    mul_const_enc_times = []
    mul_const_dec_times = []
    log=Logger("../logs/paillier_test.log")
    log.open_log()

    for bit_len in range(10, 1000 + 10, 10):
        elapsed_times = {}
        elapsed_times['enc_add'] = test('enc_add', bit_len, priv, pub, log)
        elapsed_times['enc_add_const'] = test('enc_add_const', bit_len, priv, pub, log)
        elapsed_times['enc_mul_const'] = test('enc_mul_const', bit_len, priv, pub, log)
        
        add_enc_times.append(elapsed_times['enc_add']['enc'])
        add_dec_times.append(elapsed_times['enc_add']['dec'])
        add_const_enc_times.append(elapsed_times['enc_add_const']['enc'])
        add_const_dec_times.append(elapsed_times['enc_add_const']['dec'])
        mul_const_enc_times.append(elapsed_times['enc_mul_const']['enc'])
        mul_const_dec_times.append(elapsed_times['enc_mul_const']['dec'])
    
    log.close_log()

    # plot elapsed times
    x = list(range(10, 1000 + 10, 10))
    f, ((ax1, ax2, ax7), (ax3, ax4, ax8), (ax5, ax6, ax9)) = plt.subplots(ncols=3, nrows=3, figsize=(10, 10))
    plt.suptitle('Elapsed times of Paillier')
    ax1.plot(x, add_enc_times)
    ax1.set_xlabel('Bits')
    ax1.set_ylabel('Add encryption time(s)')
    ax2.plot(x, add_dec_times)
    ax2.set_xlabel('Bits')
    ax2.set_ylabel('Add decryption time(s)')
    ax3.plot(x, add_const_enc_times)
    ax3.set_xlabel('Bits')
    ax3.set_ylabel('Add const encryption time(s)')
    ax4.plot(x, add_const_dec_times)
    ax4.set_xlabel('Bits')
    ax4.set_ylabel('Add const decryption time(s)')
    ax5.plot(x, mul_const_enc_times)
    ax5.set_xlabel('Bits')
    ax5.set_ylabel('Mul const encryption time(s)')
    ax6.plot(x, mul_const_dec_times)
    ax6.set_xlabel('Bits')
    ax6.set_ylabel('Mul const decryption time(s)')
    ax7.plot(x, [t1 + t2 for t1, t2 in zip(add_enc_times, add_dec_times)])
    ax7.set_xlabel('Bits')
    ax7.set_ylabel('Add total time(s)')
    ax8.plot(x, [t1 + t2 for t1, t2 in zip(add_const_enc_times, add_const_dec_times)])
    ax8.set_xlabel('Bits')
    ax8.set_ylabel('Add const total time(s)')
    ax9.plot(x, [t1 + t2 for t1, t2 in zip(mul_const_enc_times, mul_const_dec_times)])
    ax9.set_xlabel('Bits')
    ax9.set_ylabel('Mul const total time(s)')
    plt.tight_layout()
    current_time = datetime.datetime.now()
    # 将时间转换为字符串形式
    time_string = current_time.strftime("%Y$%m$%d$%H$%M$%S")
    plt.savefig('../logs/'+time_string+'+paillier_time.png')