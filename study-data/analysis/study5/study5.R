library(tidyverse)
library(lme4) 
library(lmerTest) 
library(RColorBrewer) # with colour-blind-friendly palettes


# MUKI
# process output:
sim_data <- read_csv("Study5_Muki.csv") %>%
  rename(chain_step = Chain_step, chain_id = Chain_id, content = Content, count = Count) %>% # consistence with previous code
  filter(content != "None") # to be consistent with the original study, we do not include this in the analysis 
# find proportions:
totals <- read_csv("Muki_totals.csv")

sim_data <- sim_data %>%
  mutate(totals = case_when (content == "CI_B" ~ sum(totals=="CI_B1" | totals=="CI_B2" | totals=="CI_B3" , na.rm = TRUE),
                            content == "CI_M" ~ sum(totals=="CI_M1" | totals=="CI_M2" , na.rm = TRUE),
                            content == "CI_P" ~ sum(totals=="CI_P1" | totals=="CI_P2" , na.rm = TRUE), 
                            content == "Emo_Neg" ~ sum(totals=="Emo_Neg", na.rm = TRUE),
                            content == "Emo_Posi" ~ sum(totals=="Emo_Posi", na.rm = TRUE),
                            content == "Moral" ~ sum(totals=="Moral", na.rm = TRUE),
                            content == "Social_Basic" ~ sum(totals=="Social_Basic", na.rm = TRUE),
                            content == "Social_Gossip" ~ sum(totals=="Social_Gossip", na.rm = TRUE),
                            content == "Survival" ~ sum(totals=="Survival", na.rm = TRUE),
                            content == "Rational" ~ sum(totals=="Rational", na.rm = TRUE))) %>%
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
  labs(title = "Study 5 - Muki")
ggsave("study5_Muki_all_content.pdf", height = 5, width = 6)
  

# group content together
# group content
data_content_aggr <- sim_data %>%
  add_column(sterotype = NA) %>%
  mutate(expected = if_else(content == "Emo_Neg" | content == "CI_B" | content == "Social_Basic" | content == "Social_Gossip", 
                             "yes", "no")) %>%
  group_by(chain_id, chain_step, expected) %>%
  summarise(count = sum(count)) %>%
  add_column(totals = rep(c(86,76), 15)) %>% # I am adding it manually
  mutate(proportion = count / totals)

sim_cumulative <- data_content_aggr # save for later

data_content_aggr %>%
  ggplot(aes(x=chain_step, y = proportion, colour = expected)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = expected, colour = expected)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  theme_bw() +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  labs(title = "Study 5 - Muki - aggregate")
ggsave("study5_Muki_aggregate.pdf", height = 5, width = 6)

out_model <- lmer(proportion ~ expected + (1|chain_step) + (1|chain_id), data = data_content_aggr)

summary(out_model)
#              Estimate Std. Error        df t value Pr(>|t|)    
# expectedyes  0.065545   0.007998 21.999998   8.195 3.95e-08 ***

# TAKA TORO

# process output:
sim_data <- read_csv("Study5_TakaToro.csv") %>%
  rename(chain_step = Chain_step, chain_id = Chain_id, content = Content, count = Total) # consistence with previous code

# find proportions:
totals <- read_csv("TakaToro_totals.csv") 


sim_data$content[sim_data$content=="Negative"] <- "Emo_neg"  # consistence with previous code
sim_data$content[sim_data$content=="Positive"] <- "Emo_pos"

sim_data <- sim_data %>%         
  mutate(totals = case_when (content == "CI_B" ~ sum(totals=="CI_B1", na.rm = TRUE),
                             content == "CI_M" ~ sum(totals=="CI_M1" | totals=="CI_M2" , na.rm = TRUE),
                             content == "CI_P" ~ sum(totals=="CI_P1" | totals=="CI_P2" | totals=="CI_P3" | totals=="CI_P4", na.rm = TRUE), 
                             content == "Emo_neg" ~ sum(totals=="Negative", na.rm = TRUE),
                             content == "Emo_pos" ~ sum(totals=="Positive", na.rm = TRUE),
                             content == "Moral" ~ sum(totals=="Moral", na.rm = TRUE),
                             content == "Social_Basic" ~ sum(totals=="Social_Basic", na.rm = TRUE),
                             content == "Social_Gossip" ~ sum(totals=="Social_Gossip", na.rm = TRUE),
                             content == "Survival" ~ sum(totals=="Survival", na.rm = TRUE),
                             content == "Rational" ~ sum(totals=="Rational", na.rm = TRUE))) %>%
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
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  labs(title = "Study 5 - TakaToro")
ggsave("study5_TakaToro_all_content.pdf", height = 5, width = 6)


# group content together
# group content
data_content_aggr <- sim_data %>%
  add_column(sterotype = NA) %>%
  mutate(expected = if_else(content == "Emo_neg" | content == "CI_B" | content == "Social_Basic" | content == "Social_Gossip", 
                            "yes", "no")) %>%
  group_by(chain_id, chain_step, expected) %>%
  summarise(count = sum(count)) %>%
  add_column(totals = rep(c(78,60), 15)) %>% # I am adding it manually 
  mutate(proportion = count / totals)

data_content_aggr %>%
  ggplot(aes(x=chain_step, y = proportion, colour = expected)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = expected, colour = expected)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  theme_bw() +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  labs(title = "Study 5 - TakaToro - aggregate")
ggsave("study5_TakaToro_aggregate.pdf", height = 5, width = 6)

out_model <- lmer(proportion ~ expected + (1|chain_step) + (1|chain_id), data = data_content_aggr)

summary(out_model)
#              Estimate Std. Error        df t value Pr(>|t|)    
# expectedyes  0.085983   0.009536 22.000006   9.017 7.66e-09 ***

# cumulative:
sim_cumulative$count <- sim_cumulative$count + data_content_aggr$count
sim_cumulative$totals <- sim_cumulative$totals + data_content_aggr$totals
sim_cumulative$proportion <-  sim_cumulative$count / sim_cumulative$totals

sim_cumulative %>%
  ggplot(aes(x=chain_step, y = proportion, colour = expected)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = expected, colour = expected)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  theme_bw() +
  labs(title = "Study 5 - cumulative - aggregate")
ggsave("study5_cumulative_aggregate.pdf", height = 5, width = 6)

out_model <- lmer(proportion ~ expected + (1|chain_step) + (1|chain_id), data = sim_cumulative)

summary(out_model)
#              Estimate Std. Error        df t value Pr(>|t|)    
# expectedyes  0.07639    0.00695 22.00000  10.991  2.1e-10 ***

# plot for publication :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
pubPalette <- c("#999999", "#E69F00")
sim_cumulative %>%
  ggplot(aes(x=chain_step, y = proportion, colour = expected)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = expected, colour = expected)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  scale_colour_manual(values = pubPalette) +
  theme_bw() +
  theme(legend.position = "none") +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  labs(title = "Negative + Social + Counterintuitive (bio)") +
  ylim(0,.3) 
ggsave("../plot/study5.pdf", height = 4, width = 4)
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
  