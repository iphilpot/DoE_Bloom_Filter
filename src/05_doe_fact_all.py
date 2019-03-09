#!/usr/bin/env python

from model.bloom_filter import BloomFilter
from model.users import PresentUsers, AbsentUsers
import matplotlib.pyplot as plt 

# This is the last experiment, a 2 factorial designed experiment. The goal is to understand 
# the mass effect of each variable, but also the interaction between the to variables we control
# and how they affect the respons variable (false positives). 
def main():
    
    # Present file contains 10,000 generated usernames that are added to the bloom filter.
    present_users_file = './src/resources/present.txt'

    # Absent file contains 1,000 generated usersnames that are not in the bloom filter.
    absent_users_file = './src/resources/absent.txt'

    # Read files into models
    present_users = PresentUsers(present_users_file)
    absent_users = AbsentUsers(absent_users_file)

    # Loop over a specified range of ints to adjust both the bit array size
    # and the hash pass count for the bloom filter. M Range is 50,000 to 70,000 with 
    # a step of 10,000. This should surround the right sized value of 62352. k range is 3 to
    # 5 and also should surround the right sized value of 4.
    # TODO: O(n^2) - refactor to more be efficient using a memoization pattern.
    cnt_size = []
    cnt_passes = []
    cnt_fp = []
    for hash_count in range(3, 5):
        for bit_arr_size in range(50000, 70000, 10000):

            # Bloom filter with varying values for both hash passes and bit array sizes 
            # for 10,000 items
            bloom_filter = BloomFilter(bit_arr_size, hash_count)

            # Add present users to the bloom filter.
            for i in range(len(present_users)):
                bloom_filter += present_users[i]

            # Test for absent users and count the false positives.
            false_positive_count = 0
            for user in absent_users:
                if user in bloom_filter:
                    false_positive_count += 1

            cnt_fp.append(false_positive_count)
            cnt_passes.append(hash_count)
            cnt_size.append(bit_arr_size)

            print('There are {} false positives when bit array size is {} and hash count is {}'
                .format(false_positive_count, bit_arr_size, hash_count))

    # plt.plot(cnt_passes, cnt_fp)   
    plt.plot(cnt_size, cnt_fp)
    plt.show() 

if __name__ == '__main__':
    main()


  