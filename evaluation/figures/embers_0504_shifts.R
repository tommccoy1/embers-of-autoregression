
library(ggplot2)
library(dplyr)
library(ggpattern)

setwd("~/")

my_se <- function(values, sample_size) {
  return (sqrt(values*(1.0-values)/sample_size))
}

base_size <- 20
theme_set(theme_bw(base_size=base_size) +
            theme(#panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              axis.text.x=element_text()))


# First rare, then common
# Decoding acc for rot-12 and rot-13
gpt35 <- c(0.00, 0.21)
gpt4 <- c(0.00, 0.51)
llama3 <- c(0.00, 0.05)
claude3 <- c(0.31, 0.98)
gemini <- c(0.00, 0.00)
olmo <- c(0.00, 0.00)


df_pairs <- data.frame(Accuracy=c(gpt35, gpt4, llama3, claude3, gemini, olmo),
                       StandardError=my_se(c(gpt35, gpt4, llama3, claude3, gemini, olmo), 100),
                       Model=rep(c("GPT-3.5", "GPT-4", "Llama 3", "Claude 3", "Gemini 1.0", "OLMo"), each=2),
                       Commonness=rep(c("Rot-12 (rare)", "Rot-13 (common)"), 12)
)

df_pairs$Commonness <- factor(df_pairs$Commonness, levels=c("Rot-12 (rare)", "Rot-13 (common)"))
df_pairs$Model <- factor(df_pairs$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))


df_pairs$Commonness <- factor(df_pairs$Commonness, levels=c("Rot-12 (rare)", "Rot-13 (common)"), labels=c("Rot-12   ", "   Rot-13"))
ggplot(data=df_pairs, aes(x=Commonness, y=Accuracy, fill=Model, pattern=Commonness)) + 
  geom_bar_pattern(stat="Identity", position=position_dodge(width=0.76), pattern_density=0.5, width=0.7, color="black") + 
  scale_pattern_manual(values = c("none", "none"))  +
  #scale_fill_manual(values = c("#00BA38", "#C77CFF"), labels=c("Blah      ", "Rot-13 (common)")) + 
  scale_fill_manual(values = c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), guide="none") + 
  ylim(0.0,1.0) +
  facet_grid(. ~ Model) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(axis.title.x=element_blank()) +
  theme(legend.position="none") +
  theme(legend.key.size = unit(0.8, 'cm')) +
  geom_errorbar(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError), width=0.2,
                position=position_dodge(width=0.76)) +
  guides(pattern=guide_legend(title="", keywidth=0.4, default.unit="inch", override.aes = list(fill = "white"))) +
  labs(x="", y="Decoding accuracy") #+ 


ggsave("embers_0504_shift_pairs_short.pdf", width=7.6, height=3.3, dpi=100)







gpt35_enc_acc <- c(0.02,0.03,0.05)
gpt4_enc_acc <- c(0.21,0.10,0.11)
llama3_enc_acc <- c(0.00, 0.00, 0.00)
claude3_enc_acc <- c(0.70, 0.62, 0.54)
gemini_enc_acc <- c(0.00, 0.00, 0.00)
olmo_enc_acc <- c(0.00, 0.00, 0.00)


gpt35_dec_acc <- c(0.21,0.07,0.04)
gpt4_dec_acc <- c(0.51,0.22,0.13)
llama3_dec_acc <- c(0.05, 0.01, 0.00)
claude3_dec_acc <- c(0.98, 0.92, 0.86)
gemini_dec_acc <- c(0.00, 0.00, 0.00)
olmo_dec_acc <- c(0.00, 0.00, 0.00)

logprobs <- c(-58.4,-86.3,-144.5)


enc_df <- data.frame(Accuracy=c(gpt35_enc_acc,gpt4_enc_acc,llama3_enc_acc,claude3_enc_acc, gemini_enc_acc, olmo_enc_acc),
                     StandardError=my_se(c(gpt35_enc_acc,gpt4_enc_acc,llama3_enc_acc,claude3_enc_acc, gemini_enc_acc, olmo_enc_acc), 100),
                     Model=rep(c("GPT-3.5", "GPT-4", "Llama 3", "Claude 3", "Gemini 1.0", "OLMo"),each=3),
                     InputProb=rep(logprobs,6)
)

enc_df$Model <- factor(enc_df$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))


