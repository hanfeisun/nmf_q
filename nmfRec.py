from nmf_q.recommend import NMF_Recommendation, NMF_Recommendation_Set
import argparse
def parse():
    parser = argparse.ArgumentParser(description="ChIP-seq Classification and Dimension Reduction with NMF")
    parser.add_argument('-b', dest='basis_path',required=True)
    parser.add_argument('-c', dest='coef_path',required=True)
    parser.add_argument('-m', dest='mask_path',default="data/dhsHG19.bed")
    parser.add_argument('-q', dest='query_path',required=True)
    parser.add_argument('--qset', dest='qset',action='store_true')
    return parser.parse_args()

def main():
    args = parse()
    if args.qset:
        from scipy.spatial.distance import cosine,correlation
        rec = NMF_Recommendation_Set(basis_path = args.basis_path,
                                     coef_path  = args.coef_path,
                                     mask_path  = args.mask_path)
        print rec.query_set(querys_table = args.query_path,
                            similar_func = cosine)
        print rec.query_set(querys_table = args.query_path,
                            similar_func = correlation)

    else:
        rec = NMF_Recommendation(basis_path = args.basis_path,
                                 coef_path  = args.coef_path,
                                 mask_path  = args.mask_path)
        rec.query(query_path = args.query_path)

if __name__ == '__main__':
    main()
