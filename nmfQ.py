import argparse

def parse():
    parser = argparse.ArgumentParser(description="ChIP-seq Classification and Dimension Reduction with NMF")
    parser.add_argument('-b', '--beds-table', dest='beds_table',required=True)
    parser.add_argument('-m', '--mask', dest='mask_path',required=True)
    return parser.parse_args()

def main():
    args = parse()

    from nmf_q.run import NMF_Run
    # Lazy import as importing nimfa is slow

    nmf_run = NMF_Run(args.beds_table, args.mask_path)

if __name__ == '__main__':
    main()
