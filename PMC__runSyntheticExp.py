from __future__ import division
import dataGenerator
import measures

import pandas as pd
import os

# a python script to compute fairness measures of synthetic data 
# can be run through command line by using command: runSyntheticExp user_N pro_N gf_measure cut_point output_fn
# user_N, pro_N are the size of input population and protected group
# gf_measure is choosed from ["rKL", "rND", "rRD"]
# cut_point is the cut rank position to compute the split fairness measure
# output_fn represents the output file name
# test of this script can be found in testSyntheticExp.py

KL_DIVERGENCE="rKL" # represent kl-divergence group fairness measure
ND_DIFFERENCE="rND" # represent normalized difference group fairness measure
RD_DIFFERENCE="rRD" # represent ratio difference group fairness measure
NORM_ITERATION=1000 # max iterations used in normalizer computation





def main(_user_N,_pro_N,_gfmeasure,_cut_point,_rez_fn, _loops):
    """
        Run the group fairness experiments of synthetic unfair rankings.
        Output group fairness results as csv file.        
        
        :param _user_N: The total user number of input ranking
        :param _pro_N: The size of protected group in the input ranking        
        :param _gfmeassure: The group fairness measure to be used in calculation 
                            one of "rKL", "rND" and "rRD" defined as constant in this py file 
        :param _cut_point: The cut off point of set-wise group fairness calculation               
        :param _rez_fn: The file name to output group fairness results
        
        :return: no returns.
    """

    # define the input mixing proportion
    f_probs=[i/10 for i in range(10)] 
    f_probs.append(0.98) #using 0.98 as extreme case considering the limitation of random generator
    
    # define the output dictionary
    keys = []
    values = []

    #define output file name (fn)
    base_file_name =_rez_fn+"_user"+str(_user_N)+"_pro"+str(_pro_N)
    # output_fn = os.path.join('~', 'RMIT','RMITRepo','FairRank', 'datasets', base_file_name)
    output_fn = base_file_name + ".csv"

    with open(output_fn,'w') as mf:
        mf.write("GF_Measure,MP0.0,MP0.1,MP0.2,MP0.3,MP0.4,MP0.5,MP0.6,MP0.7,MP0.8,MP0.9,MP0.98\n")        
    rez_file=open(output_fn, 'a')
    # calculate the normalizer of the input user number and protected group
    max_GF=measures.getNormalizer(_user_N,_pro_N,_gfmeasure) 
    # generate a random input ranking and protected group
    input_ranking=[x for x in range(_user_N)]
    sensi_idx=[x for x in range(_pro_N)]
    
    for i in range(_loops):
        gf_results=[] 
        # loop the input fairness probabilities
        for fpi in range(len(f_probs)): 
            fp=f_probs[fpi]
            gf_iters=0 
            for iteri in range(1,NORM_ITERATION+1):
                sRFair=dataGenerator.generateUnfairRanking(input_ranking,sensi_idx,fp)                   
                gf=measures.calculateNDFairness(sRFair,sensi_idx,_cut_point,_gfmeasure,max_GF) 
                gf_iters=gf_iters+gf 
            gf_results.append(gf_iters/NORM_ITERATION) #record average result
            
            # append the key/value to lists for creation of data csv 
            keys.append(fp)
            values.append(gf_iters/NORM_ITERATION)
    
            # print( "Finished mixing proportion ",fp)

        # output results into csv file    
        fline=_gfmeasure + ","
        for item in gf_results:
            fline=fline+str(item)+","
        rez_file.write(fline+"\n")

    data = list(zip(keys, values))
    df = pd.DataFrame(data, columns=['prob', 'measure'])

    rez_file.close()

    data_file = os.path.join('.', 'PMCdata',  base_file_name +'_data' + '.csv')
    df.to_csv(data_file, index=False)

    return 


if __name__ == "__main__":
    # main()
    loops = 1
    main(1000,200,'rND',10,'synthetic_rND_'+str(loops), loops)
    main(1000,500,'rND',10,'synthetic_rND_'+str(loops), loops)
    main(1000,800,'rND',10,'synthetic_rND_'+str(loops), loops)
    main(1000,200,'rKL',10,'synthetic_rKL_'+str(loops), loops)
    main(1000,500,'rKL',10,'synthetic_rKL_'+str(loops), loops)
    main(1000,800,'rKL',10,'synthetic_rKL_'+str(loops), loops)
    main(1000,200,'rRD',10,'synthetic_rRD_'+str(loops), loops)
    main(1000,500,'rRD',10,'synthetic_rRD_'+str(loops), loops)
    main(1000,800,'rRD',10,'synthetic_rRD_'+str(loops), loops)

