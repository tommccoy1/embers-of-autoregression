





library(ggplot2)
library(dplyr)
library(ggpattern)


setwd("~/")

base_size <- 16
theme_set(theme_bw(base_size=base_size) +
            theme(#panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              axis.text.x=element_text()))


# first rare, then common
gpt35 <- c(0.00, 0.02, 0.00, 0.21, 0.00, 0.30, 0.40, 0.54, 0.00, 0.391, 0.00, 0.47, 0.15, 0.76)
gpt4 <- c(0.00, 0.21, 0.00, 0.51, 0.13, 0.39, 0.69, 0.84, 0.026, 0.762, 0.00, 0.33, 0.32, 0.80)
llama3 <- c(0.00, 0.00, 0.00, 0.05, 0.00, 0.05, 0.02, 0.22, 0.24, 0.544, 0.77, 0.87, 0.18, 0.67)
claude3 <- c(0.19, 0.70, 0.31, 0.98, 0.05, 0.66, 0.82, 0.83, 0.00, 0.577, 0.12, 0.56, 0.50, 0.92)
gemini <- c(0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.18, 0.33, 0.00, 0.547, 0.02, 0.01, 0.04, 0.65)
olmo <- c(0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.003, 0.00, 0.00, 0.00, 0.00)

standard_errors <- c(my_se(c(0.00, 0.02, 0.00, 0.21, 0.00, 0.30, 0.40, 0.54), 100),
                     my_se(c(0.00, 0.391), 1000),
                     my_se(c(0.00, 0.47, 0.15, 0.76), 100),
                     
                     my_se(c(0.00, 0.21, 0.03, 0.51, 0.13, 0.39, 0.69, 0.84), 100),
                     my_se(c(0.026, 0.762), 1000),
                     my_se(c(0.00, 0.33, 0.32, 0.80), 100),
                     
                     my_se(c(0.00, 0.00, 0.00, 0.05, 0.00, 0.05, 0.02, 0.22), 100),
                     my_se(c(0.24, 0.544), 1000),
                     my_se(c(0.77, 0.87, 0.18, 0.67), 100),
                     
                     my_se(c(0.19, 0.70, 0.31, 0.98, 0.05, 0.66, 0.82, 0.830), 100),
                     my_se(c(0.00, 0.577), 1000),
                     my_se(c(0.12, 0.56, 0.50, 0.92), 100),
                     
                     my_se(c(0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.18, 0.33), 100),
                     my_se(c(0.00, 0.547), 1000),
                     my_se(c(0.02, 0.01, 0.04, 0.65), 100),
                     
                     my_se(c(0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00), 100),
                     my_se(c(0.00, 0.003), 1000),
                     my_se(c(0.00, 0.00, 0.00, 0.00), 100)
)

df_pairs <- data.frame(Accuracy=c(gpt35, gpt4, llama3, claude3, gemini, olmo),
                       StandardError=standard_errors,
                       Model=rep(c("GPT-3.5", "GPT-4", "Llama 3", "Claude 3", "Gemini 1.0", "OLMo"), each=14),
                       Task=rep(rep(c("Shift cipher\nencoding", "Shift cipher\ndecoding", "Pig Latin\nencoding", "Pig Latin\ndecoding", "Acronyms", "Linear\nfunction", "Sorting"), each=2), 6),
                       Commonness=rep(c("Rare", "Common"), 14)
)

df_pairs$Commonness <- factor(df_pairs$Commonness, levels=c("Rare", "Common"), labels=c("Rare", "Common"))
df_pairs$Task <- factor(df_pairs$Task, levels=c("Shift cipher\nencoding", "Shift cipher\ndecoding", "Pig Latin\nencoding", "Pig Latin\ndecoding", "Acronyms", "Linear\nfunction", "Sorting"))
df_pairs$Model <- factor(df_pairs$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))


df_pairs <- df_pairs[df_pairs$Model != "OLMo", ]

ggplot(data=df_pairs, aes(x=Commonness, y=Accuracy, fill=Model, pattern=Commonness)) + 
  geom_bar_pattern(stat="Identity", position=position_dodge(width=0.76), pattern_density=0.5, width=0.7, color="black") + 
  scale_pattern_manual(values = c("none", "none"))  +
  scale_fill_manual(values = c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF")) + 
  facet_grid(Model ~ Task) +
  geom_errorbar(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError), width=0.2,
                position=position_dodge(width=0.76)) +
  ylim(0.0,1.0) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="none") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(axis.title.x=element_blank()) +
  #theme(legend.key.size = unit(0.8, 'cm')) +
  #guides(pattern=guide_legend(title="Task type", keywidth=0.4, default.unit="inch")) +
  labs(x="", y="Accuracy") + 
  scale_y_continuous(breaks = c(0,0.5,1), limits = c(0, 1)) +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  guides(fill=guide_legend(title="Task type", keywidth=0.4, default.unit="inch"))

ggsave("embers_0504_pairs.pdf", width=9, height=6.8, dpi=100)







