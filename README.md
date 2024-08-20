
<h1> victork </h1>
<h2>Make our own LLM AI Model with Python Transformers Hugingface Pytorch</h2>

first install dependencies:<br/>

#pip install transformers pytorch irc etc...

<h3>File train2.py:</h3>
<br/>
this code is the one that is responsible for taking a pre-made model in this case GPT2 small Spanish plus the training data from the file: "dataset-espanish.txt", the resulting model appears in the./results folder.

<h3>File Victor-K.py:</h3>
<br/>
This code makes a chatbot application for IRC of the libera.chat network, connecting the bot in a channel you can talk to it by writing the prefix !pi and the question. Modify the connection parameters to your needs.

execute with:

python3.11 train2.py

python3.11 victor-K.py
