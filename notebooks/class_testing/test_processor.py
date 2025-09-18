import awkward as ak
from coffea import processor
from coffea.nanoevents import BaseSchema
import hist.dask as dah  # use eager version unless you're doing distributed work
import json
import sys
from pathlib import Path


current_dir = Path.cwd()

src_dir = current_dir.parent.parent / "src"
sys.path.append(str(src_dir))

print(src_dir)

from analysis_tools.taggers.lep_tagger import *
from analysis_tools.taggers.gen_tagger import *

from analysis_tools.default_analysis import default_analysis, analysis_dict


class Processor(processor.ProcessorABC):
    def __init__(self):
        self.schema = BaseSchema

    def process(self, events):

        gens = [-10, 10, 11, 12, 13]
        quals = [-1,0,1,2,3]

        electron = events.Electron
        
        #def_analysis = default_analysis(name="test", pt=electron.pt)
        #def_analysis = default_analysis(name="test")

        #test_pt = def_analysis.pt

        #test_dict = analysis_dict(electron, 'ele')

        #(obj, reg_binning, cat_binning, var_name = "pt", cat_name="genPartFlav"):
        
        output = {
            "total_entries": ak.num(events[events.run >= 0], axis=0),
            #"def_analysis": def_analysis,
            #"test_pt": test_pt,
            #"test_dict": test_dict,
            
        }

            
        return output

    def postprocess(self, accumulator):
        pass




