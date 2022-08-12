from enum import Enum
import subprocess
from typing import List, TypedDict

DEVICE = 'dev eth0'

def run(cmd: str) -> str:
    result = subprocess.run(
        cmd.split(' '), 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        error = result.stderr.decode().strip()
        raise Exception(f'Error when running command `{cmd}`:\n{error}')
    return result.stdout.decode().strip()

class Prio(Enum):
    HIGH = 6 # band 0
    DEFAULT = 0 # band 1
    LOW = 2 # band 2

class PrioInfo(TypedDict):
    port: int
    prio: Prio

def qos(port_infos: List[PrioInfo]):
    # delete previous qdisc if exist
    # this will also remove relevant filters
    qdisc = run(f'tc qdisc list {DEVICE}')
    PRIOMAP = '1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1' # the default one
    if f'qdisc prio 1: root refcnt 6 bands 3 priomap {PRIOMAP}' in qdisc:
        run(f'tc qdisc delete {DEVICE} root handle 1: prio bands 3 priomap {PRIOMAP}')
    # add a new one
    run(f'tc qdisc add {DEVICE} root handle 1: prio bands 3 priomap {PRIOMAP}')

    # add filters
    for port_info in port_infos:
        PROTOCOL = 'protocol ip'
        PARENT = 'parent 1:'
        PRIO = f'prio {port_info["prio"].value}'
        MATCH = f'u32 match ip dport {port_info["port"]} 0xffff'
        FLOW = 'flowid 1:1'
        # is flowid necessary???
        # run(f'tc filter add {DEVICE} {PROTOCOL} {PARENT} {PRIO} {MATCH} {FLOW}')
        run(f'tc filter add {DEVICE} {PROTOCOL} {PARENT} {PRIO} {MATCH}')

