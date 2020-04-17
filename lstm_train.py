#!/usr/bin/env python3
# coding: utf-8
# File: lstm_train.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-12-24

import numpy as np
from keras import backend as K
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, Bidirectional, LSTM, Dense, TimeDistributed, Dropout
from keras_contrib.layers.crf import CRF
import matplotlib.pyplot as plt
import os
import re
import string


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class LSTMNER:
    def __init__(self):
        cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.train_path = os.path.join(cur, 'DataCrawler/ner_train.txt')
        self.vocab_path = os.path.join(cur, 'ner_model/vocab.txt')
        self.embedding_file = os.path.join(cur, 'ner_model/token_vec_300.bin')
        self.model_path = os.path.join(cur, 'ner_model/tokenvec_bilstm2_crf_model_20.h5')
        self.datas, self.word_dict = self.build_data()#dates代表每一句话的内容和其类别，word_dict代表文字及索引
        self.class_dict ={
                        'O':0,
                        'B-sym':1,
                        'I-sym':2,
                        'E-sym':3,
                        'S-sym':4,
                        'B-symdescription':5,
                        'I-symdescription':6,
                        'E-symdescription':7,
                        'S-symdescription':8
                        }
        self.EMBEDDING_DIM = 300
        self.EPOCHS =5
        self.BATCH_SIZE = 128
        self.NUM_CLASSES = len(self.class_dict)
        self.VOCAB_SIZE = len(self.word_dict)
        self.TIME_STAMPS = 150
        self.embedding_matrix = self.build_embedding_matrix()

    '''构造数据集'''
    def build_data(self):
        #zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        #punc=string.punctuation
        datas = []
        sample_x = []
        sample_y = []
        vocabs = {'UNK'}
        for line in open(self.train_path,encoding='utf-8'):
            line = line.rstrip().split(' ')
            if not line:
                continue
            char = line[0]
            if not char: #or not zhmodel.search(char) or char not in punc:#如果字符不存在，或者不是中文字符或者不是标点符号则略过
                continue
            cate = line[-1]
            sample_x.append(char)
            sample_y.append(cate)
            vocabs.add(char)
            if char in ['。','?','!','！','？']:
                datas.append([sample_x, sample_y])
                sample_x = []
                sample_y = []
        word_dict = {wd:index for index, wd in enumerate(list(vocabs))}
        self.write_file(list(vocabs), self.vocab_path)
        return datas, word_dict

    '''将数据转换成keras所需的格式'''
    def modify_data(self):
        x_train = [[self.word_dict[char] for char in data[0]] for data in self.datas]
        y_train = [[self.class_dict[label] for label in data[1]] for data in self.datas]
        x_train = pad_sequences(x_train, self.TIME_STAMPS)#填充数据位数，TIME_STAMPS代表每个句子的位数，大于的截断，小于的补0
        y = pad_sequences(y_train, self.TIME_STAMPS)
        y_train = np.expand_dims(y, 2)
        return x_train, y_train

    '''保存字典文件'''
    def write_file(self, wordlist, filepath):
        with open(filepath,encoding='utf-8', mode='w+') as f:
            f.write('\n'.join(wordlist))

    '''加载预训练词向量'''
    def load_pretrained_embedding(self):
        embeddings_dict = {}
        with open(self.embedding_file,encoding='utf-8', mode='r') as f:
            for line in f:
                values = line.strip().split(' ')
                if len(values) < 300:
                    continue
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_dict[word] = coefs
        print('Found %s word vectors.' % len(embeddings_dict))
        return embeddings_dict

    '''加载词向量矩阵'''
    def build_embedding_matrix(self):
        embedding_dict = self.load_pretrained_embedding()
        embedding_matrix = np.zeros((self.VOCAB_SIZE + 1, self.EMBEDDING_DIM))
        for word, i in self.word_dict.items():
            embedding_vector = embedding_dict.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        return embedding_matrix

    '''使用预训练向量进行模型训练'''
    def tokenvec_bilstm2_crf_model(self):
        model = Sequential()
        embedding_layer = Embedding(self.VOCAB_SIZE + 1,
                                    self.EMBEDDING_DIM,#300
                                    weights=[self.embedding_matrix],
                                    input_length=self.TIME_STAMPS,
                                    trainable=False,
                                    mask_zero=True)
        model.add(embedding_layer)
        model.add(Bidirectional(LSTM(128, return_sequences=True)))
        model.add(Dropout(0.5))
        model.add(Bidirectional(LSTM(64, return_sequences=True)))
        model.add(Dropout(0.5))
        model.add(TimeDistributed(Dense(self.NUM_CLASSES)))
        crf_layer = CRF(self.NUM_CLASSES, sparse_target=True)
        model.add(crf_layer)
        model.compile('adam', loss=crf_layer.loss_function, metrics=[crf_layer.accuracy])
        model.summary()
        return model

    '''训练模型'''
    def train_model(self):
        x_train, y_train = self.modify_data()
        model = self.tokenvec_bilstm2_crf_model()
        history = model.fit(x_train[:], y_train[:], validation_split=0.2, batch_size=self.BATCH_SIZE, epochs=self.EPOCHS)
        self.draw_train(history)
        model.save(self.model_path)
        return model

    '''绘制训练曲线'''
    def draw_train(self, history):
        # Plot training & validation accuracy values
        plt.plot(history.history['crf_viterbi_accuracy'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train'], loc='upper left')
        plt.show()
        # Plot training & validation loss values
        plt.plot(history.history['loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train'], loc='upper left')
        plt.show()
        # 7836/7836 [==============================] - 205s 26ms/step - loss: 17.1782 - acc: 0.9624
        '''
        6268/6268 [==============================] - 145s 23ms/step - loss: 18.5272 - acc: 0.7196 - val_loss: 15.7497 - val_acc: 0.8109
        6268/6268 [==============================] - 142s 23ms/step - loss: 17.8446 - acc: 0.9099 - val_loss: 15.5915 - val_acc: 0.8378
        6268/6268 [==============================] - 136s 22ms/step - loss: 17.7280 - acc: 0.9485 - val_loss: 15.5570 - val_acc: 0.8364
        6268/6268 [==============================] - 133s 21ms/step - loss: 17.6918 - acc: 0.9593 - val_loss: 15.5187 - val_acc: 0.8451
        6268/6268 [==============================] - 144s 23ms/step - loss: 17.6723 - acc: 0.9649 - val_loss: 15.4944 - val_acc: 0.8451
        '''

if __name__ == '__main__':
    ner = LSTMNER()
    ner.train_model()