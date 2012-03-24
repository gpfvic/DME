data<-read.table("orange_small_train.data",header=TRUE,sep="\t");

upselling<-read.table("orange_small_train_upselling.labels",header=FALSE);
appetency<-read.table("orange_small_train_appetency.labels",header=FALSE);
churn<-read.table("orange_small_train_churn.labels",header=FALSE);


#number
for (i in 1:190){
	y <- data[i][!is.na(data[i])];
	m = mean(y);
	data[i][is.na(data[i])]<-m;
}

#String
for (i in 191:230){
	data[i][is.na(data[i])] <- "None!!"
	y <- data[i][!is.na(data[i])]
	yf<-factor(y)  #get
	yfr<-table(yf)  #frequency table
	data[i] <-factor(y,labels=sequence(length(levels(yf))))  #replace with numbers
}

# remove feture with all NA: 8 15 20 32 39 42 48 52
count = 0;
for (i in 1:230){
    if ( is.na(data[,i]) )
        count = count +1;
}






write.arff(data,"filename");

install.packets("gbm");
#R package GBM (Generalized Boosted Regression Models)

library(rpart); # decision tree

#cross validation
n<-nrow(data)
K<-10; #folds
taille<-n %/% K
set.seed(5)
alea<-runif(n)
rang<-rank(alea)
bloc<-(rang-1) %/% taille + 1
bloc<-as.factor(bloc)
print(summary(bloc))

#http://en.wikibooks.org/wiki/Data_Mining_Algorithms_In_R/Classification/Decision_Trees




#apply(), 如 apply(X,2,mean), 第二个参数1表示对行操作，2表示对列操作，这里表示对矩阵的列做均值计算。
#lapply()用于对list对象进行操作
#sapply() 更为灵活的一个apply,可以接受向量或者矩阵作为主要参数


#myfunc <- function(arg1,arg2...) {}
#定义好了函数之后，可以通过source("myfunc.R")来加载，或者在启动R的时候加载，需要在.RData中定义，或者在.Rprofile中定义

