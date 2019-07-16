# Tokenizer

This tool provides several methods for de/tokenizing a sentence using:

* [Moses tokenizer](#sentencepiece-sacremoses-and-bpe)
* [Sentencepiece](#sentencepiece-sacremoses-and-bpe)
* [Byte Pair Encoding](#sentencepiece-sacremoses-and-bpe)
* [Mecab](#mecab)
* [Stanford Word Segmenter](#stanford-word-segmenter)

## Requirements

### Sentencepiece, Sacremoses and BPE

```bash
pip install sentencepiece sacremoses subword-nmt
```

### Mecab

```bash
mkdir -p tokenizers
git clone https://github.com/midobal/mecab.git
mkdir tokenizers/mecab
export PTH=$(pwd)
cd mecab/mecab
./configure --prefix="$PTH"/tokenizers/mecab --with-charset=utf8
make install
cd ../mecab-ipadic
./configure --with-mecab-config=../mecab/mecab-config --prefix="$PTH"/tokenizers/mecab --with-charset=utf8
make install
cd "$PTH"
rm -rf mecab
```

### Stanford Word Segmenter

```bash
mkdir -p tokenizers
wget https://nlp.stanford.edu/software/stanford-segmenter-2018-10-16.zip
unzip stanford-segmenter-2018-10-16.zip
mv stanford-segmenter-2018-10-16 tokenizers/stanford_segmenter
rm stanford-segmenter-2018-10-16.zip
```