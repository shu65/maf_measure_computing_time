import maf
import maflib.plot
import maflib.rules
import maflib.util

import json

def extract_computing_time(task):
    lines = task.inputs[0].read().split('\n')
    real_line = lines[-4]
    j = {'computing_time': float(real_line.split(' ')[1][:-1])}
    task.outputs[0].write(json.dumps(j))
    

def average_value(key):
    
    @maflib.util.json_aggregator
    def body(values, outpath, parameter):
        if len(values) == 0:
            return json.dumps({})

        sum_value = 0
        for value in values[0:]:
            sum_value = sum_value + value[key]

        return sum_value / len(values)

    return maflib.core.Rule(fun=body, dependson=[average_value, key])


def options(opt):
    opt.load('maf')

def configure(conf):
    conf.load('maf')

def experiment(exp):

    parameters = maflib.util.product({'T': [0, 1, 2], 'ExecutionCount':range(3)})
    
    exp(target='raw_time_output',
            parameters=parameters,
            rule='time -p sleep ${T} 2> ${TGT}')

    exp(source='raw_time_output',
        target='computing_time',
        rule=extract_computing_time)
    
    exp(source='computing_time',
        target='average_computing_time',
        aggregate_by='ExecutionCount',
        rule=average_value('computing_time'))

    
