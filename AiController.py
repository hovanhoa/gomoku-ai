import copy

def isChessed(board,row,col,color):
    if row >= len(board) or col >= len(board):
        return False
    if row < 0 or  col < 0 :
        return False
    return board[row][col] == color

def checkWiner(board,point):
    
    row = point[0]
    col = point[1]
    color = board[row][col]
    #col
    length = 1
    d1 = True
    d2 = True
    for i in range(4):
        if  d1 and isChessed(board,row,col+1+i,color):
            length +=1
        else:
            d1 = False
        if d2 and isChessed(board,row,col-1-i,color):
            length+=1
        else:
            d2 = False
        if not d1 and not d2:
            break
    if length >= 5:
        return True
    #row
    length = 1
    d1 = True
    d2 = True
    for i in range(4):
        if  d1 and isChessed(board,row+i+1,col,color):
            length+=1
        else:
            d1 = False
        if d2 and isChessed(board,row-1-i,col,color):
            length+=1
        else:
            d2 = False
        if not d1 and not d2:
            break
    if length >= 5:
        return True
    
    #positive
    length = 1
    d1 = True
    d2 = True
    for i in range(4):
        if  d1 and isChessed(board,row-1-i,col+1+i,color):
            length+=1
        else:
            d1 = False
        if d2 and isChessed(board,row+1+i,col-1-i,color):
            length+=1
        else:
            d2 = False
        if not d1 and not d2:
            break
    if length >= 5:
        return True    
    
    #negative:
    length = 1
    d1 = True
    d2 = True
    for i in range(4):
        if  d1 and isChessed(board,row-1-i,col-1-i,color):
            length+=1
        else:
            d1 = False
        if d2 and isChessed(board,row+1+i,col+1+i,color):
            length+=1
        else:
            d2 = False
        if not d1 and not d2:
            break
    if length >= 5:
        return True
    return False

def ValueOfBoard(player,board,point):
    row = point[0]
    col = point[1]
    color = player
    value = 0
    #col
    length = 1
    d1 = True
    d2 = True
    for i in range(4):
        if  d1 and isChessed(board,row,col+1+i,color):
            length +=1
        else:
            d1 = False
        if d2 and isChessed(board,row,col-1-i,color):
            length+=1
        else:
            d2 = False
        if not d1 and not d2:
            break
    value += 10**length
    #row
    length = 1
    d1 = True
    d2 = True
    for i in range(4):
        if  d1 and isChessed(board,row+i+1,col,color):
            length+=1
        else:
            d1 = False
        if d2 and isChessed(board,row-1-i,col,color):
            length+=1
        else:
            d2 = False
        if not d1 and not d2:
            break
    value +=10**length
    
    #positive
    length = 1
    d1 = True
    d2 = True
    for i in range(4):
        if  d1 and isChessed(board,row-1-i,col+1+i,color):
            length+=1
        else:
            d1 = False
        if d2 and isChessed(board,row+1+i,col-1-i,color):
            length+=1
        else:
            d2 = False
        if not d1 and not d2:
            break
    value +=10**length
    
    #negative:
    length = 1
    d1 = True
    d2 = True
    for i in range(4):
        if  d1 and isChessed(board,row-1-i,col-1-i,color):
            length+=1
        else:
            d1 = False
        if d2 and isChessed(board,row+1+i,col+1+i,color):
            length+=1
        else:
            d2 = False
        if not d1 and not d2:
            break
    value +=10**length
    return value

class AIcontroller(object):
    def __init__(self,mode,cnn):
        self.mode = mode
        self.node = 0
        self.color = 2
        self.opsite = 1
        self.cnn = cnn
    def initilaize(self,color,mode):
        self.mode = mode
        self.node = 0
        self.color = 2
        self.opsite = 1
    def AllAviable(self,board):
        result = []
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == 0:
                    result.append([row,col])
        return result
    def findNextPoints(self):
        #using cnn to find next 10 most possible point
        if self.mode == 1:
            return self.cnn.prediction(self.board)
        else:
            return self.AllAviable(self.board)

    def Evaluate(self,board,point):
        color = board[point[0]][point[1]]
        o_color = 1 if color == 2 else 2
        playerValue = ValueOfBoard(color,board,point)
        enmyValue = ValueOfBoard(o_color,board,point)
        value = playerValue+enmyValue
        if board[point[0]][point[1]] == self.color:
            return value
        elif board[point[0]][point[1]] == self.opsite:
            return  value *-1
        return 0


    #find next point that has highest value
    def minmaxTree(self,step,probailty):
        self.node=0
        nextPoints = self.findNextPoints()
        max = -30000000
        bestPoint = nextPoints[0]
        for point in nextPoints:
           # new_board = copy.deepcopy(self.board)
            #playAchess(new_board,point,self.color)
           # board.playAchess(point,self.color)
            self.board[point[0]][point[1]] = self.color
            self.leftPos-=1
            value = self.chanceNode(step,probailty,point)
            if(max < value):
                max = value
                bestPoint = [point[0],point[1]]
            self.board[point[0]][point[1]] = 0.0
            self.leftPos +=1
        return bestPoint
    
    #def calculate the value of chance node
    def chanceNode(self,step,probailty,point):
        max_pro = 0.0
        min_pro = 0.0
        if self.board[point[0]][point[1]] == self.color:
            max_pro = probailty
            min_pro = (1-probailty)
        else:
            max_pro = (1-probailty)
            min_pro = probailty
        self.node += 1 
        over = checkWiner(self.board,point)
        if over:
                return 1000000 if self.board[point[0]][point[1]] == self.color else -1000000
        if self.leftPos == 0:
            return 0
        if step == 0:
            return self.Evaluate(self.board,point)
        return max_pro * self.maxNode(self.board,step-1,probailty) + min_pro * self.minNode(self.board,step-1,probailty)



    def minNode(self,board,step,probailty):
        nextColor = self.opsite
        nextPoints = self.findNextPoints()
        min = 30000000
        for point in nextPoints:
           # new_board = copy.deepcopy(self.board)
            #playAchess(new_board,point,self.color)
            board[point[0]][point[1]] = nextColor
            self.leftPos-=1
            value = self.chanceNode(step,probailty,point)
            if(min > value):
                min = value
            board[point[0]][point[1]] = 0.0
            self.leftPos+=1
        return min

    def maxNode(self,board,step,probailty):
        nextPoints = self.findNextPoints()
        max = -300000
        for point in nextPoints:
           # new_board = copy.deepcopy(self.board)
            #playAchess(new_board,point,self.color)
            board[point[0]][point[1]] = self.color
            self.leftPos-=1
            value = self.chanceNode(step,probailty,point)
            if(max < value):
                max = value
            board[point[0]][point[1]] = 0.0
            self.leftPos+=1
        return max
            
    def playNextStep(self,board,remainning):
        self.board = board
        self.remainning = remainning
        self.leftPos = len(remainning)
        best_point = self.minmaxTree(1,0.2)
        return best_point,self.node