import sys
sys.path.append("..")

import datetime
import random
import time
from HE import ElGamal
from HE import logger


def test_mul_homomorphic(key_size, log: logger.Logger):
    # 生成 ElGamal 密钥对
    pub_key, pri_key = ElGamal.keyGen_Elg(key_size)
    
    # 保存密钥对
    ElGamal.save_key(pub_key, "elgamal_pubkey.txt", mode=0)
    ElGamal.save_key(pri_key, "elgamal_prikey.txt", mode=1)

    log.writeline(f"Public Key: {pub_key}")
    log.writeline(f"Private Key: {pri_key}")

    # 测试同态乘法
    a = random.randint(1, pub_key.q - 1)
    b = random.randint(1, pub_key.q - 1)

    log.writeline(f"Testing Homomorphic Multiplication:")
    log.writeline(f"a: {a}, b: {b}")

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

    log.writeline(f"Decrypted Result:")
    log.writeline(f"a * b mod q: {result}")

def performance_test(key_size_list, num_tests, log: logger.Logger):
    log.writeline("\n===== Performance Test =====")
    for key_size in key_size_list:
        total_time = 0.0
        log.writeline(f"\nKey Size: {key_size} bits")
        for _ in range(num_tests):
            start_time = time.time()
            test_mul_homomorphic(key_size, log)
            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time
            log.writeline(f"Test Time: {elapsed_time:.6f} seconds")
        average_time = total_time / num_tests
        log.writeline(f"Average Test Time: {average_time:.6f} seconds\n")

def main():
    key_size_list = [512, 1024, 2048]  # 设置不同密钥长度
    num_tests = 5  # 每个密钥长度运行的测试次数
    log = logger.Logger("elgamal_test.log")
    log.open_log()

    log.writeline(f"===== ElGamal Homomorphic Multiplication Test =====")
    test_mul_homomorphic(key_size_list[0], log)  # 运行一次简单测试

    performance_test(key_size_list, num_tests, log)

    log.close_log()

if __name__ == "__main__":
    main()
