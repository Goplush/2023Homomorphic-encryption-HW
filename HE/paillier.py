# -*- coding: utf-8 -*-
# @Time    : 2022-09-01 13:25
# @Author  : gzzz
# @FileName: paillier.py
# @Software: PyCharm
# -*- coding: utf-8 -*-


import sys
import os
import math
import random
from random import shuffle
import sys
import gmpy2
from time import time
from Crypto.Util.number import getPrime

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import random
import time
from HE.util import generateLargePrime, isPrime, get_pri_root, powmod, getinv


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def int_time():
    return int(round(time.time() * 1000))

def addemup(pub, a, b):
    return gmpy2.mul(a, b)


def multime(pub, a, n):
    return gmpy2.powmod(a, n, pub.n_sq)

class PaillierPublicKey(object):
    '''
    Paillier加密算法
    '''

    def __init__(self, n):
        self.n = n
        self.n_sq = n * n
        self.g = n + 1

    def __repr__(self):
        return 'PublicKey({})'.format(self.n)

    def encrypt_int(self, m):
        one = gmpy2.mpz(1)
        state = gmpy2.random_state(int_time())
        r = gmpy2.mpz_random(state, self.n)
        while gmpy2.gcd(r, self.n) != one:
            state = gmpy2.random_state(int_time())
            r = gmpy2.mpz_random(state, self.n)
        x = gmpy2.powmod(r, self.n, self.n_sq)
        cipher = gmpy2.f_mod(gmpy2.mul(gmpy2.powmod(self.g, m, self.n_sq), x), self.n_sq)
        return cipher

    def evaluate_int(self, C1, C2):
        '''
        # 功能：实现两个密文间的同态加法
        # 接受参数：C1(c1, c2)
        # 返回参数：C(c1, c2)
        '''
        return C1 * C2 % (self.n * self.n)


class PaillierPrivateKey(object):
    '''
    x集合于(1, q - 1)
    '''

    def __init__(self, p, q, n):
        self.l = lcm(p - 1, q - 1)
        self.m = gmpy2.invert(gmpy2.f_div(gmpy2.sub(gmpy2.powmod(n + 1, self.l, n * n), gmpy2.mpz(1)), n), n)
        self.n = n
        self.p = p
        self.q = q

    def __repr__(self):
        return 'PrivateKey({}, {})'.format(self.l, self.m)

    def decrypt_int(self, cipher):
        one = gmpy2.mpz(1)
        x = gmpy2.sub(gmpy2.powmod(cipher, self.l, self.n*self.n), one)
        m = gmpy2.f_mod(gmpy2.mul(gmpy2.f_div(x, self.n), self.m), self.n)
        if m >= gmpy2.f_div(self.n, 2):
            m = m - self.n
        return m

def keyGen_Pai(keysize=1024):
    '''
    # 功能：生成keysize比特的密钥
    # 接受参数：keysize
    # 返回参数：(q, g, h), (q, x)
    '''
    start = time.time()
    p_equal_q = True
    while p_equal_q:
        p = getPrime(keysize // 2)
        q = getPrime(keysize // 2)
        if p != q and gcd(p * q, (p - 1) * (q - 1)) == 1:
            p_equal_q = False
    n = p * q
    end = time.time()
    print('密钥生成耗时: {}s'.format(end - start))
    return (PaillierPublicKey(n), PaillierPrivateKey(p, q, n))


def save_key(key, filename, mode=0):
    '''
    # 功能：保存paillier算法算法所需要的密钥
    # 接受参数：key是对应的公钥或者私钥类, filename(密钥文件名), mode为0代表公钥类 1是私钥
    # 返回参数：True(保存成功) / False(保存失败)
    '''
    try:
        if mode != 1:
            mode == 0
        with open(filename, 'w', encoding='utf-8') as f:
            if mode == 0:
                content = str(key.n) + ',' + str(key.n_sq) + ',' + str(key.g)
                f.write(content)
                return True
            elif mode == 1:
                content = str(key.l) + ',' + str(key.m) + ',' + str(key.p) + ',' + str(key.q)
                f.write(content)
                return True
            return False
    except Exception as e:
        print(e)
        return False


def load_key(filename, mode=0):
    '''
    # 功能：加载Paillier算法所需要的密钥
    # 接受参数：filename(密钥文件名), mode为0代表加载的为公钥, mode为1代表加载为私钥
    # 返回参数：成功打开则返回pubkey(q, g, h) / prikey(q, x) 失败为False
    '''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read(-1).split(',')
            for i in range(len(data)):
                data[i] = int(data[i])
            if mode == 1:
                (l, m, p, q) = data[0], data[1], data[2], data[3]
                return PaillierPrivateKey(p, q, p*q)
            else:
                (n, n_sq, g) = data[0], data[1], data[2]
                return PaillierPublicKey(n)
    except Exception as e:
        print(e)
        return





if __name__ == "__main__":
    keysize = 2048
    pubname = '../key/pai_public_key_' + str(keysize) + '.txt'
    priname = '../key/pai_private_key_' + str(keysize) + '.txt'

    pubkey, prikey = keyGen_Pai(keysize=keysize)
    ok = save_key(pubkey, pubname, 0)
    print(ok)
    ok = save_key(prikey, priname, 1)
    print(ok)

    pubkey = load_key(pubname, 0)
    prikey = load_key(priname, 1)

    num1 = 2 ** 100
    num2 = 3
    C1 = pubkey.encrypt_int(num1)
    C2 = pubkey.encrypt_int(num2)
    ans = prikey.decrypt_int(pubkey.evaluate_int(C1, C2))
    print(ans == num1 + num2)