ggplot(data=enc_df, aes(x=InputProb, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point(size=5) + 
  geom_line(size=1.5) +
  ylim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  #xlim(0.0,1.0) +
  #scale_y_continuous(breaks=seq(0,1.0,0.01)) +
  #theme(legend.position="top") +
  theme(legend.position=c(0.70, 0.78)) +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(line=guide_legend(title="", keywidth=0.6, default.unit="inch")) +
  theme(legend.key.width = unit(1,"cm")) +
  #geom_errorbar(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError), width=2, color="black") +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank(),
        legend.margin=margin(c(1,5,5,5))) +
  labs(x="Input log probability", y="Encoding accuracy")


ggsave(file.path("~", 'embers_0504_shift_encoding.pdf'), width=4.2, height=4)



dec_df <- data.frame(Accuracy=c(gpt35_dec_acc,gpt4_dec_acc,llama3_dec_acc,claude3_dec_acc, gemini_dec_acc, olmo_dec_acc),
                     StandardError=my_se(c(gpt35_dec_acc,gpt4_dec_acc,llama3_dec_acc,claude3_dec_acc, gemini_dec_acc, olmo_dec_acc), 100),
                     Model=rep(c("GPT-3.5", "GPT-4", "Llama 3", "Claude 3", "Gemini 1.0", "OLMo"),each=3),
                     OutputProb=rep(logprobs,6)
)

dec_df$Model <- factor(enc_df$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))


