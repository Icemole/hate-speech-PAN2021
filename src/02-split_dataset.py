import argparse
import random


def split_dataset(filepath, eval_percent, dev_percent, shuffle=True, seed=123):
    random.seed(seed)
    with open(filepath, 'r') as f, open(f"{filepath.rsplit('.', 1)[0]}.train.{filepath.rsplit('.', 1)[1]}", 'w') as ftrain:
        feval = None
        if eval_percent > 0:
            feval = open(f"{filepath.rsplit('.', 1)[0]}.eval.{filepath.rsplit('.', 1)[1]}", 'w')
        fdev = None
        if dev_percent > 0:
            fdev = open(f"{filepath.rsplit('.', 1)[0]}.dev.{filepath.rsplit('.', 1)[1]}", 'w')

        nlines = len(f.readlines())
        f.seek(0)

        nlines_eval = int(nlines * eval_percent)
        nlines_dev = int(nlines * dev_percent)
        nlines_train = nlines - nlines_dev + nlines_eval

        if shuffle:
            for line in f.readlines():
                r = random.uniform(0, nlines) if shuffle else 0
                if r < nlines_eval:
                    feval.write(line)
                elif r <  nlines_dev + nlines_dev:
                    fdev.write(line)
                else:
                    ftrain.write(line)
        else:
            lines = f.readlines()

            feval.writelines(lines[0:nlines_eval])
            fdev.writelines(lines[nlines_dev: nlines_dev + nlines_eval])
            ftrain.writelines(lines[nlines_dev + nlines_eval:nlines_train + nlines_dev + nlines_eval])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='../data/tok/nonhaters_es.tok.txt',
                        help='Path to dataset, requires that said dataset is split in lines')
    parser.add_argument('--eval_percent', type=float, default='0.1',
                        help='Percentage of lines assigned to the evaluation set')
    parser.add_argument('--dev_percent', type=float, default='0.0',
                        help='Percentage of lines assigned to the development set')
    args = parser.parse_args()

    split_dataset(args.dataset, args.eval_percent, args.dev_percent, shuffle=True)


if __name__ == '__main__':
    main()