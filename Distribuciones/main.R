library("univariateML")
library("goftest")
library('nakagami')
library("vcd")
library("fGarch")
library("actuar")
library("fitdistrplus")

tev0 <- read.csv2(file='datos finales/tev0.csv', dec = '.')
tev1 <- read.csv2(file='datos finales/tev1.csv', dec = '.')
tev2 <- read.csv2(file='datos finales/tev2.csv', dec = '.')
tev3 <- read.csv2(file='datos finales/tev3.csv', dec = '.')
tev4 <- read.csv2(file='datos finales/tev4.csv', dec = '.')
tev5 <- read.csv2(file='datos finales/tev5.csv', dec = '.')
tev6 <- read.csv2(file='datos finales/tev6.csv', dec = '.')
tev7 <- read.csv2(file='datos finales/tev7.csv', dec = '.')
tev8 <- read.csv2(file='datos finales/tev8.csv', dec = '.')
tev9 <- read.csv2(file='datos finales/tev9.csv', dec = '.')
tev10 <- read.csv2(file='datos finales/tev10.csv', dec = '.')
tev11 <- read.csv2(file='datos finales/tev11.csv', dec = '.')
tev12 <- read.csv2(file='datos finales/tev12.csv', dec = '.')
tev13 <- read.csv2(file='datos finales/tev13.csv', dec = '.')
tev14 <- read.csv2(file='datos finales/tev14.csv', dec = '.')
tev15 <- read.csv2(file='datos finales/tev15.csv', dec = '.')
tev16 <- read.csv2(file='datos finales/tev16.csv', dec = '.')
tev17 <- read.csv2(file='datos finales/tev17.csv', dec = '.')
tev18 <- read.csv2(file='datos finales/tev18.csv', dec = '.')
tev19 <- read.csv2(file='datos finales/tev19.csv', dec = '.')
tev20 <- read.csv2(file='datos finales/tev20.csv', dec = '.')
tev21 <- read.csv2(file='datos finales/tev21.csv', dec = '.')
tev22 <- read.csv2(file='datos finales/tev22.csv', dec = '.')
tev23 <- read.csv2(file='datos finales/tev23.csv', dec = '.')

modelos_sin_naka <- univariateML_models
remove <- c ("naka")
modelos_sin_naka %in% remove
modelos_sin_naka <- modelos_sin_naka [! modelos_sin_naka %in% remove]

