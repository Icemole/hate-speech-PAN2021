All pre-trained models are taken from the simpletransformers Python library, which itsself is derived from Huggingface's transformers framework.
The main model types available that are of interest for this task are:

- **BERT**: Good baseline performance

- **RoBERTa**: Heaviest model but highest performance in benchmark (e.g. GLUE benchmark results)

- **DistilBERT**: 97% performance of BERT but half the parameters, notable faster inference when compared to RoBERTa

- **BERTweet**: The first public large-scale language model pre-trained for English Tweets. BERTweet is trained based on the RoBERTa pre-training procedure, using the same model configuration as BERT-base.
The corpus used to pre-train BERTweet consists of 850M English Tweets (16B word tokens ~ 80GB), containing 845M Tweets streamed from 01/2012 to 08/2019 and 5M Tweets related to the COVID-19 pandemic.
BERTweet does better than its competitors RoBERTa-base and XLM-R-base and outperforms previous state-of-the-art models on three downstream Tweet NLP tasks of Part-of-speech tagging, Named entity recognition and text classification.