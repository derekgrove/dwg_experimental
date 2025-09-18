import numpy
import awkward as ak
import sys
import hist.dask as dah
from pathlib import Path

current_dir = Path.cwd()

#taggers = current_dir.parent / 'taggers'

from .plotting.histers import *
#from ../taggers.lep_tagger import *
from .taggers.lep_tagger import *
from .taggers.gen_tagger import *

class default_analysis:

    def __init__(self, name, hist=None):
        
        self.name = name
        self.hist = hist or (
        dah.Hist.new
        .Regular(500, 0, 500, name="pt") #500 (1 GeV) bins between 0 and 500
        .Double()
        )
        #self.pt = pt
        #self.pt = getattr(self, 'pt')
        
    
def tag_and_combine_ele(electron, lowptelectron):
    
    tagged_ele = tag_qual(tag_gen(electron, 'ele'), 'ele')
    tagged_lpte = tag_qual(tag_gen(lowptelectron, 'lpte'), 'lpte')

    pt_selected_electron = tagged_ele[tagged_ele.pt >= 7]
    pt_selected_lpte = tagged_lpte[tagged_lpte.pt < 7]

    ele = ak.concatenate([pt_selected_electron, pt_selected_lpte], axis=1)

    return ele


def tag_muon(muon):
    
    return tag_qual(tag_gen(muon, 'muon'), 'muon')
    

def analysis_dict(obj):
    
    """
    structure will be a dict with lots of hists of various configurations
    """
    
    ##############
    # fill hists #
    #############

    gens = [-10, 10, 11, 12, 13] #I added 1 in front for gens so I know I don't accidentally get it mixed up with qual
    quals = [-1,0,1,2,3]
    
    pt_eta_hist = make_2d2d_hist_cat(
        obj,                           
        [2,3,4,5,7,10,20,45,75,1000], 
        [0,0.8,1.442,1.556,2.5],
        cat1_binning = gens,
        cat2_binning = quals,
        var1_name = 'pt',
        var2_name = 'eta',
        cat1_name='gen_tag',
        cat2_name='qual_tag',
        var2_abs=True
       )

    pt_AN_v1 = make_1d2d_hist_reg_cat(
    obj,
    [40,0,100], #like [100, 0, 100] 100 bins between 0 and 100
    cat1_binning = gens,
    cat2_binning = quals,
    var_name="pt",
    cat1_name="gen_tag",
    cat2_name="qual_tag",
    var_abs=False,
    )

    pt_bins = [2,3,4,5,7,10,12.5,15.0,17.5,20.0,
               22.5,25.0,27.5,30.0,32.5,35.0,
               37.5,40.0,42.5,45.0,47.5,50.0,
               52.5,55.0,57.5,60.0,62.5,65.0,
               67.5,70.0,72.5,75.0,77.5,80.0,
               82.5,85.0,87.5,90.0,92.5,95.0,
               97.5,100.0]
    
    pt_AN_v2 = make_1d2d_hist_var_cat(
    obj,
    pt_bins, 
    cat1_binning = gens,
    cat2_binning = quals,
    var_name="pt",
    cat1_name="gen_tag",
    cat2_name="qual_tag",
    var_abs=False,
    )

# (obj, var_binning, cat_binning, var_name = "pt", cat_name="genPartFlav")

    ################
    # fill results #
    ###############

    results = {
        "pt_eta_hist": pt_eta_hist,
        "pt_AN_hist_v1": pt_AN_v1,
        "pt_AN_hist_v2": pt_AN_v2,
    }

    return results





def analysis_dict_old(obj, ID=None): #pushed this here, problem is "how do I combine electrons and lowpt electrons inside? maybe another function defined above that can tag and combine them but then I add a boolean flag in here to call that function for me
    
    """
    structure will be a dict with lots of hists of various configurations
    """

    acceptable_IDs = [
        'ele', 'electron',
        'lpte', 'lowptelectron',
        'mu', 'muon'] #more can be added, maybe jets and whatever if needed

    ############
    # taggers #
    ###########
    
    if ID.lower() not in acceptable_IDs:
        
        sys.exit(f'ID {ID} not acceptable, must be in {acceptable_IDs}')
    
    else:
        tagged_obj = tag_qual(tag_gen(obj, ID), ID)

    #now lep has these flags: qual_tag and gen_tag
    
    #qual_tag = [-1,0,1,2,3]
    #where -1 fails baseline, 0 is baseline, 1 is bronze, 2 silver, 3 gold
    
    #gen_tag = [-10, 10, 11, 12, 13]
    # where -10 is other gen, 10 signal, 11 is light fake, 12 is heavy decay, 13 tau decay
    
    ##############
    # fill hists #
    #############

    gens = [-10, 10, 11, 12, 13] #I added 1 in front for gens so I know I don't accidentally get it mixed up with qual
    quals = [-1,0,1,2,3]
    
    pt_eta_hist = get_2d2d_hist_cat(
        obj,                           
        [2,3,4,5,7,10,20,45,75,1000], 
        [0,0.8,1.442,1.556,2.5],
        cat1_binning = gens,
        cat2_binning = quals,
        var1_name = 'pt',
        var2_name = 'eta',
        cat1_name='gen_tag',
        cat2_name='qual_tag',
        var2_abs=True
       )

    ################
    # fill results #
    ###############

    results = {
        "pt_eta_hist": pt_eta_hist,
    }

    return results



        

    