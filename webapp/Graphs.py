import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import sys
import sqlite3

def viewg(g1):
    

    for row in g1.values():
        pass

    height=[]
    bars = ()
    bars= tuple(g1.keys())

    plt.clf()



    print(type(g1.values()))
    height= list(g1.values())
    print(bars, height)
    
    y_pos = np.arange(len(bars))
    plt.bar(bars,height, color=['blue', 'cyan', 'orange'])
    plt.xlabel('Sentiment Analysis')
    plt.ylabel('No.of Tweets')
    plt.title('Features')
    from PIL import Image 
    plt.savefig('g1.jpg')
    #im = Image.open(r"g1.jpg") 
          
    #im.show()
        
if __name__ == "__main__":
    d={'jan':2,'feb':23}
    viewg(d)



