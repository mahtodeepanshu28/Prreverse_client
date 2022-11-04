import copy
from typing import List
import re
import csv
import subprocess
import os
import json
from pylint.lint import Run
import urllib
import sys
from models.module_metrics import CommitLog
from generate_metrics import Repo
from datastore.pg_store import PgDataStore



class PyReverseClient:

    def __init__(self):
        self.pkg_fan_in = {}
        self.pkg_fan_out = {}

    def get_coupling(self, dot_path):

        # sample DOT line format:    "2468" -> "2389" [arrowhead="open", arrowtail="none"];
        # module 2468 has dependency (is coupled to) module 2389
        coupling_line_pattern = r'^\"([0-9]+)\"\s->\s\"([0-9]+)\".*$'

        dot_file = open(dot_path)

        for line in dot_file:
            if '->' in line:
                coupling_line = re.search(coupling_line_pattern, line)
                if coupling_line:
                    module_src, module_dst = coupling_line.group(1).strip(), coupling_line.group(2).strip()

                    print('module {} is dependent on {}'.format(module_src, module_dst))

                    # keep track of number of fan in/out (dependecny) per module
                    fan_out = self.pkg_fan_out.get(module_src, 0)
                    self.pkg_fan_out.update({module_src: fan_out + 1})

                    fan_in = self.pkg_fan_in.get(module_dst, 0)
                    self.pkg_fan_in.update({module_dst: fan_in + 1})

        # using fan_in as coupding metric.
        for k, v in self.pkg_fan_in.items():
            print(v)

if __name__ == '__main__':
    # Sample dot file for two projects, ERPNEXT and SEALOR
    ERP_NEXT_DOT='/home/omari/curated-python-projects/erpnext/packages_erpnext.dot'
    SALEOR_DOT = '/home/omari/curated-python-projects/saleor/packages_saleor.dot'

    # Create a client object.
    pyreverse_client = PyReverseClient()
    # print out coupling for all modules.
    pyreverse_client.get_coupling(dot_path=ERP_NEXT_DOT)