model_select(tev0$TEV, models = modelos_sin_naka, criterion = c("aic")) #GAMMA shape = 0.824484 rate = 0.002855
model_select(tev1$TEV, models = modelos_sin_naka, criterion = c("aic")) #EXP rate = 0.005502
model_select(tev2$TEV, models = modelos_sin_naka, criterion = c("aic")) #EXP rate = 0.00725
model_select(tev3$TEV, models = modelos_sin_naka, criterion = c("aic")) #GAMMA shape = 1.27188 rate = 0.01207  
model_select(tev4$TEV, models = modelos_sin_naka, criterion = c("aic")) #EXP rate = 0.01432
model_select(tev5$TEV, models = modelos_sin_naka, criterion = c("aic")) #EXP rate = 0.01471
model_select(tev6$TEV, models = modelos_sin_naka, criterion = c("aic")) #GAMMA shape = 0.82603, rate =  0.01754
model_select(tev7$TEV, models = modelos_sin_naka, criterion = c("aic")) #GAMMA shape = 0.76578 , rate = 0.06982 
model_select(tev8$TEV, models = modelos_sin_naka, criterion = c("aic")) #GAMMA shape = 0.69389, rate = 0.07052  
model_select(tev9$TEV, models = modelos_sin_naka, criterion = c("aic")) #GAMMA shape = 0.62622, rate = 0.06599
model_select(tev10$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape = 0.62801, rate = 0.06811
model_select(tev11$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.63640, rate =  0.06274
model_select(tev12$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.66237, rate =  0.06084
model_select(tev13$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.73307, rate =  0.06331  
model_select(tev14$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.7082, rate =  0.0562  
model_select(tev15$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.77401, rate =  0.05628  
model_select(tev16$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.70061  , rate =  0.04434  
model_select(tev17$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.77431, rate =  0.04419  
model_select(tev18$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.77036  , rate =  0.02449  
model_select(tev19$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.77329  , rate =  0.02159
model_select(tev20$TEV, models = modelos_sin_naka, criterion = c("aic"))#EXP rate = 0.02225
model_select(tev21$TEV, models = modelos_sin_naka, criterion = c("aic"))#EXP rate = 0.02002  
model_select(tev22$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.86502  , rate =  0.01323  
model_select(tev23$TEV, models = modelos_sin_naka, criterion = c("aic"))#GAMMA shape= 0.90140  , rate =  0.01195  


hist(tev0$TEV, main = "Tiempo entre eventos entre 00:00 y 00:59", freq = FALSE, breaks = 50)
lines(mlgamma(tev0$TEV), lwd = 2, col = "red")
ad.test(tev0$TEV, "gamma",  shape = 0.824484, rate = 0.002855)

qqmlplot(tev0$TEV, mlgamma, datax = TRUE, main = "QQ Plot for TEV19")
qqmlline(tev0$TEV, mlgamma, datax = TRUE)

hist(tev1$TEV, main = "Tiempo entre eventos entre 01:00 y 01:59", freq = FALSE, breaks = 50)
lines(mlgamma(tev1$TEV), lwd = 2, col = "red")
lines(mlexp(tev1$TEV), lwd = 2, col = "blue")
ad.test(tev1$TEV, "exp",  rate = 0.005502)

qqmlplot(tev1$TEV, mlexp, datax = TRUE, main = "QQ Plot for TEV19")
qqmlline(tev1$TEV, mlexp, datax = TRUE)

hist(tev2$TEV, main = "Tiempo entre eventos entre 02:00 y 02:59", freq = FALSE, breaks = 50, xlim = c(0, 500),  ylim = c(0, 0.01))
lines(mlgamma(tev2$TEV), lwd = 2, col = "red")
lines(mlweibull(tev2$TEV), lwd = 2, col = "green")
lines(mlexp(tev2$TEV), lwd = 2, col = "blue")
ad.test(tev2$TEV, "exp",  rate = 0.00725  )

qqmlplot(tev2$TEV, mlexp, datax = TRUE, main = "QQ Plot for TEV19")
qqmlline(tev2$TEV, mlexp, datax = TRUE)

ppmlplot(tev2$TEV, mlexp, main = "Many P-P plots", datax = TRUE)
ppmlpoints(tev2$TEV, mlnorm, col = "blue", datax = TRUE)
ppmlpoints(tev2$TEV, mlexp, col = "red", datax = TRUE)


hist(tev3$TEV, main = "Tiempo entre eventos entre 03:00 y 03:59", freq = FALSE, breaks = 50, xlim = c(0, 500),  ylim = c(0, 0.01))
lines(mlgamma(tev3$TEV), lwd = 2, col = "red")
lines(mlexp(tev3$TEV), lwd = 2, col = "blue")
ad.test(tev3$TEV, "pgamma",  shape = 1.27188, rate = 0.01207 )


hist(tev4$TEV, main = "Tiempo entre eventos entre 04:00 y 04:59", freq = FALSE, breaks = 50)
lines(mlexp(tev4$TEV), lwd = 2, col = "red")
ad.test(tev4$TEV, "pexp",  rate = 0.01432 )


hist(tev5$TEV, main = "Tiempo entre eventos entre 05:00 y 05:59", freq = FALSE, breaks = 100)
lines(mlgamma(tev5$TEV), lwd = 2, col = "red")
lines(mlexp(tev5$TEV), lwd = 2, col = "blue")

tev5_AIC <- AIC(mlbetapr(tev5$TEV),
                mlexp(tev5$TEV),
                mlinvgamma(tev5$TEV),
                mlgamma(tev5$TEV),
                mllnorm(tev5$TEV),
                mlinvgauss(tev5$TEV),
                mlweibull(tev5$TEV),
                mlrayleigh(tev5$TEV))
mlexp(tev5$TEV)
mlgamma(tev5$TEV)
ad.test(tev5$TEV, "pexp",  rate = 0.01471  )

hist(tev6$TEV, main = "Tiempo entre eventos entre 06:00 y 06:59", freq = FALSE, breaks = 100)
lines(mlgamma(tev6$TEV), lwd = 2, col = "red")
lines(mlexp(tev6$TEV), lwd = 2, col = "blue")
ad.test(tev6$TEV, "pgamma",  shape = 0.82603, rate =  0.01754)

hist(tev7$TEV, main = "Tiempo entre eventos entre 07:00 y 07:59", freq = FALSE, breaks = 100 )
lines(mlgamma(tev7$TEV), lwd = 2, col = "red")
lines(mlexp(tev7$TEV), lwd = 2, col = "blue")
ad.test(tev7$TEV, "pgamma",  shape = 0.76578 , rate = 0.06982 )

hist(tev8$TEV, main = "Tiempo entre eventos entre 08:00 y 08:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev8$TEV), lwd = 2, col = "red")
lines(mlexp(tev8$TEV), lwd = 2, col = "blue")
ad.test(tev8$TEV, "pgamma", shape = 0.69389, rate = 0.07052)

hist(tev9$TEV, main = "Tiempo entre eventos entre 09:00 y 09:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev9$TEV), lwd = 2, col = "red")
lines(mlexp(tev9$TEV), lwd = 2, col = "blue")
ad.test(tev9$TEV, "pgamma", shape = 0.62622, rate = 0.06599)

hist(tev10$TEV, main = "Tiempo entre eventos entre 10:00 y 10:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev10$TEV), lwd = 2, col = "red")
lines(mlexp(tev10$TEV), lwd = 2, col = "blue")
ad.test(tev10$TEV, "pgamma", shape = 0.62801, rate = 0.06811 )

hist(tev11$TEV, main = "Tiempo entre eventos entre 11:00 y 11:59", freq = FALSE, breaks = 100 )
lines(mlgamma(tev11$TEV), lwd = 2, col = "red")
lines(mlexp(tev11$TEV), lwd = 2, col = "blue")
ad.test(tev11$TEV, "pgamma", shape = 0.63640, rate = 0.06274)

hist(tev12$TEV, main = "Tiempo entre eventos entre 12:00 y 12:59", freq = FALSE, breaks = 100 )
lines(mlgamma(tev12$TEV), lwd = 2, col = "red")
lines(mlexp(tev12$TEV), lwd = 2, col = "blue")
ad.test(tev12$TEV, "pgamma", shape = 0.66237, rate = 0.06084)

hist(tev13$TEV, main = "Tiempo entre eventos entre 13:00 y 13:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev13$TEV), lwd = 2, col = "red")
ad.test(tev13$TEV, "pgamma", shape= 0.73307, rate =  0.06331 )

hist(tev14$TEV, main = "Tiempo entre eventos entre 14:00 y 14:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev14$TEV), lwd = 2, col = "red")
ad.test(tev14$TEV, "pgamma", shape= 0.7082, rate =  0.0562)

hist(tev15$TEV, main = "Tiempo entre eventos entre 15:00 y 15:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev15$TEV), lwd = 2, col = "red")
ad.test(tev15$TEV, "gamma", shape= 0.77401, rate =  0.05628)

hist(tev16$TEV, main = "Tiempo entre eventos entre 16:00 y 16:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev16$TEV), lwd = 2, col = "red")
ad.test(tev16$TEV, "gamma", shape= 0.70061  , rate =  0.04434)

# DE AQUI PARA ARRIBA TODO LISTO
hist(tev17$TEV, main = "Tiempo entre eventos entre 17:00 y 17:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev17$TEV), lwd = 2, col = "red")
ad.test(tev17$TEV, "gamma", shape= 0.77431    , rate =  0.04419)

hist(tev18$TEV, main = "Tiempo entre eventos entre 18:00 y 18:59", freq = FALSE, breaks = 50)
lines(mlgamma(tev18$TEV), lwd = 2, col = "red")
ad.test(tev18$TEV, "gamma", shape= 0.77036, rate =  0.02449)

hist(tev19$TEV, main = "Tiempo entre eventos entre 19:00 y 19:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev19$TEV), lwd = 2, col = "red")
ad.test(tev19$TEV, "gamma", shape= 0.77329  , rate =  0.02159)

hist(tev20$TEV, main = "Tiempo entre eventos entre 20:00 y 20:59", freq = FALSE, breaks = 50 )
lines(mlexp(tev20$TEV), lwd = 2, col = "blue")
ad.test(tev20$TEV, "pexp", rate =  0.02225)

hist(tev21$TEV, main = "Tiempo entre eventos entre 21:00 y 21:59", freq = FALSE, breaks = 50 )
lines(mlexp(tev21$TEV), lwd = 2, col = "blue")
ad.test(tev21$TEV, "pexp", rate =  0.02002)

hist(tev22$TEV, main = "Tiempo entre eventos entre 22:00 y 22:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev22$TEV), lwd = 2, col = "red")
ad.test(tev22$TEV, "pgamma", shape= 0.86502    , rate =  0.01323)

hist(tev23$TEV, main = "Tiempo entre eventos entre 23:00 y 23:59", freq = FALSE, breaks = 50 )
lines(mlgamma(tev23$TEV), lwd = 2, col = "red")
ad.test(tev23$TEV, "pgamma", shape= 0.90140, rate = 0.01195)


qqmlplot(tev21$TEV, mlexp, datax = TRUE, main = "QQ Plot for TEV19")
qqmlline(tev21$TEV, mlexp, datax = TRUE)

qqmlplot(tev23$TEV, mlgamma, datax = TRUE, main = "QQ Plot for TEV19")
qqmlline(tev23$TEV, mlgamma, datax = TRUE)







#TIEMPOS DE ATENCION

eventos = read.csv2(file='../Simulacion/datos/eventos.csv', dec = '.')
summary(eventos$ATENCION)

model_select(eventos$ATENCION, models = modelos_sin_naka, criterion = c("aic"))


mlsged(eventos$ATENCION)
mlinvgauss(eventos$ATENCION)
ad.test(eventos$ATENCION, null= "psged", mean = 16.534, sd=10.181 ,  nu = 1.547, xi = 76.760)
ad.test(eventos$ATENCION, null= "pinvgauss" , mean = 16.48 , shape= 35.64 )


hist(eventos$ATENCION, main = "Histograma tiempos de atención", freq = FALSE, breaks = 50, xlim = c(0, 50),ylim = c(0,0.06), xlab="Minutos", ylab="Densidad")

lines(mlinvgauss(eventos$ATENCION), lwd = 2, col = "blue")
lines(dsged(c(0:100),mean = 16.534, sd=10.181 ,  nu = 1.547, xi = 76.760), lwd=2, col= "red")
lines(dsged(c(0:100),mean = 12.334, sd=10.181 ,  nu = 1.547, xi = 76.770), lwd=2, col= "red")
legend("topright", legend=c("Distribución de Error Generalizado Sesgado", "Distribución Gaussiana Inversa"),
       col=c("red", "blue"), lty=1:1, lwd = 2)




diezmilRSGED <- rsged(10000, mean = 16.534, sd=10.181 ,  nu = 1.547, xi = 76.760)
summary(diezmilRSGED)
write.csv(diezmilRSGED,'muestraSGED.csv', row.names = FALSE)
hist(diezmilRSGED, main = "Histograma SGED", freq = FALSE, breaks = 50, xlim = c(0, 50),ylim = c(0,0.06), xlab="Minutos", ylab="Densidad")

qqmlplot(eventos$ATENCION, mlinvgauss, datax = TRUE, main = "QQ Plot ")
qqmlline(eventos$ATENCION, mlinvgauss, datax = TRUE)


comparacion_akaik <- AIC(
    mlcauchy(eventos$ATENCION),
    mlgumbel(eventos$ATENCION),
    mllaplace(eventos$ATENCION),
    mlnorm(eventos$ATENCION),
    mlstd(eventos$ATENCION),
    mlsged(eventos$ATENCION),
    mlged(eventos$ATENCION),
    mlsnorm(eventos$ATENCION),
    mlsstd(eventos$ATENCION),
    mlsged(eventos$ATENCION),
    mlbetapr(eventos$ATENCION),
    mlexp(eventos$ATENCION),
    mlgamma(eventos$ATENCION),
    mlinvgamma(eventos$ATENCION),
    mlinvgauss(eventos$ATENCION),
    mlinvweibull(eventos$ATENCION),
    mllnorm(eventos$ATENCION),
    mlunif(eventos$ATENCION),
    mlpower(eventos$ATENCION)
)

# Stats Atencion

fit.SGED <- fitdist(eventos$ATENCION, method = "mle", distr="sged", start = list(mean = 16.534, sd=10.181 ,  nu = 1.547, xi = 76.760  ))
plot(fit.SGED)
gofstat(fit.SGED)

fit.INVGAUSSIANA <- fitdist(eventos$ATENCION, method = "mle", distr="invgauss", start = list(mean = 16.48 , shape= 35.64))
plot(fit.INVGAUSSIANA)
gofstat(fit.INVGAUSSIANA)

# PARA TEV

fit_tev0 <- fitdist(tev0$TEV, method = "mle", distr="gamma", start = list(shape = 0.824484, rate = 0.002855))
plot(fit_tev0)
gofstat(fit_tev0)

fit_tev1 <- fitdist(tev1$TEV, method = "mle", distr="exp", start = list(rate = 0.005502))
plot(fit_tev1)
gofstat(fit_tev1)

fit_tev2 <- fitdist(tev2$TEV, method = "mle", distr="exp", start = list(rate = 0.00725))
plot(fit_tev2)
gofstat(fit_tev2)

fit_tev3 <- fitdist(tev3$TEV, method = "mle", distr="gamma", start = list(shape = 1.27188, rate = 0.01207))
plot(fit_tev3)
gofstat(fit_tev3)

fit_tev4 <- fitdist(tev4$TEV, method = "mle", distr="exp", start = list(rate = 0.01432))
plot(fit_tev4)
gofstat(fit_tev4)

fit_tev5 <- fitdist(tev5$TEV, method = "mle", distr="exp", start = list(rate = 0.01471))
plot(fit_tev5)
gofstat(fit_tev5)


fit_tev6 <- fitdist(tev6$TEV, method = "mle", distr="gamma", start = list(shape = 0.82603, rate =  0.01754))
plot(fit_tev6)
gofstat(fit_tev6)

fit_tev7 <- fitdist(tev7$TEV, method = "mle", distr="gamma", start = list(shape = 0.76578, rate =  0.06982))
plot(fit_tev7)
gofstat(fit_tev7)

fit_tev8 <- fitdist(tev8$TEV, method = "mle", distr="gamma", start = list(shape = 0.69389, rate =  0.07052))
plot(fit_tev8)
gofstat(fit_tev8)

fit_tev9 <- fitdist(tev9$TEV, method = "mle", distr="gamma", start = list(shape = 0.62622, rate =  0.06599))
plot(fit_tev9)
gofstat(fit_tev9)


fit_tev10 <- fitdist(tev10$TEV, method = "mle", distr="gamma", start = list(shape = 0.62801, rate = 0.06811))
plot(fit_tev10)
gofstat(fit_tev10)








fit_tev11 <- fitdist(tev11$TEV, method = "mle", distr="gamma", start = list(shape = 0.63640, rate = 0.06274))
plot(fit_tev11)
gofstat(fit_tev11)

fit_tev12 <- fitdist(tev12$TEV, method = "mle", distr="gamma", start = list(shape = 0.66237, rate = 0.06084))
plot(fit_tev12)
gofstat(fit_tev12)

fit_tev13 <- fitdist(tev13$TEV, method = "mle", distr="gamma", start = list(shape= 0.73307, rate =  0.06331 ))
plot(fit_tev13)
gofstat(fit_tev13)

fit_tev14 <- fitdist(tev14$TEV, method = "mle", distr="gamma", start = list(shape= 0.7082, rate =  0.0562))
plot(fit_tev14)
gofstat(fit_tev14)

fit_tev15 <- fitdist(tev15$TEV, method = "mle", distr="gamma", start = list(shape = 0.77401, rate =  0.05628))
plot(fit_tev15)
gofstat(fit_tev15)

fit_tev16 <- fitdist(tev16$TEV, method = "mle", distr="gamma", start = list(shape= 0.70061  , rate =  0.04434))
plot(fit_tev16)
gofstat(fit_tev16)

fit_tev17 <- fitdist(tev17$TEV, method = "mle", distr="gamma", start = list(shape= 0.77431, rate =  0.04419))
plot(fit_tev17)
gofstat(fit_tev17)

fit_tev18 <- fitdist(tev18$TEV, method = "mle", distr="gamma", start = list(shape= 0.77036  , rate =  0.02449))
plot(fit_tev18)
gofstat(fit_tev18)

fit_tev19 <- fitdist(tev19$TEV, method = "mle", distr="gamma", start = list(shape= 0.77329  , rate =  0.02159))
plot(fit_tev19)
gofstat(fit_tev19)

fit_tev20 <- fitdist(tev20$TEV, method = "mle", distr="exp", start = list(rate = 0.02225))
plot(fit_tev20)
gofstat(fit_tev20)

fit_tev21 <- fitdist(tev21$TEV, method = "mle", distr="exp", start = list(rate = 0.02002 ))
plot(fit_tev21)
gofstat(fit_tev21)

fit_tev22 <- fitdist(tev22$TEV, method = "mle", distr="gamma", start = list(shape= 0.86502  , rate =  0.01323))
plot(fit_tev22)
gofstat(fit_tev22)

fit_tev23 <- fitdist(tev23$TEV, method = "mle", distr="gamma", start = list(shape= 0.90140  , rate =  0.01195))
plot(fit_tev23)
gofstat(fit_tev23)


# Entrega 3

mean_diario <- read.csv2(file='../Simulacion/entrega3/estabilizacion/mean_diario.csv', dec = '.')
plot(mean_diario$DIA, mean_diario$TIEMPO_DESPACHO,main = "Tiempo promedio despacho", type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(mean_diario$DIA, mean_diario$TIEMPO_ATENCION, main = "Tiempo promedio atencion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos", ylim = c(15,17))
plot(mean_diario$DIA, mean_diario$TIEMPO_DERIVACION, main = "Tiempo promedio derivacion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(mean_diario$DIA, mean_diario$TIEMPO_ATRASO, main = "Tiempo promedio atraso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(mean_diario$DIA, mean_diario$TIEMPO_PROCESO, main = "Tiempo promedio proceso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")

diario25 <- read.csv2(file='../Simulacion/entrega3/estabilizacion/25%_diario.csv', dec = '.')
plot(diario25$DIA, diario25$TIEMPO_DESPACHO,main = "Tiempo 25% despacho", type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario25$DIA, diario25$TIEMPO_ATENCION, main = "Tiempo 25% atencion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos",ylim = c(7,9))
plot(diario25$DIA, diario25$TIEMPO_DERIVACION, main = "Tiempo 25% derivacion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos",ylim = c(14,18))
plot(diario25$DIA, diario25$TIEMPO_ATRASO, main = "Tiempo 25% atraso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario25$DIA, diario25$TIEMPO_PROCESO, main = "Tiempo 25% proceso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")

diario50 <- read.csv2(file='../Simulacion/entrega3/estabilizacion/50%_diario.csv', dec = '.')
plot(diario50$DIA, diario50$TIEMPO_DESPACHO,main = "Tiempo 50% despacho", type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario50$DIA, diario50$TIEMPO_ATENCION, main = "Tiempo 50% atencion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos", ylim = c(12,15))
plot(diario50$DIA, diario50$TIEMPO_DERIVACION, main = "Tiempo 50% derivacion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario50$DIA, diario50$TIEMPO_ATRASO, main = "Tiempo 50% atraso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario50$DIA, diario50$TIEMPO_PROCESO, main = "Tiempo 50% proceso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")

diario75 <- read.csv2(file='../Simulacion/entrega3/estabilizacion/75%_diario.csv', dec = '.')
plot(diario75$DIA, diario75$TIEMPO_DESPACHO,main = "Tiempo 75% despacho", type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario75$DIA, diario75$TIEMPO_ATENCION, main = "Tiempo 75% atencion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos",ylim = c(19,22))
plot(diario75$DIA, diario75$TIEMPO_DERIVACION, main = "Tiempo 75% derivacion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario75$DIA, diario75$TIEMPO_ATRASO, main = "Tiempo 75% atraso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario75$DIA, diario75$TIEMPO_PROCESO, main = "Tiempo 75% proceso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")

diario90 <- read.csv2(file='../Simulacion/entrega3/estabilizacion/90%_diario.csv', dec = '.')
plot(diario90$DIA, diario90$TIEMPO_DESPACHO,main = "Tiempo 90% despacho", type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario90$DIA, diario90$TIEMPO_ATENCION, main = "Tiempo 90% atencion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos",ylim = c(28,30))
plot(diario90$DIA, diario90$TIEMPO_DERIVACION, main = "Tiempo 90% derivacion",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario90$DIA, diario90$TIEMPO_ATRASO, main = "Tiempo 90% atraso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")
plot(diario90$DIA, diario90$TIEMPO_PROCESO, main = "Tiempo 90% proceso",type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")

# Nuevas VA

hist(eventos$DESPACHO, main = "Histograma tiempos despacho", freq = FALSE, breaks = 50, xlab="Minutos", ylab="Densidad")
model_select(eventos$DESPACHO, models = modelos_sin_naka, criterion = c("aic"))
lines(dsged(c(0:100),mean = 4.153, sd=3.114 ,  nu = 1.318, xi = 107.802  ), lwd=2, col= "red")

muestraDespacho <- rsged(10000, mean = 4.153, sd=3.114 ,  nu = 1.318, xi = 107.802)
summary(muestraDespacho)
write.csv(muestraDespacho,'muestraDespacho.csv', row.names = FALSE)
hist(muestraDespacho, main = "Histograma Despacho", freq = FALSE, breaks = 50, xlab="Minutos", ylab="Densidad")

muestraDerivacion <- rsged(10000, mean = 11.303, sd=6.764  ,  nu = 1.512, xi = 2327.423)
summary(muestraDerivacion)
write.csv(muestraDerivacion,'muestraDerivacion.csv', row.names = FALSE)
hist(muestraDerivacion, main = "Histograma Derivacion", freq = FALSE, breaks = 50,  xlab="Minutos", ylab="Densidad")

despachoFiltrado <- read.csv2(file='../Simulacion/datos/muestraDespachofiltrada.csv', dec = '.')
derivacionFiltrado <- read.csv2(file='../Simulacion/datos/muestraDerivacionfiltrada.csv', dec = '.')
summary(despachoFiltrado)
summary(derivacionFiltrado)

# Estabilizacion v6 base vs cercanos
casobase_v6_mean <- read.csv2(file='../Simulacion/entrega3/cores/0/mean_diario.csv', dec = '.')
plot(casobase_v6_mean$DIA, casobase_v6_mean$TIEMPO_PROCESO,main = "Promedio proceso base", type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos", ylim = c(100,250))

casobase_v6_95 <- read.csv2(file='../Simulacion/entrega3/cores/0/95%_diario.csv', dec = '.')
lines(casobase_v6_95$DIA, casobase_v6_95$TIEMPO_PROCESO,main = "95% proceso base", type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")

caso4_v6_95 <- read.csv2(file='../Simulacion/entrega3/cores/4/95%_diario.csv', dec = '.')
plot(caso4_v6_95$DIA, caso4_v6_95$TIEMPO_PROCESO,main = "95% proceso caso 4", type = "b", pch = 19, col = "red", xlab = "Dias", ylab = "Minutos")

lines(caso4_v6_95$DIA, caso4_v6_95$TIEMPO_PROCESO, type = "b", pch = 19, col = "blue",)

