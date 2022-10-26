#!/usr/bin/env python

import bz2, zlib, pylzma
import string, random
import csv, math

def generate_string(size):
    letters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    return ''.join(random.choice(letters) for i in range(size))

if __name__ == '__main__':
    with open('compression_tests.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter=',')
        fieldnames = ['msg len',"",
                      'min len bz2', 'max len bz2', 'ave len bz2', 'min ratio bz2', 'max ratio bz2', 'ave ratio bz2', "",
                      'min len zlib', 'max len zlib', 'ave len zlib', 'min ratio zlib', 'max ratio zlib', 'ave ratio zlib', "",
                      'min len lzma', 'max len lzma', 'ave len lzma', 'min ratio lzma', 'max ratio lzma', 'ave ratio lzma']
        writer.writerow(fieldnames)
        
        for i in range(1000):
            print('here1'+str(i))
            bz2_total, zlib_total, lzma_total = 0, 0, 0
            bz2_min, zlib_min, lzma_min = 999999, 999999, 999999
            bz2_max, zlib_max, lzma_max = 0, 0, 0
            bz2_ratio_total, zlib_ratio_total, lzma_ratio_total = 0, 0, 0
            bz2_ratio_min, zlib_ratio_min, lzma_ratio_min = 999999, 999999, 999999
            bz2_ratio_max, zlib_ratio_max, lzma_ratio_max = 0, 0, 0
            for x in range(10):
                print('here2'+str(x))
                test_str = generate_string(i+1)
                bz2_str = bz2.compress(test_str)
                zlib_str = zlib.compress(test_str)
                lzma_str = pylzma.compress(test_str)
                
                #lengths of the compressed strings
                bz2_length = len(bz2_str)
                zlib_length = len(zlib_str)
                lzma_length = len(lzma_str)
                
                #compression ratios
                bz2_ratio = float(i)/float(bz2_length)
                zlib_ratio = float(i)/float(zlib_length)
                lzma_ratio = float(i)/float(lzma_length)
                
                #total length, used for calc ave length 
                bz2_total += bz2_length
                zlib_total += zlib_length
                lzma_total += lzma_length
                
                #total ratio, used for calc ave ratio
                bz2_ratio_total += bz2_ratio
                zlib_ratio_total += zlib_ratio
                lzma_ratio_total += lzma_ratio
                
                #update and store min/max lengths for each compression
                if bz2_length < bz2_min:
                    bz2_min = bz2_length
                if bz2_length > bz2_max:
                    bz2_max = bz2_length
                    
                if zlib_length < zlib_min:
                    zlib_min = zlib_length
                if zlib_length > zlib_max:
                    zlib_max = zlib_length
                    
                if lzma_length < lzma_min:
                    lzma_min = lzma_length
                if lzma_length > lzma_max:
                    lzma_max = lzma_length
                    
                #update and store min/max comprassion ratios
                if bz2_ratio < bz2_ratio_min:
                    bz2_ratio_min = bz2_ratio
                if bz2_ratio > bz2_ratio_max:
                    bz2_ratio_max = bz2_ratio
                    
                if zlib_ratio < zlib_ratio_min:
                    zlib_ratio_min = zlib_ratio
                if zlib_ratio > zlib_ratio_max:
                    zlib_ratio_max = zlib_ratio
                    
                if lzma_ratio < lzma_ratio_min:
                    lzma_ratio_min = lzma_ratio
                if lzma_ratio > lzma_ratio_max:
                    lzma_ratio_max = lzma_ratio
                    
            #ave lengths
            bz2_ave = float(bz2_total)/10
            zlib_ave = float(zlib_total)/10
            lzma_ave = float(lzma_total)/10
            
            #ave ratios
            bz2_ratio_ave = float(bz2_ratio_total)/10
            zlib_ratio_ave = float(zlib_ratio_total)/10
            lzma_ratio_ave = float(lzma_ratio_total)/10
            
            writer.writerow([i+1, "",
                             bz2_min, bz2_max, bz2_ave, bz2_ratio_min, bz2_ratio_max, bz2_ratio_ave, "",
                             zlib_min, zlib_max, zlib_ave, zlib_ratio_min, zlib_ratio_max, zlib_ratio_ave, "",
                             lzma_min, lzma_max, lzma_ave, lzma_ratio_min, lzma_ratio_max, lzma_ratio_ave])
    print('here')
            