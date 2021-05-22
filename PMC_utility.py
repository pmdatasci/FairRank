
# Usage of runRealDataExp
from runRealDataExp import *




def main(data_folder,output_fn,sensi_att):

    print("Finished experiments on real data sets")
    print("Result stores in "+ output_fn+".csv")

    # Finishing computation of data: ProPublica_race
    # Finishing computation of data: ProPublica_sex
    # Finishing computation of data: GermanCredit_sex
    # Finishing computation of data: GermanCredit_age25
    # Finishing computation of data: GermanCredit_age35
    # Finished experiments on real data sets
    # Result stores in Fairness_real_data.csv



if __name__ == "__main__":
    
    # Initialization
    # Step 1: Specify a folder that includes all the source csv file of real data sets
    data_folder = 'datasets'
    
    # Step 2: Specify which value of sentitive attribute represents the protected group
    sensi_att = 1

    # Step 3: Specify the file to output experiment results
    output_fn = "Fairness_real_data"

    main(data_folder,output_fn,sensi_att)
