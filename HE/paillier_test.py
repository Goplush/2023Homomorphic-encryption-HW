import datetime
import random, sys 
import time
from gmpy2 import mpz, powmod, f_div, random_state, mpz_urandomb, gcd 
import matplotlib.pyplot as plt


import sys
sys.path.append("..")
import HE.paillier as paillier
import HE.logger as logger


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

def test(mode, bit_len, priv, pub, log:logger.Logger):
    rand = random_state(random.randrange(sys.maxsize))

    def generate_num(bit_len):
        return mpz(2)**(bit_len - 1) + mpz_urandomb(rand, bit_len - 1)
    
    log.writeline('=====TEST ' + mode + '=====')
    a = generate_num(bit_len)
    b = generate_num(bit_len)
    c = generate_num(bit_len)

    start = time.time()
    m1 = enc(pub, a)
    m2 = enc(pub, b)
    if mode == 'enc_add':
        enc_plain = enc_add(pub, m1, m2)
        ground_truth = powmod(a + b, 1, pub.n)
        log.writeline('a:'+ str(a) + '\tb:' + str(b)+'\tground_truth(a+b mod n):' + str(ground_truth))
    elif mode == 'enc_add_const':
        enc_plain = enc_add_const(pub, m1, c)
        ground_truth = powmod(a + c, 1, pub.n)
        log.writeline('a:'+ str(a) + '\tc:' + str(c)+'\tground_truth(a+c mod n):' + str(ground_truth))
    elif mode == 'enc_mul_const':
        enc_plain = enc_mul_const(pub, m1, c)
        ground_truth = powmod(a * c, 1, pub.n)
        log.writeline('a:'+ str(a) + '\tc:' + str(c)+'\tground_truth(a+c mod n):' + str(ground_truth))
    else:
        raise NotImplementedError

    dec_cipher = dec(priv, pub, enc_plain)
    end = time.time()
    log.writeline('dec_cipher:' + str(dec_cipher))

    if dec_cipher == ground_truth:
        log.writeline('=====PASS=====\n')
    else:
        log.writeline('=====FAIL=====\n')
    
    elapsed_time = end - start
    return elapsed_time


def integrated_testing():
    lengths = (512, 1024, 2048)
    modes = ('enc_add', 'enc_add_const', 'enc_mul_const')
    elapsed_times = {}
    keys = {}
    for l in lengths:
        keypair = paillier.keyGen_Pai(l)
        keys[l] = (keypair[0], keypair[1])
    log=logger.Logger("../logs/paillier_test.log")
    log.open_log()
    for mode in modes:
        elapsed_times[mode] = {}
        for key_len  in lengths:
            pub = keys[key_len][0]
            priv = keys[key_len][1]
            elapsed_times[mode][key_len] = list()
            for bit_len in range(10, 1000 + 10, 10):
                elapsed_times[mode][key_len].append(test(mode, bit_len, priv, pub, log))
            
    
    log.close_log()

    # plot elapsed times
    add_time_512 = elapsed_times['enc_add'][512]
    add_time_1024 = elapsed_times['enc_add'][1024]
    add_time_2048 = elapsed_times['enc_add'][2048]

    add_const_time_512 = elapsed_times['enc_add_const'][512]
    add_const_time_1024 = elapsed_times['enc_add_const'][1024]
    add_const_time_2048 = elapsed_times['enc_add_const'][2048]

    mul_const_time_512 = elapsed_times['enc_mul_const'][512]
    mul_const_time_1024 = elapsed_times['enc_mul_const'][1024]
    mul_const_time_2048 = elapsed_times['enc_mul_const'][2048]

    x = list(range(10, 1000 + 10, 10))
    f, ((ax1, ax2, ax7), (ax3, ax4, ax8), (ax5, ax6, ax9)) = plt.subplots(ncols=3, nrows=3, figsize=(10, 10))
    plt.suptitle('Elapsed times of Paillier')
    ax1.plot(x, add_time_512)
    ax1.set_xlabel('Message bits')
    ax1.set_ylabel('Add time(s) for 512 bit key')
    ax2.plot(x, add_time_1024)
    ax2.set_xlabel('Message bits')
    ax2.set_ylabel('Add time(s) for 1024 bit key')
    ax3.plot(x, add_const_time_512)
    ax3.set_xlabel('Message bits')
    ax3.set_ylabel('Add const time(s) for 512 bit key')
    ax4.plot(x, add_const_time_1024)
    ax4.set_xlabel('Message bits')
    ax4.set_ylabel('Add const time(s) for 1024 bit key')
    ax5.plot(x, mul_const_time_512)
    ax5.set_xlabel('Message bits')
    ax5.set_ylabel('Mul const time(s) for 512 bit key')
    ax6.plot(x, mul_const_time_1024)
    ax6.set_xlabel('Message bits')
    ax6.set_ylabel('Mul const time(s) for 1024 bit key')
    ax7.plot(x, add_time_2048)
    ax7.set_xlabel('Message bits')
    ax7.set_ylabel('Add time(s) for 2048 bit key')
    ax8.plot(x, add_const_time_2048)
    ax8.set_xlabel('Message bits')
    ax8.set_ylabel('Add const time(s) for 2048 bit key')
    ax9.plot(x, mul_const_time_2048)
    ax9.set_xlabel('Message bits')
    ax9.set_ylabel('Mul const time(s) for 2048 bit key')
    plt.tight_layout()
    current_time = datetime.datetime.now()
    # 将时间转换为字符串形式
    time_string = current_time.strftime("%Y$%m$%d$%H$%M$%S")
    plt.savefig('../logs/'+time_string+'+paillier_time.png')