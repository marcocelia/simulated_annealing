net <- read.table("./data/Zachary_Karate_club.txt", quote="\"", comment.char="")
vertices=sort(unique(unlist(net)))
n=length(vertices)

# modularity function
modularity=function(net=net, solution=solution){

  vertices=sort(unique(unlist(net)))
  n=length(vertices)
  L=nrow(net)
  Ki=table(unlist(net))
  Ki=as.vector(unname(Ki))

  linksCOM=net
  linksCOM=cbind(solution[linksCOM[,1]], solution[linksCOM[,2]])

  e=c()
  for(i in 1:2){
    subi=subset(linksCOM,linksCOM[,1]==i & linksCOM[,2]==i)
    e[i]=nrow(subi)
  }
  er=e/L
  matrCOMK=cbind(solution,Ki)

  a=c()
  for(i in 1:2){
    subi=subset(matrCOMK,matrCOMK[,1]==i)
    a[i]=sum(subi[, 2])
  }
  ar=a/(2*L)
  ar2=ar^2
  modul=sum(er-ar2)
  return(modul)
}

cmppysol<-function(rsol, pysol, flip=T){
  if (flip){
    for (i in 1:length(pysol)) {
      pysol[i] = ifelse(pysol[i]==1,2,1)
    }
  }
  return(cbind(1:length(rsol),rsol-pysol))
}


modularityVEC=c()
nsim=600;
for(i in 1:nsim){
  sol=sample(c(1,2),n,replace=T)
  modularityVEC[i]=modularity(net,sol)
}

dis=c()
for(i in 1:(nsim-1)){
  for(j in (i+1):nsim){
    disttemp=abs(modularityVEC[i]- modularityVEC[j])
    dis=append(dis,disttemp)
   }
}

mm=mean(dis)
T0=100*mm
Tf = mm/100
nsim = 50000
A = T0
B = log(Tf/A)/nsim
Temp=A*exp(B*(1:nsim))

modularityPROC = c()
sol=sample(c(1,2),n,replace=T)
solNEW = sol
modularityBEST=modularity(net, solNEW)

for(t in 1:nsim){
  nodeRAN=sample(1:n,1)
  solNEW[nodeRAN]=ifelse(sol[nodeRAN]==1, 2, 1)
  modularityNEW=modularity(net, solNEW)
  if(modularityNEW >= modularityBEST){
    sol=solNEW
    modularityBEST=modularityNEW
  }else{
    diff=modularityBEST-modularityNEW
    p=exp(-diff/Temp[t])
    ran=runif(1)
    if(ran<=p){
      sol=solNEW
      modularityBEST=modularityNEW
    }
  }
  modularityPROC[t]=modularityBEST
}

plot(modularityPROC, type = "p")
