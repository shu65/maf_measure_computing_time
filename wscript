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
    
def min(key):
    """Creates an aggregator to select the minimum value of given key.

    The created aggregator chooses the result with the minimum value of
    ``key``, and writes the JSON object to the output node.

    :param key: A key to be used for selection of minimum value.
    :type key: ``str``
    :return: An aggregator.
    :rtype: :py:class:`maflib.core.Rule`

    """
    @maflib.util.json_aggregator
    def body(values, outpath, parameter):
        if len(values) == 0:
            return json.dumps({})

        min_value = values[0][key]
        argmin = values[0]
        for value in values[1:]:
            if min_value > value[key]:
                min_value = value[key]
                argmin = value
        return argmin

    return maflib.core.Rule(fun=body, dependson=[min, key])


def average(key):
    
    @maflib.util.json_aggregator
    def body(values, outpath, parameter):
        if len(values) == 0:
            return json.dumps({})

        sum = 0
        for value in values[0:]:
            sum = sum + value[key]

        return sum / len(values)

    return maflib.core.Rule(fun=body, dependson=[average, key])

class Task(object):
    def __init__(self, name, rule, parameter):
        self.name = name
        self.rule = rule
        self.parameter = parameter

def execute_sequential(exp, tasks):
    source = ""
    for i in range(len(tasks)) :
        task = tasks[i]
        exp(source=source, target=task.name,
            parameters=[task.parameter],
            for_each=[],
            rule=task.rule)
        source = task.name


def options(opt):
    opt.load('maf')

def configure(conf):
    conf.load('maf')

def experiment(exp):

    parameters = maflib.util.product({'A': [0, 1, 2],
                                    'B': range(3)})
    tasks = []
    for i in range(len(parameters)):
        name = "task." + str(i)
        parameter = parameters[i]
        rule = 'time -p sleep ${A} 2> ${TGT}'
        tasks.append(Task(name, rule, parameter))

    execute_sequential(exp, tasks)
    
    task_names = [task.name for task in tasks]
    # Parse the output message and extract the real time.
    
    task_names_str = " ".join(task_names)
    exp(source=task_names_str,
        target='computing_time',
        rule=extract_computing_time)
    
    exp(source='computing_time',
        target='average_computing_time',
        aggregate_by='B',
        rule=average('computing_time'))

    
