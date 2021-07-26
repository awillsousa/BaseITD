#!/bin/bash

sudo docker commit mongodbserver mongo:latest
sudo docker stop mongodbserver 
