import argparse
import random


def split_dataset(filepath, eval_proportion, dev_proportion, extract_to, grouped, shuffle=True, block_size=200, seed=123):
    random.seed(seed)
    filename = filepath.rstrip("/").split("/")[-1]
    if grouped:
        filename_train = f"{filename.rsplit('.', 1)[0]}_grouped.train.{filename.rsplit('.', 1)[1]}"
        filename_dev = f"{filename.rsplit('.', 1)[0]}_grouped.dev.{filename.rsplit('.', 1)[1]}"
        filename_eval = f"{filename.rsplit('.', 1)[0]}_grouped.eval.{filename.rsplit('.', 1)[1]}"
    else:
        filename_train = f"{filename.rsplit('.', 1)[0]}.train.{filename.rsplit('.', 1)[1]}"
        filename_dev = f"{filename.rsplit('.', 1)[0]}.dev.{filename.rsplit('.', 1)[1]}"
        filename_eval = f"{filename.rsplit('.', 1)[0]}.eval.{filename.rsplit('.', 1)[1]}"
    extract_to += "/"
    
    with open(filepath, 'r') as f, open(extract_to + filename_train, 'w') as ftrain:
        feval = None
        if eval_proportion > 0:
            feval = open(extract_to + filename_eval, 'w')
        fdev = None
        if dev_proportion > 0:
            fdev = open(extract_to + filename_dev, 'w')

        nlines = len(f.readlines())
        f.seek(0)

        nlines_eval = int(nlines * eval_proportion)
        nlines_dev = int(nlines * dev_proportion)
        nlines_train = nlines - nlines_dev - nlines_eval

        lines = f.readlines()

        if shuffle:
            # We want to preserve author order: 200 tweets per author
            blocks = [lines[i:i+block_size] for i in range(0, len(lines), block_size)]
            for block in blocks:
                # Shuffle inside an author
                random.shuffle(block)
            # Shuffle all authors
            random.shuffle(blocks)
            lines[:] = [sent for block in blocks for sent in block]
        
        if grouped:
            # An author is already a block as defined by this code
            nlines_eval = int(nlines_eval / block_size)
            nlines_dev = int(nlines_dev / block_size)
            nlines_train = int(nlines_train / block_size)

            blocks = [lines[i:i+block_size] for i in range(0, len(lines), block_size)]
            lines = [" ".join([sent.strip("\n") for sent in block]) + "\n" for block in blocks]
        
        feval.writelines(lines[0:nlines_eval])
        fdev.writelines(lines[nlines_eval: nlines_eval + nlines_dev])
        ftrain.writelines(lines[nlines_dev + nlines_eval:nlines_train + nlines_dev + nlines_eval])
        
        if fdev is not None:
            fdev.close()
        if feval is not None:
            feval.close()


def main():
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='../data/tok/nonhaters_es.tok.txt',
                        help='Path to dataset, requires that said dataset is split in lines')
    parser.add_argument('--eval_proportion', type=float, default='0.1',
                        help='Percentage of lines assigned to the evaluation set')
    parser.add_argument('--dev_proportion', type=float, default='0.0',
                        help='Percentage of lines assigned to the development set')
    parser.add_argument('--extract_to', default='data/tok/partitioned_data',
                        help='Path where to extract the split data')
    parser.add_argument('--grouped', type=str2bool, nargs='?', const=True, default=False,
                        help='One line will contain all tweets for an specific author')
    args = parser.parse_args()
    
    split_dataset(args.dataset, args.eval_proportion, args.dev_proportion, args.extract_to, args.grouped, shuffle=True)


if __name__ == '__main__':
    main()