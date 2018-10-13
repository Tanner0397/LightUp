generate_table = read.table("generator.txt")
generate_repar_table = read.table("generator_repair.txt")
read_table = read.table("read.txt")
read_repair_table = read.table("read_repair.txt")

generate_average = data.frame(V1 = generate_table[[1]], V2 = generate_table[[2]])
generate_average_vector = generate_average[[2]]
generate_best = data.frame(V1 = generate_table[[1]], V2 = generate_table[[3]])
generate_best_vector = generate_best[[2]]

generate_repair_average = data.frame(V1 = generate_repar_table[[1]], V2 = generate_repar_table[[2]])
generate_repair_average_vector = generate_repair_average[[2]]
generate_repair_best = data.frame(V1 = generate_repar_table[[1]], V2 = generate_repar_table[[3]])
generate_repair_best_vector = generate_repair_best[[2]]

read_average = data.frame(V1 = read_table[[1]], V2 = read_table[[2]])
read_average_vector = read_average[[2]]
read_best = data.frame(V1 = read_table[[1]], V2 = read_table[[3]])
read_best_vector = read_best[[2]]

read_repair_average = data.frame(V1 = read_repair_table[[1]], V2 = read_repair_table[[2]])
read_repair_average_vector = read_repair_average[[2]]
read_repair_best = data.frame(V1 = read_repair_table[[1]], V2 = read_repair_table[[3]])
read_repair_best_vector = read_repair_best[[2]]

png(file = "gen_wo_repair.jpeg", width=700)
plot(type="s", generate_average, xlab="Evaluations", ylab="Fitness", main="Generated Puzzle without Repair Function\n Evaluations vs. Fitness\nBest Run from logs/logs.txt", col="red", ylim=c(0, 100))
#dev.off()
par(new=TRUE)
plot(type="s", generate_best, xlab="Evaluations", ylab="Fitness", main="", col="blue", yaxt="n" ,xaxt="n", ylim=c(0, 100))
legend("topright", legend=c("Average", "Best"), col=c("red", "blue"), lty=c(1, 1))
dev.off()

png(file = "gen_w_repair.jpeg", width=700)
plot(type="s", generate_repair_average, xlab="Evaluations", ylab="Fitness", main="Generated Puzzle with Repair Function\n Evaluations vs. Fitness\nBest Run from logs/log_w_repair.txt", col="red", ylim=c(0, 100))
#dev.off()
par(new=TRUE)
plot(type="s", generate_repair_best, xlab="Evaluations", ylab="Fitness", main="", col="blue", yaxt="n" ,xaxt="n", ylim=c(0, 100))
legend("topright", legend=c("Average", "Best"), col=c("red", "blue"), lty=c(1, 1))
dev.off()

png(file = "read_wo_repair.jpeg", width=700)
plot(type="s", read_average, xlab="Evaluations", ylab="Fitness", main="Provided Puzzle without Repair Function\n Evaluations vs. Fitness\nBest Run from logs/log_read_timer.txt", col="red", ylim=c(0, 40))
#dev.off()
par(new=TRUE)
plot(type="s", read_best, xlab="Evaluations", ylab="Fitness", main="", col="blue", yaxt="n" ,xaxt="n", ylim=c(0, 40))
legend("topright", legend=c("Average", "Best"), col=c("red", "blue"), lty=c(1, 1))
dev.off()

png(file = "read_w_repair.jpeg", width=700)
plot(type="s", read_repair_average, xlab="Evaluations", ylab="Fitness", main="Provided Puzzle with Repair Function\n Evaluations vs. Fitness\nBest Run from logs/log_read_w_repair.txt", col="red", ylim=c(0, 40))
#dev.off()
par(new=TRUE)
plot(type="s", read_repair_best, xlab="Evaluations", ylab="Fitness", main="", col="blue", yaxt="n" ,xaxt="n", ylim=c(0, 40))
legend("topright", legend=c("Average", "Best"), col=c("red", "blue"), lty=c(1, 1))
dev.off()


MEAN_gen_avg = mean(generate_average_vector)
SD_gen_avg = sd(generate_average_vector)

MEAN_gen_best = mean(generate_best_vector)
SD_gen_best = sd(generate_best_vector)

MEAN_gen_r_avg = mean(generate_repair_average_vector)
SD_gen_r_avg = sd(generate_repair_average_vector)

MEAN_gen_r_best = mean(generate_repair_best_vector)
SD_gen_r_best = sd(generate_repair_best_vector)

#-----------------

MEAN_read_avg = mean(read_average_vector)
SD_read_avg = sd(read_average_vector)

MEAN_read_best = mean(read_best_vector)
SD_read_best = sd(read_best_vector)

MEAN_read_r_avg = mean(read_repair_average_vector)
SD_read_r_avg = sd(read_repair_average_vector)

MEAN_read_r_best = mean(read_repair_best_vector)
SD_read_r_best = sd(read_repair_best_vector)


#----------- Statistical Analysis ------------

f_test_1 = var.test(unlist(generate_best_vector), unlist(generate_repair_best_vector))
f_test_2 = var.test(unlist(generate_average_vector), unlist(generate_repair_average_vector))
#print(f_test_1)
#print(f_test_2)

f_test_3 = var.test(unlist(read_best_vector), unlist(read_repair_best_vector))
f_test_4 = var.test(unlist(read_average_vector), unlist(read_repair_average_vector))
#print(f_test_3)
#print(f_test_4)

#---------------do t Test

t_test_1 = t.test(unlist(generate_best_vector), unlist(generate_repair_best_vector))
t_test_2 = t.test(unlist(generate_average_vector), unlist(generate_repair_average_vector))
t_test_3 = t.test(unlist(read_best_vector), unlist(read_repair_best_vector))
t_test_4 = t.test(unlist(read_average_vector), unlist(read_repair_average_vector))

print(t_test_1)
print(t_test_2)
print(t_test_3)
print(t_test_4)

