import sys
from threading import current_thread

from matplotlib import pyplot as plt
sys.path.append("..")

import datetime
import random
import time
from HE import ElGamal
from HE import logger
from gmpy2 import mpz, powmod, f_div, random_state, mpz_urandomb, gcd 

def generate_num(bit_len):
        rand = random_state(random.randrange(sys.maxsize))
        return mpz(2)**(bit_len - 1) + mpz_urandomb(rand, bit_len - 1)

def test_mul_homomorphic(key_size, log: logger.Logger, num_range=1000):

    test_times = []
    bit_lengths = []

    
    time_start=time.time()
    # 生成 ElGamal 密钥对
    pub_key, pri_key = ElGamal.keyGen_Elg(key_size)
    time_end=time.time()
    key_gen_time=time_end-time_start
    log.writeline(f"==========KEY GENERATION TIME===========\n\tkey length: {key_size} bit\tgeneration time: {key_gen_time}")

    for bit_len in range(10, num_range + 10, 10):

        log.writeline(f"\nsetting: number length: {bit_len}")
        # 测试同态乘法
        a = generate_num(bit_len)
        b = generate_num(bit_len)

        ground_truth = (a*b)%pub_key.q
        log.writeline(f"a: {a}, b: {b}")

        time_start=time.time()

        # 加密
        C1_a, C2_a = pub_key.encrypt_int(a)
        C1_b, C2_b = pub_key.encrypt_int(b)

        log.writeline(f"Ciphertext (a): ({C1_a}, {C2_a})")
        log.writeline(f"Ciphertext (b): ({C1_b}, {C2_b})")

        # 同态乘法
        C1_mul, C2_mul = pub_key.evaluate_int((C1_a, C2_a), (C1_b, C2_b))

        log.writeline(f"Homomorphic Multiplication Result:")
        log.writeline(f"Ciphertext (a * b): ({C1_mul}, {C2_mul})")

        # 解密
        result = pri_key.decrypt_int((C1_mul, C2_mul))
        time_end=time.time()

        test_time=time_end-time_start

        log.writeline(f"Decrypted Result:{result}\tGround truth, (a * b) mod q: {ground_truth}")
        log.writeline("====pass=====\n" if ground_truth==result else "========Fail=======\n")

        test_times.append(test_time)
        bit_lengths.append(bit_len)

    return test_times, bit_lengths


def test():
    key_size_list = [512, 1024, 2048]  # 设置不同密钥长度
    log = logger.Logger("../logs/elgamal_test.log")
    log.open_log()
    test_time_dict = {}
    bit_len_dict = {}


    log.writeline(f"===== ElGamal Homomorphic Multiplication Test =====")
    for key_size in key_size_list:
        test_time_dict[key_size], bit_len_dict[key_size] = test_mul_homomorphic(key_size, log)
    log.close_log()

    f, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1, figsize=(10, 10))
    ax1.plot(bit_len_dict[512],test_time_dict[512])
    ax1.set_xlabel('Bits')
    ax1.set_ylabel('encryption time(s) with key length: 512')
    ax2.plot(bit_len_dict[1024],test_time_dict[1024])
    ax2.set_xlabel('Bits')
    ax2.set_ylabel('encryption time(s) with key length: 1024')
    ax3.plot(bit_len_dict[2048],test_time_dict[2048])
    ax3.set_xlabel('Bits')
    ax3.set_ylabel('encryption time(s) with key length: 2048')
    plt.tight_layout()
    current_time = datetime.datetime.now()
    # 将时间转换为字符串形式
    time_string = current_time.strftime("%Y$%m$%d$%H$%M$%S")
    plt.savefig('../logs/'+time_string+'+elgamal_time.png')


if __name__ == "__main__":
    test()
