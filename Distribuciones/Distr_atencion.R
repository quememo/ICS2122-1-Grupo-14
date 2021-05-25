
################ AQUI LO IMPORTANTE  #########

data <- read.csv2(file.choose())
data <- as.data.frame(data)
library(univariateML)
library(dplyr)

data$ATENCION <- as.numeric(as.character(data$ATENCION))
data$CLUSTER <- as.numeric(as.character(data$CLUSTER))

cluster1 = filter(data, CLUSTER == 1)
cluster2 = filter(data, CLUSTER == 2)
cluster3 = filter(data, CLUSTER == 3)
cluster4 = filter(data, CLUSTER == 4)
cluster5 = filter(data, CLUSTER == 5)
cluster6 = filter(data, CLUSTER == 6)
cluster7 = filter(data, CLUSTER == 7)
cluster8 = filter(data, CLUSTER == 8)
cluster9 = filter(data, CLUSTER == 9)

###### BIC ########
# Se comparan únicamente las distribuciones con un dominio [0, +inf)

install.packages("univariateML")
library(univariateML)

##### MAPA COMPLETO ####

###### BIC ########
# Se comparan únicamente las distribuciones con un dominio [0, +inf)

comparacion_bic_data <- BIC(
  mlcauchy(data$ATENCION),
  mlgumbel(data$ATENCION),
  mllaplace(data$ATENCION),
  mllogis(data$ATENCION),
  mlnorm(data$ATENCION),
  mlstd(data$ATENCION),
  mlged(data$ATENCION),
  mlsnorm(data$ATENCION),
  mlsstd(data$ATENCION),
  mlsged(data$ATENCION),
  mlbetapr(data$ATENCION),
  mlexp(data$ATENCION),
  mlgamma(data$ATENCION),
  mlinvgamma(data$ATENCION),
  mlinvgauss(data$ATENCION),
  mlinvweibull(data$ATENCION),
  mlllogis(data$ATENCION),
  mllnorm(data$ATENCION),
  mlunif(data$ATENCION),
  mlpower(data$ATENCION)
)

###### AIC ########
comparacion_aic_data <- AIC(
  mlcauchy(data$ATENCION),
  mlgumbel(data$ATENCION),
  mllaplace(data$ATENCION),
  mllogis(datas$ATENCION),
  mlnorm(data$ATENCION),
  mlstd(data$ATENCION),
  mlged(data$ATENCION),
  mlsnorm(data$ATENCION),
  mlsstd(data$ATENCION),
  mlsged(data$ATENCION),
  mlbetapr(data$ATENCION),
  mlexp(data$ATENCION),
  mlgamma(data$ATENCION),
  mlinvgamma(data$ATENCION),
  mlinvgauss(data$ATENCION),
  mlinvweibull(data$ATENCION),
  mlllogis(datas$ATENCION),
  mllnorm(data$ATENCION),
  mlunif(data$ATENCION),
  mlpower(data$ATENCION)
)

###### HISTOGRAMAS Y LINEAS ########

hist(data$ATENCION,
     main = "Distribución tiempo de atención",
     freq = FALSE,
     ylim = c(0, 0.08))
lines(mlinvgauss(data$ATENCION), lwd = 2, lty = 2, col = "red")
lines(mllnorm(data$ATENCION), lwd = 2, lty = 1, col = "yellow")
#lines(mlsged(data$ATENCION), lwd = 2, lty = 1, col = "blue")
lines(mlcauchy(data$ATENCION), lwd = 2, lty = 2, col = "green")
legend(x = 15000, y = 0.0001, legend = c("invgauss", "lnorm"),
       col = c("red", "yellow"), lty = 2:1)
rug(data$ATENCION)


###### AJUSTE DISTRIBUCIÓN ########

# Ajuste de una distribución log-normal
distribucion <- mlinvgauss(data$ATENCION)   #16.48079  35.63567
summary(distribucion)

# Intervalo de confianza del 95% estimados por bootstrapping
bootstrapml(distribucion, probs = c(0.05, 0.95), reps = 1000)


########## AHORA LO SACAMOS POR CLUSTERS   ####

#cluster1$ATENCION <- as.numeric(as.character(cluster1$ATENCION))

comparacion_bic1 <- BIC(
  mlcauchy(cluster1$ATENCION),
  mlgumbel(cluster1$ATENCION),
  mllaplace(cluster1$ATENCION),
  mllogis(cluster1$ATENCION),
  mlnorm(cluster1$ATENCION),
  mlstd(cluster1$ATENCION),
  mlged(cluster1$ATENCION),
  mlsnorm(cluster1$ATENCION),
  mlsstd(cluster1$ATENCION),
  mlsged(cluster1$ATENCION),
  mlbetapr(cluster1$ATENCION),
  mlexp(cluster1$ATENCION),
  mlgamma(cluster1$ATENCION),
  mlinvgamma(cluster1$ATENCION),
  mlinvgauss(cluster1$ATENCION),
  mlinvweibull(cluster1$ATENCION),
  mlllogis(cluster1$ATENCION),
  mllnorm(cluster1$ATENCION),
  mlunif(cluster1$ATENCION),
  mlpower(cluster1$ATENCION)
)

