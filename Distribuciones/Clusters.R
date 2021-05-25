
########## CALCULAR CANTIDAD DE CLUSTERS ############

library(tidyverse)  # data manipulation
library(cluster)    # clustering algorithms
library(factoextra) # clustering algorithms & visualization

data <- read.csv2(file.choose())
datos <- as.data.frame(data)

#PASAR LAS COLUMNAS A NUM #######

datos$ATENCION <- as.numeric(as.character(datos$ATENCION))
datos$COORDENADA_X <- as.numeric(as.character(datos$COORDENADA_X))
datos$COORDENADA_Y <- as.numeric(as.character(datos$COORDENADA_Y))
coordenadas <- select(datos, COORDENADA_X, COORDENADA_Y)

####   Elbow method
# function to compute total within-cluster sum of square 
wss <- function(k) {
  kmeans(coordenadas, k, nstart = 20 )$tot.withinss
}

# Compute and plot wss for k = 1 to k = 15
k.values <- 1:15

# extract wss for 2-15 clusters
wss_values <- map_dbl(k.values, wss)

plot(k.values, wss_values,
     type="b", pch = 19, frame = FALSE, 
     xlab="Number of clusters K",
     ylab="Total within-clusters sum of squares")


####  Avergage slhouette method
# function to compute average silhouette for k clusters
avg_sil <- function(k) {
  km.res <- kmeans(coordenadas, centers = k, nstart = 25)
  ss <- silhouette(km.res$cluster, dist(coordenadas))
  mean(ss[, 3])
}

# Compute and plot wss for k = 2 to k = 15
k.values <- 2:15

# extract avg silhouette for 2-15 clusters
avg_sil_values <- map_dbl(k.values, avg_sil)

plot(k.values, avg_sil_values,
     type = "b", pch = 19, frame = FALSE, 
     xlab = "Number of clusters K",
     ylab = "Average Silhouettes")

#### Gap stat method   
gap_stat <- clusGap(coordenadas, FUN = kmeans, nstart = 25,
                    K.max = 15, B = 50)   
#NO CORRER, SE DEMORA AÑOS #HACER MENOS B ?

#POR SILHOUETTE ELEGIMOS 9

######### SEPARAR CLUSTERS  ##########
library(tidyverse)
library(ggpubr)
library(SuppDists)
library(magrittr)
library(dplyr)
library(ggplot2)

#Para 9 clusters
km_clusters_9 <- kmeans(x = coordenadas, centers = 9, nstart = 40)
datos9 <- coordenadas %>% mutate(cluster = km_clusters_9$cluster)
ggplot(data = datos9, aes(x = COORDENADA_X, y = COORDENADA_Y, color = as.factor(cluster))) +
  geom_point(size = 0.001) +
  labs(title = "Kmeans con k=9") +
  theme_bw()  +
theme(legend.title = element_text(colour="black", size=10, face="bold")) +
  theme(legend.text = element_text(colour="black", size=10, face="bold"))
p9

#Para 11 clusters
km_clusters_11 <- kmeans(x = coordenadas, centers = 11, nstart = 40)
datos11 <- coordenadas %>% mutate(cluster = km_clusters_11$cluster)
ggplot(data = datos11, aes(x = COORDENADA_X, y = COORDENADA_Y, color = as.factor(cluster))) +
  geom_point(size = 0.02) +
  labs(title = "Kmeans con k=11") +
  theme_bw() +
  theme(legend.title = element_text(colour="black", size=10, face="bold")) +
  theme(legend.text = element_text(colour="black", size=10, face="bold"))
p11

#Guarda la tabla como csv
write.table(datos9,file="9clusters.csv",sep=';',row.name=FALSE)
write.csv(datos9, file="9clusters2.csv")

#eventos9 <- read.csv2(file.choose())
eventos9 <- cbind(datos,datos9$cluster)
eventos9 <- as.data.frame(eventos9)
names(eventos9)[names(eventos9) == 'datos9$cluster'] <- 'cluster'