# OLD COLOR: "#F8766D"
ggplot(data=dec_df, aes(x=OutputProb, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point(size=5) + 
  geom_line(size=1.5) +
  ylim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  theme(legend.key.width = unit(1,"cm")) +
  #xlim(0.0,1.0) +
  #scale_y_continuous(breaks=seq(0,1.0,0.05), limits=c(0,1.0)) +
  #theme(legend.position="top") +
  theme(legend.position=c(0.70, 0.78)) +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank(),
        legend.margin=margin(c(1,5,5,5))) +
  labs(x="Output log probability", y="Decoding accuracy")




ggsave(file.path("~", 'embers_0504_shift_decoding.pdf'), width=4.2, height=4)











base_size <- 16
theme_set(theme_bw(base_size=base_size) +
            theme(#panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              axis.text.x=element_text()))

shift_level <- 1:25
gpt35_acc <- c(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.21,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
gpt4_acc <- c(0.82,0.02,0.76,0.01,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
llama3_acc <- c(0.0,0.0,0.01,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.05,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
claude3_acc <- c(0.95,0.96,0.96,0.85,0.85,0.64,0.86,0.43,0.34,0.27,0.23,0.31,0.98,0.38,0.13,0.25,0.38,0.25,0.35,0.07,0.21,0.36,0.67,0.47,0.94)
gemini_acc <- c(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
olmo_acc <- c(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)


shift_df <- data.frame(Accuracy=c(gpt35_acc, gpt4_acc, llama3_acc, claude3_acc, gemini_acc, olmo_acc),
                       StandardError=my_se(c(gpt35_acc, gpt4_acc, llama3_acc, claude3_acc, gemini_acc, olmo_acc), 100),
                       Shift=rep(shift_level, 6),
                       Model=rep(c("GPT-3.5", "GPT-4", "Llama 3", "Claude 3", "Gemini 1.0", "OLMo"), each=25)
)

shift_df$Model <- factor(shift_df$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))

shift_df <- shift_df[shift_df$Model != "OLMo", ]

ggplot(data=shift_df, aes(x=Shift, y=Accuracy, color=Model, shape=Model)) + 
  geom_point(size=3) + 
  geom_line() +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  ylim(0.0,1.0) +
  #xlim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_x_continuous(breaks=seq(1,25,1)) +
  theme(legend.position=c(0.7,0.78))+
  #theme(legend.position="right")+
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank(),
        legend.margin=margin(c(1,5,5,5))) +
  labs(x="Shift", y="Decoding accuracy")


ggsave(file.path("~", 'embers_0504_shifts.pdf'), width=9, height=4)


ggplot(data=shift_df, aes(x=Shift, y=Accuracy, color=Model, shape=Model)) + 
  geom_point(size=3) + 
  geom_line() +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  ylim(0.0,1.0) +
  #xlim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_x_continuous(breaks=seq(1,25,1)) +
  theme(legend.position=c(0.7,0.73))+
  #theme(legend.position="right")+
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank(),
        legend.margin=margin(c(1,5,5,5))) +
  labs(x="Shift", y="Decoding accuracy")

ggsave(file.path("~", 'embers_0504_shifts_short.pdf'), width=9, height=3.5)












# NOT CHANGED BELOW HERE

# Shifts vs prompt styles

shift_level <- 1:25
basic_acc <- c(0.82,0.02,0.76,0.01,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
step_acc <- c(0.88,0.2,0.86,0.19,0.16,0.21,0.14,0.09,0.08,0.01,0.0,0.0,0.59,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.03,0.05)
cot_acc <- c(0.89,0.66,0.98,0.49,0.57,0.48,0.48,0.36,0.2,0.03,0.01,0.0,0.79,0.0,0.0,0.0,0.0,0.01,0.0,0.0,0.27,0.17,0.5,0.51,0.34)


prompt_shift_df <- data.frame(Accuracy=c(basic_acc, step_acc, cot_acc),
                              StandardError=my_se(c(basic_acc, step_acc, cot_acc), 100),
                              Shift=rep(shift_level, 3),
                              Prompt=rep(c("Basic", "Step-by-step", "Chain-of-thought"), each=25)
)

prompt_shift_df$Prompt <- factor(prompt_shift_df$Prompt, levels=c("Basic", "Step-by-step", "Chain-of-thought"))

ggplot(data=prompt_shift_df, aes(x=Shift, y=Accuracy, color=Prompt, shape=Prompt)) + 
  geom_point(size=3) + 
  geom_line() +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Prompt), alpha=0.2, color=NA) +
  ylim(0.0,1.0) +
  #xlim(0.0,1.0) +
  scale_color_manual(values=c("#00BFC4", "#F8766D", "#00BA38")) + 
  scale_fill_manual(values=c("#00BFC4", "#F8766D", "#00BA38")) +
  scale_x_continuous(breaks=seq(1,25,1)) +
  theme(legend.position=c(0.85,0.84))+
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  theme(
    legend.margin = margin(3, 3, 3, 3)) +
  labs(x="Shift", y="Decoding accuracy")


ggsave(file.path("~", 'embers_0915_promptshifts.pdf'), width=9, height=4)







# First rare, then common
# Decoding acc for rot-2 and rot-13
basic <- c(0.03, 0.51)
step <- c(0.19, 0.53)
cot <- c(0.70, 0.78)

df_pairs <- data.frame(Accuracy=c(basic, step, cot),
                       Prompt=rep(c("Basic", "Step-by-step", "Chain-of-thought"), each=2),
                       Commonness=rep(c("Rot-2 (rare)", "Rot-13 (common)"), 3)
)

df_pairs$Commonness <- factor(df_pairs$Commonness, levels=c("Rot-2 (rare)", "Rot-13 (common)"))
df_pairs$Prompt <- factor(df_pairs$Prompt, levels=c("Basic", "Step-by-step", "Chain-of-thought"))

ggplot(data=df_pairs, aes(x=Commonness, y=Accuracy, fill=Prompt, pattern=Commonness)) + 
  geom_bar_pattern(stat="Identity", position=position_dodge(), pattern_density=0.5, width=0.7, color="black") + 
  scale_pattern_manual(values = c("none", "none"), labels=c("Rot-2 (rare)      ", "Rot-13 (common)"))  +
  scale_fill_manual(values = c("#00BA38", "#C77CFF"), labels=c("Rot-2 (rare)      ", "Rot-13 (common)")) + 
  ylim(0.0,1.0) +
  facet_grid(. ~ Prompt) + 
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(axis.title.x=element_blank()) +
  theme(legend.position="none") +
  scale_fill_manual(values=c("#00BFC4", "#00BA38", "#F8766D")) +
  theme(legend.key.size = unit(0.8, 'cm')) +
  guides(pattern=guide_legend(title="", keywidth=0.4, default.unit="inch")) +
  labs(x="", y="Decoding accuracy") + 
  guides(fill=guide_legend(title="", keywidth=0.4, default.unit="inch"))

ggsave("embers_0915_shift_pairs_prompts.pdf", width=6, height=4, dpi=100)








basic_enc_acc <- c(0.21, 0.10, 0.11)
step_enc_acc <- c(0.20, 0.08, 0.12)
cot_enc_acc <- c(0.11, 0.04, 0.04)

basic_dec_acc <- c(0.51, 0.22, 0.13)
step_dec_acc <- c(0.53, 0.38, 0.21)
cot_dec_acc <- c(0.78, 0.56, 0.32)

logprobs <- c(-58.4,-86.3,-144.5)


enc_df <- data.frame(Accuracy=c(basic_enc_acc, step_enc_acc, cot_enc_acc),
                     StandardError=my_se(c(basic_enc_acc, step_enc_acc, cot_enc_acc), 100),
                     Prompt=rep(c("Basic", "Step-by-step", "Chain-of-thought"),each=3),
                     InputProb=rep(logprobs,3)
)

enc_df$Prompt <- factor(enc_df$Prompt, levels=c("Basic", "Step-by-step", "Chain-of-thought"))


ggplot(data=enc_df, aes(x=InputProb, y=Accuracy, color=Prompt, shape=Prompt)) + 
  geom_point(size=3) + 
  geom_line() +
  ylim(0.0,1.0) +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Prompt), alpha=0.2, color=NA) +
  scale_color_manual(values=c("#00BFC4", "#F8766D", "#00BA38")) + 
  scale_fill_manual(values=c("#00BFC4", "#F8766D", "#00BA38")) +
  #scale_shape_manual(values=c("circle","triangle"), labels=c("GPT-3.5    ", "GPT-4")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="none") +
  guides(color=guide_legend(nrow=3,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(line=guide_legend(title="", keywidth=0.6, default.unit="inch")) +
  theme(legend.key.width = unit(1,"cm")) +
  theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Input log probability", y="Encoding accuracy")


ggsave(file.path("~", 'embers_0915_shift_encoding_prompts.pdf'), width=3.8, height=3.9)




dec_df <- data.frame(Accuracy=c(basic_dec_acc, step_dec_acc, cot_dec_acc),
                     StandardError=my_se(c(basic_dec_acc, step_dec_acc, cot_dec_acc), 100),
                     Prompt=rep(c("Basic", "Step-by-step", "Chain-of-thought"),each=3),
                     InputProb=rep(logprobs,3)
)

dec_df$Prompt <- factor(dec_df$Prompt, levels=c("Basic", "Step-by-step", "Chain-of-thought"))


ggplot(data=dec_df, aes(x=InputProb, y=Accuracy, color=Prompt, shape=Prompt)) + 
  geom_point(size=3) + 
  geom_line() +
  ylim(0.0,1.0) +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Prompt), alpha=0.2, color=NA) +
  scale_color_manual(values=c("#00BFC4", "#F8766D", "#00BA38")) + 
  scale_fill_manual(values=c("#00BFC4", "#F8766D", "#00BA38")) +
  #scale_shape_manual(values=c("circle","triangle"), labels=c("GPT-3.5    ", "GPT-4")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="none") +
  guides(color=guide_legend(nrow=3,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(line=guide_legend(title="", keywidth=0.6, default.unit="inch")) +
  theme(legend.key.width = unit(1,"cm")) +
  theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Output log probability", y="Decoding accuracy")


ggsave(file.path("~", 'embers_0915_shift_decoding_prompts.pdf'), width=3.8, height=3.9)







# First rare, then common
# Decoding acc for rot-2 and rot-13
gpt35 <- c(0.01, 0.23)
gpt4 <- c(0.01, 0.49)

df_pairs <- data.frame(Accuracy=c(gpt35, gpt4),
                       Model=rep(c("GPT-3.5", "GPT-4"), each=2),
                       Commonness=rep(c("Shift by 12 (rare)", "Shift by 13 (common)"), 2)
)

df_pairs$Commonness <- factor(df_pairs$Commonness, levels=c("Shift by 12 (rare)", "Shift by 13 (common)"))

ggplot(data=df_pairs, aes(x=Model, y=Accuracy, fill=Commonness, pattern=Commonness)) + 
  geom_bar_pattern(stat="Identity", position=position_dodge(), pattern_density=0.5, width=0.7) + 
  scale_pattern_manual(values = c("none", "stripe"), labels=c("Shift by 12 (rare)      ", "Shift by 13 (common)"))  +
  scale_fill_manual(values = c("#00BA38", "#C77CFF"), labels=c("Shift by 12 (rare)      ", "Shift by 13 (common)")) + 
  ylim(0.0,1.0) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(axis.title.x=element_blank()) +
  theme(legend.position="top") +
  theme(legend.key.size = unit(0.8, 'cm')) +
  guides(pattern=guide_legend(title="", keywidth=0.4, default.unit="inch", nrow=2,byrow=TRUE)) +
  labs(x="", y="Decoding accuracy") + 
  guides(fill=guide_legend(title="", keywidth=0.4, default.unit="inch", nrow=2,byrow=TRUE))

ggsave("embers_0824_shift_first.pdf", width=3, height=4, dpi=100)






