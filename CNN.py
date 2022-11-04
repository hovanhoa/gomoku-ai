import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from SGFfile import SGF
#path to save the log
logPath = "logs/log15"
#path to save the model
modePath = "model/m15.ckpt"
#size of board
board_size = 15
#0for empty;
#1 for black;
 #2 for white;
class CNN():
    def __init__(self,size):
        self.graph = tf.Graph()
        self.session = tf.InteractiveSession(graph=self.graph)
        self.x = tf.placeholder(tf.float32,[None,size*size])
        self.y = tf.placeholder(tf.float32,[None,size*size])
        self.w_conv1 = self.weight_variable([5,5,1,32])
        self.b_conv1 = self.bias_variable([32])
        self.x_image = tf.reshape(self.x,[-1,size,size,1])
        self.conv1 = tf.nn.relu(self.conv2d(self.x_image,self.w_conv1)+self.b_conv1)
        self.pool1 = self.max_pool(self.conv1)

        self.w_conv2 = self.weight_variable([5,5,32,64])
        self.b_conv2 = self.bias_variable([64])
        self.conv2 = tf.nn.relu(self.conv2d(self.pool1,self.w_conv2)+self.b_conv2)
        self.pool2 = self.max_pool(self.conv2)
        max_size = self.pool2.shape[1].value
        self.w_fc1 = self.weight_variable([max_size*max_size*64,1024])
        self.b_fc1 = self.bias_variable([1024])
        self.pool2_flat = tf.reshape(self.pool2,[-1,max_size*max_size*64])
        self.fc1 = tf.nn.relu(tf.matmul(self.pool2_flat,self.w_fc1)+self.b_fc1)


        self.w_fc2 = self.weight_variable([1024,size*size])
        self.b_fc2 = self.bias_variable([size*size])
        self.y_conv = tf.nn.softmax(tf.matmul(self.fc1,self.w_fc2)+self.b_fc2)

        self.sorted_pred = tf.argsort(self.y_conv,direction="DESCENDING")
        self.cross_entropy = -tf.reduce_sum(self.y * tf.log(self.y_conv))
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.cross_entropy)

        tf.summary.scalar("loss",self.cross_entropy)
        self.merged_summary = tf.summary.merge_all()
        self.saver = tf.train.Saver()
        self.session.run(tf.global_variables_initializer())
        correction_prediction = tf.equal(tf.argmax(self.y_conv,1),tf.argmax(self.y,1))
    @staticmethod
    def weight_variable(shape):
        return tf.Variable(tf.truncated_normal(shape,stddev=0.1))
    @staticmethod
    def bias_variable(shape):
        return tf.Variable(tf.constant(0.1,shape=shape))
    @staticmethod
    def conv2d(x,weight):
        return tf.nn.conv2d(x,weight,strides=[1,1,1,1],padding='SAME')
    @staticmethod
    def max_pool(x):
        return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

    def expend(self,board):
        new = [[0.0 for i in range(15)] for i in range(15)]
        size = len(board)
        extra = (15-size)/2
        extra = int(extra)
        for i in range(size):
            for l in range(size):
                new[extra+i][extra+l] = board[i][l]
        return new,extra

    def prediction(self,board):
        '''
        new_board = board
        extra = 0
        if len(board) < 15:
           new_board,extra= self.expend(board) 
        data = []
        tmp = []
        result = []
        finded = 0
        for row in new_board:
            for point in row:
                    tmp.append(point)
        data.append(tmp)
        left_col = extra
        right_col = extra+len(board)-1
        top_row = extra
        bottom_row = extra+len(board)-1
        '''
        data = []
        tmp = []
        result = []
        finded = 0
        size = len(board)
        for row in board:
            for point in row:
                tmp.append(point)
        data.append(tmp)
        sorted = self.session.run(self.sorted_pred,feed_dict={self.x:data})
        for dis in sorted[0]:
            col = dis%size
            if dis < size:
                row = 0
            else:
                row = (dis - col)/size
                row = int(row)
            if board[row][col] == 0.0:
                finded += 1
                result.append([row,col])
            if finded >= 10:
                break
        return result
    
    def save(self,path):
        saver = tf.train.Saver(write_version=tf.train.SaverDef.V2)
        saver.save(self.session,path)
    
    def restore(self,path):
        self.saver.restore(self.session,path)
if __name__ == "__main__":
    _cnn = CNN(board_size)
    sgf = SGF()
    batch = 0
    files = sgf.getAllFileName('.\sgf\\')
    train_file = files
    summary_writer = tf.summary.FileWriter(logPath)
    batch = 0
    for file in train_file:
        print(file)
        x,y = sgf.transferDataToTrain(file,1)
        n_x,n_y = sgf.shrinkTrainToSize(board_size,x,y)
        _cnn.session.run(_cnn.train_step,feed_dict={_cnn.x:n_x,_cnn.y:n_y})
        summary = _cnn.session.run(_cnn.merged_summary,feed_dict={_cnn.x:n_x,_cnn.y:n_y})

        summary_writer.add_summary(summary,batch)
        batch += 1
        print(batch)
    _cnn.save(modePath)


