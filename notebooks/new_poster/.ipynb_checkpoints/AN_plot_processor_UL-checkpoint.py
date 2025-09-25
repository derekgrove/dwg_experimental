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

# print(src_dir)

from analysis_tools.taggers.lep_tagger_UL import *
from analysis_tools.taggers.gen_tagger import *

from analysis_tools.default_analysis import lep_analysis_dict, lpte_analysis_dict


class Processor(processor.ProcessorABC):
    def __init__(self):
        self.schema = BaseSchema

    def process(self, events):

        electron = events.Electron
        lowptelectron = events.LowPtElectron
        muon = events.Muon

        ele = tag_and_combine_ele(electron, lowptelectron)
        muon = tag_muon(muon)

        ele_dict = lep_analysis_dict(ele)
        muon_dict = lep_analysis_dict(muon)

        lpte = tag_lpte(lowptelectron)
        lpte_dict = lpte_analysis_dict(lpte)
        
        
        output = {
            "total_entries": ak.num(events[events.run >= 0], axis=0),
            
            "ele_dict": ele_dict,
            "muon_dict": muon_dict,
            "lpte_dict": lpte_dict,
            
        }

            
        return output

    def postprocess(self, accumulator):
        pass
