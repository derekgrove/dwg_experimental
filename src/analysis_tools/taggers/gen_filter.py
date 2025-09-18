# Parent filter for our signal samples

# We are concerned with primary electrons, so:
# Only allows W's, Z's, and sleptons through

import awkward as ak
import numpy as np


###########################################################################
# Gen Parent Filtering here


def WZ_mask(obj):
    # obj could be events.Electron, events.LowPtElectron, or events.Muon

    is_W = (abs(obj.matched_gen.distinctParent.pdgId) == 24)
    is_W_clean = ak.fill_none(is_W, False)
    
    is_Z = (obj.matched_gen.distinctParent.pdgId == 23)
    is_Z_clean = ak.fill_none(is_Z, False)

    all_filters = (is_W_clean | is_Z_clean)

    return all_filters #returns a boolean mask



def susy_mask(obj):
    # obj could be events.Electron or events.LowPtElectron

    is_sel = ((obj.matched_gen.distinctParent.pdgId == 1000011) | 
              (obj.matched_gen.distinctParent.pdgId == 2000011))
    is_sel_clean = ak.fill_none(is_sel, False)

    is_smu = ((obj.matched_gen.distinctParent.pdgId == 1000013) | 
              (obj.matched_gen.distinctParent.pdgId == 2000013))
    is_smu_clean = ak.fill_none(is_smu, False)

    is_LSP = (obj.matched_gen.distinctParent.pdgId == 1000022)
    is_LSP_clean = ak.fill_none(is_LSP, False)

    is_sLSP = (obj.matched_gen.distinctParent.pdgId == 1000023)
    is_sLSP_clean = ak.fill_none(is_sLSP, False)

    is_LCG = (abs(obj.matched_gen.distinctParent.pdgId) == 1000024)
    is_LCG_clean = ak.fill_none(is_LCG, False)

    all_filters = (is_sel_clean | is_smu_clean | is_LSP_clean | is_sLSP_clean | is_LCG_clean)

    return all_filters #returns a boolean mask



def parent_mask(obj):
    
    mask = WZ_mask(obj) | susy_mask(obj)

    return mask



###########################################################################
# Gen kinematic masks here


def ele_gen_mask(ele_obj):
    
    mask = ((ele_obj.matched_gen.pt > 4.5) & (np.abs(ele_obj.matched_gen.eta) < 3))
    mask_clean = ak.fill_none(mask, False)
    
    return mask_clean

    

def muon_gen_mask(muon_obj):
    
    mask = ((muon_obj.matched_gen.pt > 2.5) & (np.abs(muon_obj.matched_gen.eta) < 3))
    mask_clean = ak.fill_none(mask, False)
    
    return mask_clean

    

def lpte_gen_mask(lpte_obj):

    mask = ((lpte_obj.matched_gen.pt > 0.5) & (np.abs(lpte_obj.matched_gen.eta) < 3))
    mask_clean = ak.fill_none(mask, False)
    
    return mask_clean
    
