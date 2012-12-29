from nmf_q.recommend import NMF_Recommendation
import sys

rec = NMF_Recommendation(basis_path = "NMF_26872/p_NMF_Nimfa_NMF_Run_26872__metasites_all",
                         coef_path  = "NMF_26872/p_NMF_Nimfa_NMF_Run_26872__metasample_all",
                         query_path = sys.argv[1],
                         mask_path  = "data/dhsHG19.bed")

rec.load()
rec.run()
