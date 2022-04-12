#import library numpy
import numpy as np 
#module implementasi Euclidean algorithm.
from egcd import egcd

#inisialisasi jml huruf disini 26 huruf
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#konversi abjad ke angka dan angka ke abjad kembali
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))

def matrix_mod_inv(matrix, modulus):
    #mencari determinan
    det = int(np.round(np.linalg.det(matrix)))
    #mencari determinan invers sesuai dengan modulus (jml alphabet)
    det_inv = egcd(det, modulus)[1] % modulus 
    #mencari adjoint invers
    matrix_modulus_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )
    return matrix_modulus_inv

#fungsi enkripsi
def enkripsi(message, K):
    encrypted = ""
    message_in_numbers = []

    for letter in message:
        message_in_numbers.append(letter_to_index[letter])

    split_P = [
        message_in_numbers[i : i + int(K.shape[0])]
        for i in range(0, len(message_in_numbers), int(K.shape[0]))
    ]

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index["Z"])[:, np.newaxis]

        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0] #panjang pesan enkripsi dalam angka
        #mengembalikan angka ke teks alphabet
        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]

    return encrypted

#fungsi dekripsi
def dekripsi(cipher, Kinv):
    decrypted = ""
    cipher_in_numbers = []

    for letter in cipher:
        cipher_in_numbers.append(letter_to_index[letter])

    split_C = [
        cipher_in_numbers[i : i + int(Kinv.shape[0])]
        for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))
    ]

    for C in split_C:
        C = np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(Kinv, C) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]

    return decrypted


def main():
    message = 'SATUSEMBILANSATUNOLDUASATUDUAEMPAT'

    pesan1 = 'EKOYANUARSOBUDI'
    pesan2 = 'SATUSEMBILANSATUNOLDUASATUDUAEMPAT'
    pesan3 = 'TAKEARISK'

    #kunci matrix 3x3
    K = np.matrix([[3, 10, 20], [20,9,17], [9,4,17]]) # for length of alphabet = 26
    # K = np.matrix([[3,10,20],[20,9,17], [9,4,17]]) # for length of alphabet = 27
    Kinv = matrix_mod_inv(K, len(alphabet))

    enkripsi_pesan1 = enkripsi(pesan1,K)
    enkripsi_pesan2 = enkripsi(pesan2,K)
    enkripsi_pesan3 = enkripsi(pesan3,K)

    dekripsi_pesan1 = enkripsi(enkripsi_pesan1,Kinv)
    dekripsi_pesan2 = enkripsi(enkripsi_pesan2,Kinv)
    dekripsi_pesan3 = enkripsi(enkripsi_pesan3,Kinv)

    print("Pesan asli: " + pesan1 + ", " + pesan2 + ", " + pesan3)
    print("Pesan enkripsi: " + enkripsi_pesan1 + ", " + enkripsi_pesan2 + ", " + enkripsi_pesan3)
    print("Pesan dekripsi: " + dekripsi_pesan1 + ", " + dekripsi_pesan2 + ", " + dekripsi_pesan3)


main()