distribucion1 <- mlinvgauss(cluster1$ATENCION)   #16.48113  37.26090
summary(distribucion1)

#cluster2$ATENCION <- as.numeric(as.character(cluster2$ATENCION))

comparacion_bic2 <- BIC(
  mlcauchy(cluster2$ATENCION),
  mlgumbel(cluster2$ATENCION),
  mllaplace(cluster2$ATENCION),
  mllogis(cluster2$ATENCION),
  mlnorm(cluster2$ATENCION),
  mlstd(cluster2$ATENCION),
  mlged(cluster2$ATENCION),
  mlsnorm(cluster2$ATENCION),
  mlsstd(cluster2$ATENCION),
  mlsged(cluster2$ATENCION),
  mlbetapr(cluster2$ATENCION),
  mlexp(cluster2$ATENCION),
  mlgamma(cluster2$ATENCION),
  mlinvgamma(cluster2$ATENCION),
  mlinvgauss(cluster2$ATENCION),
  mlinvweibull(cluster2$ATENCION),
  mlllogis(cluster2$ATENCION),
  mllnorm(cluster2$ATENCION),
  mlunif(cluster2$ATENCION),
  mlpower(cluster2$ATENCION)
)

distribucion2 <- mlinvgauss(cluster2$ATENCION)   #16.41224  34.69584
summary(distribucion2)

#cluster3$ATENCION <- as.numeric(as.character(cluster3$ATENCION))

comparacion_bic3 <- BIC(
  mlcauchy(cluster3$ATENCION),
  mlgumbel(cluster3$ATENCION),
  mllaplace(cluster3$ATENCION),
  mllogis(cluster3$ATENCION),
  mlnorm(cluster3$ATENCION),
  mlstd(cluster3$ATENCION),
  mlged(cluster3$ATENCION),
  mlsnorm(cluster3$ATENCION),
  mlsstd(cluster3$ATENCION),
  mlsged(cluster3$ATENCION),
  mlbetapr(cluster3$ATENCION),
  mlexp(cluster3$ATENCION),
  mlgamma(cluster3$ATENCION),
  mlinvgamma(cluster3$ATENCION),
  mlinvgauss(cluster3$ATENCION),
  mlinvweibull(cluster3$ATENCION),
  mlllogis(cluster3$ATENCION),
  mllnorm(cluster3$ATENCION),
  mlunif(cluster3$ATENCION),
  mlpower(cluster3$ATENCION)
)

distribucion3 <- mlinvgauss(cluster3$ATENCION)   #16.49151  35.03534 
summary(distribucion3)

#cluster4$ATENCION <- as.numeric(as.character(cluster4$ATENCION))

comparacion_bic4 <- BIC(
  mlcauchy(cluster4$ATENCION),
  mlgumbel(cluster4$ATENCION),
  mllaplace(cluster4$ATENCION),
  mllogis(cluster4$ATENCION),
  mlnorm(cluster4$ATENCION),
  mlstd(cluster4$ATENCION),
  mlged(cluster4$ATENCION),
  mlsnorm(cluster4$ATENCION),
  mlsstd(cluster4$ATENCION),
  mlsged(cluster4$ATENCION),
  mlbetapr(cluster4$ATENCION),
  mlexp(cluster4$ATENCION),
  mlgamma(cluster4$ATENCION),
  mlinvgamma(cluster4$ATENCION),
  mlinvgauss(cluster4$ATENCION),
  mlinvweibull(cluster4$ATENCION),
  mlllogis(cluster4$ATENCION),
  mllnorm(cluster4$ATENCION),
  mlunif(cluster4$ATENCION),
  mlpower(cluster4$ATENCION)
)
distribucion4 <- mlinvgauss(cluster4$ATENCION)   #15.78613  34.44476
summary(distribucion4)

#cluster5$ATENCION <- as.numeric(as.character(cluster5$ATENCION))

