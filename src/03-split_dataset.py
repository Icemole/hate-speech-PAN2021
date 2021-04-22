import argparse
import random


def split_dataset(filepath, eval_percent, dev_percent, extract_to, shuffle=True, seed=123):
    random.seed(seed)
    filename = filepath.rstrip("/").split("/")[-1]
    extract_to += "/"
    
    with open(filepath, 'r') as f, open(extract_to + f"{filename.rsplit('.', 1)[0]}.train.{filename.rsplit('.', 1)[1]}", 'w') as ftrain:
        feval = None
        if eval_percent > 0:
            feval = open(extract_to + f"{filename.rsplit('.', 1)[0]}.eval.{filename.rsplit('.', 1)[1]}", 'w')
        fdev = None
        if dev_percent > 0:
            fdev = open(extract_to + f"{filename.rsplit('.', 1)[0]}.dev.{filename.rsplit('.', 1)[1]}", 'w')

        nlines = len(f.readlines())
        f.seek(0)

        nlines_eval = int(nlines * eval_percent)
        nlines_dev = int(nlines * dev_percent)
        nlines_train = nlines - nlines_dev - nlines_eval

        if shuffle:
            for line in f.readlines():
                r = random.uniform(0, nlines) if shuffle else 0
                if r < nlines_eval:
                    feval.write(line)
                elif r < nlines_eval + nlines_dev:
                    fdev.write(line)
                else:
                    ftrain.write(line)
        else:
            lines = f.readlines()

            feval.writelines(lines[0:nlines_eval])
            fdev.writelines(lines[nlines_dev: nlines_dev + nlines_eval])
            ftrain.writelines(lines[nlines_dev + nlines_eval:nlines_train + nlines_dev + nlines_eval])
        
        if fdev is not None:
            fdev.close()
        if feval is not None:
            feval.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='../data/tok/nonhaters_es.tok.txt',
                        help='Path to dataset, requires that said dataset is split in lines')
    parser.add_argument('--eval_percent', type=float, default='0.1',
                        help='Percentage of lines assigned to the evaluation set')
    parser.add_argument('--dev_percent', type=float, default='0.0',
                        help='Percentage of lines assigned to the development set')
    parser.add_argument('--extract_to', default='data/tok/partitioned_data',
                        help='Path where to extract the split data')
    args = parser.parse_args()
    
    split_dataset(args.dataset, args.eval_percent, args.dev_percent, args.extract_to, shuffle=True)


if __name__ == '__main__':
    main()