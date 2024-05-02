library(tidyverse)
library(lme4) 
library(lmerTest) 
library(RColorBrewer) # with colour-blind-friendly palettes



sim_data <- read_csv("study3.csv")
# there is an empty column in the original file:
sim_data <- sim_data %>%
  mutate(X5 = NULL) 

# find proportions:

sim_data <- sim_data %>%
  add_column(totals = 14) %>%
  mutate(proportion = count / totals)

# example plot (chains are averaged, content is separated):
sim_data %>%
  ggplot(aes(x=chain_step, y = proportion, colour = content)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = content, colour = content)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  theme_bw() +
  labs(title = "Study 3") 
ggsave("study3.pdf", height = 5, width = 6)


# group content together
data_content_aggr <- sim_data %>%
  add_column(social = NA) %>%
  mutate(information = if_else(content == "Goss" | content == "Social", 
                              "social", "non social")) %>%
  group_by(chain_id, chain_step, information) %>%
  summarise(count = sum(count)) %>%
  add_column(totals = rep(c(28,28), 15)) %>% # I am adding it manually
  mutate(proportion = count / totals)

data_content_aggr %>%
  ggplot(aes(x=chain_step, y = proportion, colour = information)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = information, colour = information)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  theme_bw() +
  labs(title = "Study 3 - aggregate")
ggsave("study3_aggregate.pdf", height = 5, width = 6)

out_model <- lmer(proportion ~ information + (1|chain_step) + (1|chain_id), data = data_content_aggr)

summary(out_model)
#                      Estimate Std. Error       df t value Pr(>|t|)    
# informationsocial  0.32143    0.01969 22.00000  16.328 8.81e-14 ***

# plot for publication :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
pubPalette <- c("#999999", "#E69F00")
data_content_aggr %>%
  ggplot(aes(x=chain_step, y = proportion, colour = information)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = information, colour = information)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  scale_colour_manual(values = pubPalette) +
  theme_bw() +
  theme(legend.position = "none") +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  labs(title = "Social") +
  ylim(0,.75) 
ggsave("../plot/study3.pdf", height = 4, width = 4)
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
