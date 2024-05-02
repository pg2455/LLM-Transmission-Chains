library(tidyverse)
library(lme4) 
library(lmerTest) 
library(RColorBrewer) # with colour-blind-friendly palettes


# # prepare the coding document:
# n_content <- 8
# n_chains <- 5
# n_steps <- 3
# sim_data <- tibble(chain_step = factor(rep(1:n_steps, each = n_chains * n_content)),
#                   chain_id = factor(rep(rep(1:n_chains, each = n_content), n_steps)),
#                   content = rep(c("BMC", "BFC", "PMC", "PFC", "BMI", "PFI", "BFI", "PMI"), n_chains * n_steps),
#                   count =  NA)
# 
# # re-order using chain_id so it is easy to code:
# sim_data <- arrange(sim_data, chain_id)
# 
# # export and code:
# write_csv(sim_data, "study1.csv")

# process output:
sim_data <- read_csv("study1.csv")

# find proportions:

sim_data <- sim_data %>%
  mutate(totals = case_when (content == "BMC" ~ 5, 
                            content == "BFC" ~ 5,
                            content == "PMC" ~ 4, 
                            content == "PFC" ~ 5,
                            content == "BMI" ~ 3,
                            content == "PFI" ~ 6,
                            content == "BFI" ~ 3,
                            content == "PMI" ~ 4)) %>%
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
  labs(title = "Study 1")
ggsave("study1_all_content.pdf", height = 5, width = 6)
  
# group content together
# "PMC", "PFC", "BMC", "BFC" consistent
# group content
data_content_aggr <- sim_data %>%
  add_column(sterotype = NA) %>%
  mutate(stereotype = if_else(content == "PMC" | content == "PFC" | content == "BMC" | content == "BFC", 
                             "consistent", "non consistent")) %>%
  group_by(chain_id, chain_step, stereotype) %>%
  summarise(count = sum(count)) %>%
  add_column(totals = rep(c(19,16), 15)) %>% # I am adding it manually
  mutate(proportion = count / totals)

print(data_content_aggr)

data_content_aggr %>%
  ggplot(aes(x=chain_step, y = proportion, colour = stereotype)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = stereotype, colour = stereotype)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,1) +
  scale_color_brewer(palette = "Paired") +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  theme_bw() +
  labs(title = "Study 1 - aggregate")
ggsave("study1_aggregate.pdf", height = 5, width = 6)

# change order of levels so the model test consistent content (instead of non consistent)
data_content_aggr$stereotype <- factor(data_content_aggr$stereotype, levels = c("non consistent", "consistent"))

out_model <- lmer(proportion ~ stereotype + (1|chain_step) + (1|chain_id), data = data_content_aggr)

summary(out_model)
#                      Estimate Std. Error       df t value Pr(>|t|)    
# stereotypeconsistent  0.05855    0.01958 24.00000   2.991 0.006338 ** 


# PLOT FOR PUBLICATION
pubPalette <- c("#E69F00", "#999999")
data_content_aggr %>%
  ggplot(aes(x=chain_step, y = proportion, colour = stereotype)) +
  stat_summary(fun = mean, geom = "line", size = 1.5, aes(group = stereotype, colour = stereotype)) +
  stat_summary(fun = mean, geom = "point", size = 3) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.05, size = 1) + 
  ylim(0,.3) +
  scale_colour_manual(values = pubPalette) +
  theme_bw() +
  theme(legend.position = "none") +
  labs(x = "Chain step", y = "Proportion retained") +
  scale_x_continuous(breaks = c(1,2,3)) +
  labs(title = "Stereotype consistent")
ggsave("../plot/study1.pdf", height = 4, width = 4)

