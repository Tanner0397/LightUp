runs = 30

#Generate List
runs_gen = vector(mode = "list", length = runs)
runs_read = vector(mode = "list", length = runs)

for (i in 1:runs)
{
  run_g = read.table(paste("1b_gen/run", paste(toString(i), ".txt", sep=""), sep=""))
  run_r = read.table(paste("1b_read/run", paste(toString(i), ".txt", sep=""), sep=""))
  runs_gen[[i]] <- run_g
  runs_read[[i]] <- run_r
}

runs_gen_average = matrix(nrow = 991)
runs_read_average = matrix(nrow = 991)
runs_gen_best = matrix(nrow = 991)
runs_read_best = matrix(nrow = 991)

#Make column vectors
for (i in 1:runs)
{
  runs_gen_average <- cbind(as.matrix(unlist(runs_gen[[i]][[2]])), runs_gen_average)
  runs_read_average <- cbind(as.matrix(unlist(runs_read[[i]][[2]])), runs_read_average)
  runs_gen_best <- cbind(as.matrix(unlist(runs_gen[[i]][[3]])), runs_gen_best)
  runs_read_best <- cbind(as.matrix(unlist(runs_read[[i]][[3]])), runs_read_best)
}

#remove last column
runs_gen_average <- runs_gen_average[, -31]
runs_read_average <- runs_read_average[, -31]
runs_gen_best <- runs_gen_best[, -31]
runs_read_best <- runs_read_best[, -31]

read_average_average_vector = as.vector(rowMeans(runs_read_average))
read_average_best_vector = as.vector(rowMeans(runs_read_best))

gen_average_average_vector = as.vector(rowMeans(runs_gen_average))
gen_average_best_vector = as.vector(rowMeans(runs_gen_best))

#I know for a fact all runs have the exact same number of evaluations, so this will be valid
evals_vector = as.vector(unlist(runs_gen[[1]][[1]]))

data_gen_average = data.frame(V1=evals_vector, V2=gen_average_average_vector)
data_gen_best = data.frame(V1=evals_vector, V2=gen_average_best_vector)

data_read_average = data.frame(V1=evals_vector, V2=read_average_average_vector)
data_read_best = data.frame(V1=evals_vector, V2=read_average_best_vector)

png(file = "gen.jpeg", width=700)
plot(type="s", data_gen_average, xlab="Evaluations", ylab="Fitness", main="Generated Puzzle\nFitness vs. Evaluations averaged across all runs.\n logs/log.txt", col="red", ylim=c(0, 100))
#dev.off()
par(new=TRUE)
plot(type="s", data_gen_best, xlab="Evaluations", ylab="Fitness", main="", col="blue", yaxt="n" ,xaxt="n", ylim=c(0, 100))
legend("topright", legend=c("Average", "Best"), col=c("red", "blue"), lty=c(1, 1))
dev.off()

par(new=FALSE)

png(file = "read.jpeg", width=700)
plot(type="s", data_read_average, xlab="Evaluations", ylab="Fitness", main="Provided Puzzle\nFitness vs. Evaluations averaged across all runs\n logs/log_read_timer.txt", col="red", ylim=c(0, 45))
par(new=TRUE)
plot(type="s", data_read_best, xlab="Evaluations", ylab="Fitness", main="", col="blue", yaxt="n", xaxt="n", ylim=c(0, 45))
legend("topright", legend=c("Average", "Best"), col=c("red", "blue"), lty=c(1, 1))
dev.off()

one_a_local_best = read.table("1a_best_local.txt")
one_b_local_best = read.table("1b_best_local.txt")

a_mean = mean(as.numeric(unlist(one_a_local_best[1])))
a_sd = sd(as.numeric(unlist(one_a_local_best[1])))

b_mean = mean(as.numeric(unlist(one_b_local_best[1])))
b_sd = sd(as.numeric(unlist(one_b_local_best[1]))) 

print(a_mean)
print(a_sd)
print(b_mean)
print(b_sd)

f_test = var.test(unlist(one_a_local_best[1]), unlist(one_b_local_best[1]))
print(f_test)

#t test for R assumes variances are unequal to begin with
#R also assumes two-sided by default
ttest = t.test(unlist(one_a_local_best[1]), unlist(one_b_local_best[1]))
print(ttest)