comparacion_bic5 <- BIC(
  mlcauchy(cluster5$ATENCION),
  mlgumbel(cluster5$ATENCION),
  mllaplace(cluster5$ATENCION),
  mllogis(cluster5$ATENCION),
  mlnorm(cluster5$ATENCION),
  mlstd(cluster5$ATENCION),
  mlged(cluster5$ATENCION),
  mlsnorm(cluster5$ATENCION),
  mlsstd(cluster5$ATENCION),
  mlsged(cluster5$ATENCION),
  mlbetapr(cluster5$ATENCION),
  mlexp(cluster5$ATENCION),
  mlgamma(cluster5$ATENCION),
  mlinvgamma(cluster5$ATENCION),
  mlinvgauss(cluster5$ATENCION),
  mlinvweibull(cluster5$ATENCION),
  mlllogis(cluster5$ATENCION),
  mllnorm(cluster5$ATENCION),
  mlunif(cluster5$ATENCION),
  mlpower(cluster5$ATENCION)
)
distribucion5 <- mlinvgauss(cluster5$ATENCION)   #16.68389  35.61363 
summary(distribucion5)

#cluster6$ATENCION <- as.numeric(as.character(cluster6$ATENCION))

comparacion_bic6 <- BIC(
  mlcauchy(cluster6$ATENCION),
  mlgumbel(cluster6$ATENCION),
  mllaplace(cluster6$ATENCION),
  mllogis(cluster6$ATENCION),
  mlnorm(cluster6$ATENCION),
  mlstd(cluster6$ATENCION),
  mlged(cluster6$ATENCION),
  mlsnorm(cluster6$ATENCION),
  mlsstd(cluster6$ATENCION),
  mlsged(cluster6$ATENCION),
  mlbetapr(cluster6$ATENCION),
  mlexp(cluster6$ATENCION),
  mlgamma(cluster6$ATENCION),
  mlinvgamma(cluster6$ATENCION),
  mlinvgauss(cluster6$ATENCION),
  mlinvweibull(cluster6$ATENCION),
  mlllogis(cluster6$ATENCION),
  mllnorm(cluster6$ATENCION),
  mlunif(cluster6$ATENCION),
  mlpower(cluster6$ATENCION)
)
distribucion6 <- mlinvgauss(cluster6$ATENCION)   #16.62763  35.89465
summary(distribucion6)

comparacion_bic7 <- BIC(
  mlcauchy(cluster7$ATENCION),
  mlgumbel(cluster7$ATENCION),
  mllaplace(cluster7$ATENCION),
  mllogis(cluster7$ATENCION),
  mlnorm(cluster7$ATENCION),
  mlstd(cluster7$ATENCION),
  mlged(cluster7$ATENCION),
  mlsnorm(cluster7$ATENCION),
  mlsstd(cluster7$ATENCION),
  mlsged(cluster7$ATENCION),
  mlbetapr(cluster7$ATENCION),
  mlexp(cluster7$ATENCION),
  mlgamma(cluster7$ATENCION),
  mlinvgamma(cluster7$ATENCION),
  mlinvgauss(cluster7$ATENCION),
  mlinvweibull(cluster7$ATENCION),
  mlllogis(cluster7$ATENCION),
  mllnorm(cluster7$ATENCION),
  mlunif(cluster7$ATENCION),
  mlpower(cluster7$ATENCION)
)
distribucion7 <- mlinvgauss(cluster7$ATENCION)   #16.30330  35.99362
summary(distribucion7)


comparacion_bic8 <- BIC(
  mlcauchy(cluster8$ATENCION),
  mlgumbel(cluster8$ATENCION),
  mllaplace(cluster8$ATENCION),
  mllogis(cluster8$ATENCION),
  mlnorm(cluster8$ATENCION),
  mlstd(cluster8$ATENCION),
  mlged(cluster8$ATENCION),
  mlsnorm(cluster8$ATENCION),
  mlsstd(cluster8$ATENCION),
  mlsged(cluster8$ATENCION),
  mlbetapr(cluster8$ATENCION),
  mlexp(cluster8$ATENCION),
  mlgamma(cluster8$ATENCION),
  mlinvgamma(cluster8$ATENCION),
  mlinvgauss(cluster8$ATENCION),
  mlinvweibull(cluster8$ATENCION),
  mlllogis(cluster8$ATENCION),
  mllnorm(cluster8$ATENCION),
  mlunif(cluster8$ATENCION),
  mlpower(cluster8$ATENCION)
)
distribucion8 <- mlinvgauss(cluster8$ATENCION)   #16.50513  35.26737
summary(distribucion8)


distribucion9 <- mlinvgauss(cluster9$ATENCION)   #16.48033  36.96150
summary(distribucion9)




###### HISTOGRAMAS Y LINEAS ########

hist(cluster1$ATENCION,
     main = "Distribución Clusters 1",
     freq = FALSE,
     ylim = c(0, 0.08))
lines(mlinvgauss(cluster1$ATENCION), lwd = 2, lty = 2, col = "red")
lines(mllnorm(cluster1$ATENCION), lwd = 2, lty = 1, col = "yellow")
lines(mlcauchy(cluster1$ATENCION), lwd = 2, lty = 2, col = "green")
legend(x = 15000, y = 0.0001, legend = c("invgauss", "lnorm"),
       col = c("red", "yellow"), lty = 2:1)
