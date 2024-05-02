library(tidyverse)
library(lme4) 
library(lmerTest) 
library(RColorBrewer) # with colour-blind-friendly palettes



sim_data <- read_csv("study2.csv")

# find proportions:

sim_data <- sim_data %>%
  add_column(totals = 8) %>%
  mutate(proportion = count / totals)

# example plot (chains are averaged, content is separated):
sim_data %>%
  ggplot(aes(x=chain_step, y = proportion, colour = content)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = content, colour = content)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  theme_bw() +
  labs(title = "Study 2")
ggsave("study2.pdf", height = 5, width = 6)

# change order of levels so the model test negative content (instead of positive)
sim_data$content <- factor(sim_data$content, levels = c("positive", "negative"))

out_model <- lmer(proportion ~ content + (1|chain_step) + (1|chain_id), data = sim_data)

summary(out_model)
#                 Estimate Std. Error       df t value Pr(>|t|)    
# contentnegative  0.11667    0.02190 22.00000   5.326  2.4e-05 ***



# # prepare the coding document for the ambiguous sentences resolution:
# n_content <- 3
# n_chains <- 5
# n_steps <- 3
# sim_data <- tibble(chain_step = factor(rep(1:n_steps, each = n_chains * n_content)),
#                   chain_id = factor(rep(rep(1:n_chains, each = n_content), n_steps)),
#                   content = rep(c("negative", "positive", "neutral"), n_chains * n_steps),
#                   count =  NA)
# 
# # re-order using chain_id so it is easy to code:
# sim_data <- arrange(sim_data, chain_id)
# 
# # export and code:
# write_csv(sim_data, "study2_ambiguous.csv")


sim_data <- read_csv("study2_ambiguous.csv")
# find proportions:

sim_data <- sim_data %>%
  add_column(totals = 8) %>%
  mutate(proportion = count / totals)

# example plot (chains are averaged, content is separated):
sim_data %>%
  ggplot(aes(x=chain_step, y = proportion, colour = content)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = content, colour = content)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  theme_bw() +
  labs(title = "Study 2 - ambiguous resolution")
ggsave("study2_ambiguous.pdf", height = 5, width = 6)

sim_data$content <- factor(sim_data$content, levels = c("neutral", "positive", "negative"))

out_model <- lmer(proportion ~ content + (1|chain_step) + (1|chain_id), data = sim_data)

summary(out_model)
#                 Estimate Std. Error       df t value Pr(>|t|)    
# contentpositive -0.02500    0.02610 42.00000  -0.958  0.34362    
# contentnegative  0.18333    0.02610 42.00000   7.024 1.34e-08 ***
