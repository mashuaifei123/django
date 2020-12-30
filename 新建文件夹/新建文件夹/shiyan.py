import pandas as pd
from os import listdir
import re

in_path = r'K:\mashuaifei\20200314excel拆分\Fw_A2019027-T014-01健康检查个体数就和方案\A2019027-T014-01体温.xlsx'
huxi_M = pd.read_excel(in_path, skiprows=1, usecols='J:O')
print(huxi_M)