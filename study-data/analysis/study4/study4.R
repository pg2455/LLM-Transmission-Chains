library(tidyverse)
library(lme4) 
library(lmerTest) 
library(RColorBrewer) # with colour-blind-friendly palettes


# # prepare the coding document:
# n_content <- 3
# n_chains <- 5
# n_steps <- 5
# sim_data <- tibble(chain_step = factor(rep(1:n_steps, each = n_chains * n_content)),
#                   chain_id = factor(rep(rep(1:n_chains, each = n_content), n_steps)),
#                   content = rep(c("negative", "threat", "neutral"), n_chains * n_steps),
#                   count =  NA)
# 
# # re-order using chain_id so it is easy to code:
# sim_data <- arrange(sim_data, chain_id)
# 
# # export and code:
# write_csv(sim_data, "study4_Flash_Ultra.csv")

# process output:
sim_data <- read_csv("study4_Flash_Ultra.csv") # change name here and below in the plot
# find proportions:
sim_data <- sim_data %>%
  mutate(totals = case_when (content == "negative" ~ 2, 
                             content == "threat" ~ 2,
                             content == "neutral" ~ 4)) %>%
  mutate(proportion = count / totals)

# example plot (chains are averaged, content is separated):
sim_data %>%
  ggplot(aes(x=chain_step, y = proportion, colour = content)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = content, colour = content)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  scale_x_continuous(breaks = c(1,2,3,4,5)) +
  labs(title = "Threat-related") +
  theme_bw() +
  labs(title = "Study 4 - Flash Ultra Color")
ggsave("study4_Flash_Ultra.pdf", height = 5, width = 6)
  

# cumulative:
sim_data <- read_csv("study4_Lancer.csv")
sim_data2 <- read_csv("study4_Flash_Ultra.csv")
sim_data3 <- read_csv("study4_Nutane.csv")

sim_data <- sim_data %>%
  mutate(cumulative = sim_data$count + sim_data2$count + sim_data3$count) %>%
  mutate(totals = case_when (content == "negative" ~ 6, 
                             content == "threat" ~ 6,
                             content == "neutral" ~ 12)) %>%
  mutate(proportion = cumulative / totals)


sim_data %>%
  ggplot(aes(x=chain_step, y = proportion, colour = content)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = content, colour = content)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  theme_bw() +
  scale_x_continuous(breaks = c(1,2,3,4,5)) +
  labs(title = "Threat-related") +
  labs(title = "Study 4 - cumulative") +
  ggsave("study4_cumulative.pdf", height = 5, width = 6)


# change order of levels so the model use neutral has baseline
sim_data$content <- factor(sim_data$content, levels = c("neutral", "negative", "threat"))
out_model <- lmer(proportion ~ content + (1|chain_step) + (1|chain_id), data = sim_data)

summary(out_model)
#                 Estimate Std. Error       df t value Pr(>|t|)    
# contentnegative  0.07000    0.03677 68.00000   1.904  0.06120 .  
# contentthreat    0.52333    0.03677 68.00000  14.231  < 2e-16 ***


# TEST ONLY NEGATIVE VERSUS NEUTRAL:
sim_data$content <- factor(sim_data$content, levels = c("neutral", "negative"))
out_model <- lmer(proportion ~ content + (1|chain_step) + (1|chain_id), data = sim_data)

summary(out_model)
#                 Estimate Std. Error       df t value Pr(>|t|)    
# contentnegative  0.07000    0.02348 44.00000   2.981  0.00467 **

# plot for publication :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
pubPalette <- c("#999999", "#CCCCCC", "#E69F00")
sim_data %>%
  ggplot(aes(x=chain_step, y = proportion, colour = content)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = content, colour = content)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  scale_colour_manual(values = pubPalette) +
  theme_bw() +
  theme(legend.position = "none") +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3,4,5)) +
  labs(title = "Threat-related") +
  ylim(0,1) 
ggsave("../plot/study4.pdf", height = 4, width = 4)
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
