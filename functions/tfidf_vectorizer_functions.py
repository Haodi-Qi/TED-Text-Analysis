#!/usr/bin/env python
# coding: utf-8

# In[1]:


def tokenizer(string):
    string_seperator = '{@}'
    return string.split(string_seperator)

def preprocessor(string):
    return string

