from nmf_q.run import Nimfa_NMF_Run, Pymf_NMF_Run
import argparse

def parse():
    parser = argparse.ArgumentParser(description="ChIP-seq Classification and Dimension Reduction with NMF")
    parser.add_argument('-b', '--beds-table', dest='beds_table',required=True)
    parser.add_argument('-m', '--mask', dest='mask_path',required=True)
    parser.add_argument('-t', '--nmf-tool', dest='nmf_tool',default="pymf")
    parser.add_argument('-n', '--process-name', dest='process_name',default="nmf_process")
    parser.add_argument('--debug', dest='debug_mode',action="store_true")

    return parser.parse_args()

def main():
    args = parse()
    tools = {"nimfa" : Nimfa_NMF_Run,
             "pymf"  : Pymf_NMF_Run}

    # Lazy import as importing nimfa is slow
    nmf_run = (tools[args.nmf_tool])(**vars(args))
    try:
        nmf_run.run()
    finally:
        if not args.debug_mode:
            nmf_run.clean()
    nmf_run.output_metasites()
    return nmf_run

if __name__ == '__main__':
    nmf_run = main()
