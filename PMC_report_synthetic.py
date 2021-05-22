
import warnings
warnings.filterwarnings("ignore")


import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def process_datafile(file_path, metric, metric_abbrev):
    ''' read a csv file and return df for plotting '''
    _df = pd.read_csv(file_path)

    _df.columns = ['Fairness Probabilty', metric]
    _df = _df.copy().sort_values(by=['Fairness Probabilty'], ascending=False)
    _df.reset_index(drop=True, inplace=True)    

    return _df

def plot_fairness_results_single_metric(df, metric, metric_abbrev,  dataset_name, x, y):

    # gca stands for 'get current axis'
    ax = plt.gca()

    df.plot(kind='line',x=x,y=y, ax=ax)

    out_file= os.path.join('.', 'PMCoutput', dataset_name + '_' + metric_abbrev + '.png')
    plt.savefig(out_file)


    return 


def plot_fairness(data):
    ''' plot fairness onto one png file '''

    metric = data.get('metric')
    file_path = data.get('file_path')
    metric_abbrev = data.get('metric_abbrev')
    y_col = str(data.get('p_plus')) + ' in protected group P+'
    df = process_datafile(file_path, metric, metric_abbrev)
    # change column name 
    print (df.columns.to_list())
    df.columns = ['Fairness Probabilty',y_col]

    plot_fairness_results_single_metric(df
                                        ,metric
                                        ,metric_abbrev
                                        ,dataset_name = 'synthetic_data'
                                        ,x = 'Fairness Probabilty'
                                        ,y = y_col)

 
    return


def get_file_dictionary():
    '''
    buildsa dict of the files and metrics associated wth them
    '''
    data=dict()

    # fairness metric name and abbrev
    metrics = [('Normalised Disc. k-L Divergence', 'rKL'),
               ('Normalised Disc. Difference','rND'),
               ('Normalised Disc. Ratio','rRD')]

    # total_poulation - n
    n=1000
    # protected class population
    p_plus =[200, 500, 800]

    i = 0
    # the data files - sources for plotting
    for m, ma in metrics:
        print(m , ma)
        for pp in p_plus:
            i = i+1
            key = str(i)
            name='synthetic_' + ma + '_1_user' + str(n) + '_pro' + str(pp) +'_data' + '.csv'
            file_path = os.path.join('.', 'PMCdata', name)
            item = {'metric' : m,'metric_abbrev' : ma, 'n' : n,
                    'p_plus' : pp, 'name' : name,'file_path' : file_path}
            data[key] = item
  
    print(f'added {i} items to the dictionary of data files')
    return data    

def plot_metrics(data, metrics):

    # loop through all metrics
    for m, ma in metrics:
        for key in data:
            if data[key]['metric_abbrev'] == ma:
                plot_fairness(data[key])     
        
        ax = plt.gca()
        ax.set_ylabel(m)
        plt.show()

    return


def main():

    
    metrics = [('Normalised Disc. k-L Divergence', 'rKL'),
               ('Normalised Disc. Difference','rND'),
               ('Normalised Disc. Ratio','rRD')]

    data = get_file_dictionary()

    # plot metrics
    plot_metrics(data, metrics)

    return




if __name__ == "__main__":

    '''
        process each file type
    '''
    main() 