rug(cluster1$ATENCION)

hist(cluster2$ATENCION,
     main = "Distribución Clusters 2",
     freq = FALSE,
     ylim = c(0, 0.08))
lines(mlsged(cluster2$ATENCION), lwd = 2, lty = 2, col = "red")
lines(mllnorm(cluster2$ATENCION), lwd = 2, lty = 1, col = "yellow")
lines(mlcauchy(cluster2$ATENCION), lwd = 2, lty = 2, col = "green")
legend(x = 15000, y = 0.0001, legend = c("invgauss", "lnorm"),
       col = c("red", "yellow"), lty = 2:1)
rug(cluster2$ATENCION)

hist(cluster3$ATENCION,
     main = "Distribución Clusters 3",
     freq = FALSE,
     ylim = c(0, 0.08))
lines(mlinvgauss(cluster3$ATENCION), lwd = 2, lty = 2, col = "red")
lines(mllnorm(cluster3$ATENCION), lwd = 2, lty = 1, col = "yellow")
lines(mlcauchy(cluster3$ATENCION), lwd = 2, lty = 2, col = "green")
legend(x = 15000, y = 0.0001, legend = c("invgauss", "lnorm"),
       col = c("red", "yellow"), lty = 2:1)
rug(cluster3$ATENCION)

hist(cluster4$ATENCION,
     main = "Distribución Clusters 4",
     freq = FALSE,
     ylim = c(0, 0.08))
lines(mlinvgauss(cluster4$ATENCION), lwd = 2, lty = 2, col = "red")
lines(mllnorm(cluster4$ATENCION), lwd = 2, lty = 1, col = "yellow")
lines(mlcauchy(cluster4$ATENCION), lwd = 2, lty = 2, col = "green")
legend(x = 15000, y = 0.0001, legend = c("invgauss", "lnorm"),
       col = c("red", "yellow"), lty = 2:1)
rug(cluster4$ATENCION)

hist(cluster5$ATENCION,
     main = "Distribución Clusters 5",
     freq = FALSE,
     ylim = c(0, 0.08))
lines(mlinvgauss(cluster5$ATENCION), lwd = 2, lty = 2, col = "red")
lines(mllnorm(cluster5$ATENCION), lwd = 2, lty = 1, col = "yellow")
lines(mlcauchy(cluster5$ATENCION), lwd = 2, lty = 2, col = "green")
legend(x = 15000, y = 0.0001, legend = c("invgauss", "lnorm"),
       col = c("red", "yellow"), lty = 2:1)
rug(cluster5$ATENCION)

hist(cluster6$ATENCION,
     main = "Distribución Clusters 6",
     freq = FALSE,
     ylim = c(0, 0.08))
lines(mlinvgauss(cluster6$ATENCION), lwd = 2, lty = 2, col = "red")
lines(mllnorm(cluster6$ATENCION), lwd = 2, lty = 1, col = "yellow")
lines(mlcauchy(cluster6$ATENCION), lwd = 2, lty = 2, col = "green")
legend(x = 15000, y = 0.0001, legend = c("invgauss", "lnorm"),
       col = c("red", "yellow"), lty = 2:1)
rug(cluster6$ATENCION)


###########  PARA SACAR PARAMETROS ######

distribucion <- mlsged(data$ATENCION) 
distribucion1 <- mlsged(cluster1$ATENCION)
distribucion2 <- mlsged(cluster2$ATENCION)
distribucion3 <- mlsged(cluster3$ATENCION)
distribucion4 <- mlsged(cluster4$ATENCION)
distribucion5 <- mlsged(cluster5$ATENCION)
distribucion6 <- mlsged(cluster6$ATENCION)
distribucion7 <- mlsged(cluster7$ATENCION)
distribucion8 <- mlsged(cluster8$ATENCION)
distribucion9 <- mlsged(cluster9$ATENCION)


summary(distribucion)          
summary(distribucion1)   
summary(distribucion2)   
summary(distribucion3)   
summary(distribucion4)    
summary(distribucion5)   
summary(distribucion6)   
summary(distribucion7)   
summary(distribucion8)   
summary(distribucion9)

#TODA 16.534297  10.181317   1.547342  76.759614
#1.     16.527571     9.979530     1.628056  1988.671087
#2.    16.453024    10.373477     1.450344  1242.029204
#3.     16.559176    10.160623     1.563011  1489.138481
#4.    15.808719  10.146349   1.325434  13.187429
#5.     16.750293  10.250217   1.590465  37.598476
#6.    16.681971    10.249126     1.565067  1407.178997
#7.     16.353146   10.021809    1.550733  921.677222
#8.    16.564921    10.228791     1.536481  1019.772078
#9.    16.553963   9.867084   1.685003  19.240702






