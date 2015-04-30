#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on 30 Apr., 2015

RECON: A Reciprocal Recommender for Online Dating.(Recsys'10)

@author: ochi
'''

import json
import numpy as np

def run():
    userprofile = getJsonFile("sample-profile.json")
    userpreference = getJsonFile("sample-preference.json")
    communicationHistory = getJsonFile("sample-communication-history.json")

    def findPreference(x):
        P_x = userpreference[x]
        return P_x

    def calcurate_compatibility(P_x, y):
        U_y = userprofile[y]
        attrs = U_y.keys()
        scores = []
        for a in attrs:
            v_a = U_y[a]
            if a == "age":
                for agekey in P_x[a].keys():
                    ages = agekey.split('-')
                    min_age = int(ages[0])
                    max_age = int(ages[1])
                    if v_a >= min_age and v_a <= max_age:
                        p_x_a = P_x[a][agekey]
                        break
                    else:
                        continue
            else:
                p_x_a = P_x[a][v_a]
            n = sum(P_x[a].values())
            s_a = float(p_x_a) / float(n)
            if s_a == 0:
                compatibility = 0
                return compatibility
            else:
                scores.append(s_a)
        compatibility = np.average(scores)
        return compatibility

    def reciprocalRecommender(x, N=3):
        P_x = findPreference(x)
        R = findAllUsersNotMessagedBy(x)
        print "user %s"%(x)
        S = []
        for y in R:
            s_y = calcurate_compatibility(P_x, y)
            print "compatible score %s is %.3f"%(y,s_y)
            if s_y > 0:
                P_y = findPreference(y)
                s_x = calcurate_compatibility(P_y,x)
                if s_x == 0:
                    s_y = 0
                else:
                    s_y = 2.0/(s_y**(-1)+s_x**(-1))
            S.append(s_y)
        sorted_indices = [ i[0] for i in sorted(enumerate(S), key=lambda x:-x[1]) ]
       
        newR = []
        newS = []
        for idx in sorted_indices[0:N]:
            newR.append(R[idx])
            newS.append(S[idx])
        return newR,newS

    def findAllUsersNotMessagedBy(x):
        R = []
        for user in communicationHistory[x].keys():
            if communicationHistory[x][user] is False:
                R.append(user)
            else:
                continue
        return R

    users = sorted(userprofile.keys())
    for u in users:
        R,S = reciprocalRecommender(u, N=3)
        print "recommend for %s"%(u)
        for i, y in enumerate(R):
            print "reciprocal score %s is %.3f"%(y,S[i])

def getJsonFile(jsonfile):
    f = open(jsonfile, 'r')
    obj = json.load(f)
    f.close()
    return obj


if __name__ == "__main__":
    run()
