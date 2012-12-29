from nmf_q.run import Nimfa_NMF_Run
import argparse

def parse():
    parser = argparse.ArgumentParser(description="ChIP-seq Classification and Dimension Reduction with NMF")
    parser.add_argument('-b', '--beds-table', dest='beds_table',required=True)
    parser.add_argument('-m', '--mask', dest='mask_path',required=True)
    parser.add_argument('-n', '--process-name', dest='process_name',default="nmf_process")
    parser.add_argument('-r', '--rank', dest='nmf_rank',default=10, type=int)
    parser.add_argument('--max-iter', dest='max_iter',default=100,type=int)
    parser.add_argument('--debug', dest='debug_mode',action="store_true")
    parser.add_argument('--dump-masked', dest='dump_masked_mode',action="store_true")
    parser.add_argument('--load-masked', dest='load_masked_path', default="")
    parser.add_argument('--dump-nmf', dest='dump_nmf_mode',action="store_true")
    parser.add_argument('--load-nmf', dest='load_nmf_path', default="")
    return parser.parse_args()

def main():
    args = parse()
    # Lazy import as importing nimfa is slow
    nmf_run = Nimfa_NMF_Run(**vars(args))
    try:
        nmf_run.run()
    finally:
        if not args.debug_mode:
            nmf_run.clean()
    nmf_run.persist()
    return nmf_run

if __name__ == '__main__':
    nmf_run = main()
