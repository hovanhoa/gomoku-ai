
import os
class SGF():
    def __init__(self):
        self.POS = 'abcdefghijklmno'
    def readData(self,path):
        f = open(path,'r',errors="ignore")
        data = f.read()
        # print(data)
        f.close()
        data = data.split(";")
        board = []
        step =0
        for point in data[2:-1]:
            x = self.POS.index(point[2])
            y = self.POS.index(point[3])
            board.append([x,y])
        return board

    def transferDataToTrain(self,path,color):
        data = self.readData(path)
        total_step = len(data)
        train_x = []
        train_y = []
        player = 1.0
        tmp = [0.0 for i in range(225)]
        for step in range(total_step):
            y = [0.0 for i in range(225)]
            train_x.append(tmp.copy())
            tmp[data[step][0]*15+data[step][1]] = player
            player = 2.0 if player == 1.0 else 1.0
            y[data[step][0]*15+data[step][1]] = 1.0
            train_y.append(y.copy())
        return train_x,train_y
    def shrinkTrainToSize(self,size,train_x,train_y):
        n_x = []
        n_y = []
        extra = (15-size)/2
        extra = int(extra)
        left_col = extra
        right_col = extra+size-1
        top_row = extra
        bottom_row = extra+size-1
        for j in range(len(train_x)):
            r_x = [0.0 for i in range(size*size)]
            r_y = [0.0 for i in range(size*size)]
            for i in range(225):
                col = i %15
                if i < 15:
                    row = 0
                else:
                    row = i/15
                    row = int(row)
                if row >= top_row and row <= bottom_row and col >= left_col and col <= right_col:
                    r_x[(row-extra)*size+(col-extra)] = train_x[j][i]
                    r_y[(row-extra)*size+(col-extra)] = train_y[j][i]
            n_x.append(r_x.copy())
            n_y.append(r_y.copy())
        return n_x,n_y
            
    @staticmethod
    def getAllFileName(path):
        root = os.listdir(path)
        files = []
        for p in root:
            child = os.path.join("%s%s" % (path,p))
            files.append(child)
        return files