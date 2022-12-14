# -*- coding: utf-8 -*-
"""손글씨-2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Uhdimt3CGgPzfQiuWxUs_86_4aEQ0uHh
"""

import numpy as np
np.random.seed(4)
import pandas as pd
import torch
import imageio
import glob

data_file = open("train.csv",'r') #'r'은 읽기 전용
data_list = data_file.readlines()
data_file.close()

len(data_list)

data_list[0]

# Commented out IPython magic to ensure Python compatibility.
import numpy
import matplotlib.pyplot
# %matplotlib inline

all_values = data_list[1].split(',') 
image_array = numpy.asfarray(all_values[1:]).reshape((28,28)) 
matplotlib.pyplot.imshow(image_array, cmap='Greys', interpolation='None')

# scale input to range 0.01 to 1.00
scaled_input = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
print(scaled_input)

#출력 노드 계층의 노드 수는 10 (10개의 레이블)
onodes = 10
targets = numpy.zeros(onodes) + 0.01 #0을 피하기 위해 +0.01
targets[int(all_values[0])] = 0.99

print(targets)

# Commented out IPython magic to ensure Python compatibility.
#3계층의 신경망으로 MNIST 데이터를 학습하는 코드

import numpy
# 시그모이드 함수 expit() 사용을 위해 scipy.special 불러오기
import scipy.special
# 행렬을 시각화하기 위한 라이브러리
import matplotlib.pyplot
# 시각화가 외부 윈도우가 아닌 현재의 노트북 내에서 보이도록 설정
# %matplotlib inline

# 신경망 클래스의 정의 
class neuralNetwork:
    
    
    # 신경망 초기화하기
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # 입력, 은익, 출력 계층의 노드 개수 설정
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        
        # 가중치 matrices, wih와 who
        # arrays 내 가중치는 w_i_j로 표기
        self.wih = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))

        # 학습률
        self.lr = learningrate
        
        # activation 함수는 sigmoid 함수
        self.activation_function = lambda x: scipy.special.expit(x)
        
        pass

    
    # 신경망 학습시키기
    def train(self, inputs_list, targets_list):
        # 입력 리스트를 2차원의 행렬로 변환
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        
        # 은닉 계층으로 들어오는 신호를 계산
        hidden_inputs = numpy.dot(self.wih, inputs)
        # 은닉 계층에서 나가는 신호를 계산
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # 최종 출력 계층으로 들어오는 신호를 계산
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # 최종 출력 계층에서 나가는 신호를 계산
        final_outputs = self.activation_function(final_inputs)
        
        # 출력 계층의 오차는 (target - actual)
        output_errors = targets - final_outputs
        # 은닉 계층의 오차는 가중치에 의해 나뉜 출력 계층의 오차들을 재조합해 계산
        hidden_errors = numpy.dot(self.who.T, output_errors) 
        
        # 은닉 계층과 출력 계층 간의 가중치 업데이트
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        
        # 입력 계층과 은닉 계층 간의 가중치 업데이트
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))
        
        pass

    
    # 신경망에 질의하기
    def query(self, inputs_list):
        # inputs list를 2d array로 변환
        inputs = numpy.array(inputs_list, ndmin=2).T
        
        # hidden layer로 들어오는 신호 계산
        hidden_inputs = numpy.dot(self.wih, inputs)
        # hidden layer에서 나가는 신호 계산
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # final output layer로 들어오는 신호 계산
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # final output layer에서 나가는 신호 계산
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs

training_data_file = open("train.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

#심층학습
input_nodes = 784
hidden_nodes = 200
output_nodes = 10

learning_rate = 0.2

n = neuralNetwork(input_nodes,hidden_nodes,output_nodes, learning_rate)

training_data_file = open("train.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

# 주기(epoch)
epochs = 7

for e in range(epochs):
    for record in training_data_list:
        all_values = record.split(',')
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        targets = numpy.zeros(output_nodes) + 0.01
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)
        pass
    pass

test_data_file = open("train.csv", 'r')
test_data_list = test_data_file.readlines()
test_data_file.close()

scorecard = []

for record in test_data_list:
    all_values = record.split(',')
    correct_label = int(all_values[0])
    inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
    outputs = n.query(inputs)
    label = numpy.argmax(outputs)
    if (label == correct_label):
        scorecard.append(1)
    else:
        scorecard.append(0)
        pass
    
    pass

scorecard_array = numpy.asarray(scorecard)
print ("performance = ", scorecard_array.sum() / scorecard_array.size)

data_file = open("test.csv",'r') #'r'은 읽기 전용
Test_data_list = data_file.readlines()
data_file.close()

from PIL import Image

our_own_dataset = []
label = 0

# test.png는 그림판에서 붓으로 숫자 8을 그린 이미지 파일
# test.png 파일 열어서 L(256단계 흑백이미지)로 변환
img = Image.open("test13.png").convert("L")

# 이미지를 784개 흑백 픽셀로 사이즈 변환
img = np.resize(img, (1, 784))

# 데이터를 모델에 적용할 수 있도록 가공
test_data = ((np.array(img) / 255) - 1) * -1

# data is remaining values
inputs = test_data

# query the network
outputs = n.query(inputs)
print (outputs)

# the index of the highest value corresponds to the label
label = np.argmax(outputs)
print("network says ", label)

