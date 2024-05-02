import numpy as np
import matplotlib.pyplot as plt


# set width of bar
class bargraph:
    def view(d, img, word):
        img='D:\\Django\\Sentiment Reddit\\Sentiment\\Sentiment\\webapp\\static\\images\\'+img
        try:
            a1 = []
            a2 = []
            a3 = []
            a4 = []
            algo = []

            for r in d:
                print(r)
                algo.append(r)
                a1.append(round(float(d[r][0]), 2))
                


            k = []
            v = []
            barWidth = 0.25
            fig = plt.subplots(figsize=(10, 7))
            br1 = np.arange(len(a1))
            br2 = [x + barWidth for x in br1]

            plt.bar(br1, a1, color='purple', width=barWidth,
                    edgecolor='grey', label=word)
            
            plt.xlabel('Algorithms ', fontweight='bold', fontsize=15)
            plt.ylabel(word, fontweight='bold', fontsize=15)
            plt.xticks([r + barWidth for r in range(len(a1))], algo)
            plt.legend()
            plt.savefig(img, dpi=(200))
        except Exception as e:
            print(e)
            



if __name__ == '__main__':
    bargraph.view({'a1': [1, 2], 'a2': [1, 3], 'a3': [1, 2]},'g1.jpg','ACC')
