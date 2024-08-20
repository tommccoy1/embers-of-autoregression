

my_se <- function(values, sample_size) {
  return (sqrt(values*(1.0-values)/sample_size))
}

base_size <- 20
theme_set(theme_bw(base_size=base_size) +
            theme(#panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              axis.text.x=element_text()))

# -way, -ay, -yay, -hay, -say
# pig, pigc, pigb, pigd, boar
freqs <- c(0.46, 0.31, 0.18, 0.05, 0.00)

# Encoding
accs_gpt35 <- c(0.24,0.30,0.17,0.12,0.01)
accs_gpt4 <- c(0.42,0.39,0.24,0.23,0.06)
accs_llama3 <- c(0.00, 0.05, 0.00, 0.00, 0.00)
accs_claude3 <- c(0.67, 0.66, 0.72, 0.63, 0.46)
accs_gemini <- c(0.14, 0.00, 0.00, 0.00, 0.00)
accs_olmo <- c(0.00, 0.00, 0.00, 0.00, 0.00)


pig_df <- data.frame(Frequency=rep(freqs,6),
                     Accuracy=c(accs_gpt35, accs_gpt4, accs_claude3, accs_llama3, accs_gemini, accs_olmo),
                     StandardError=my_se(c(accs_gpt35, accs_gpt4, accs_claude3, accs_llama3, accs_gemini, accs_olmo), 100),
                     Model=rep(c("GPT-3.5", "GPT-4",  "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"), each=5)
)

pig_df$Model <- factor(pig_df$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))

pig_df <- pig_df[ pig_df$Model != "OLMo", ]
ggplot(data=pig_df, aes(x=Frequency, y=Accuracy, color=Model, shape=Model)) + 
  geom_point(size=5) + 
  geom_line(size=1.5) +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  ylim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position=c(0.70, 0.8)) +
  theme(legend.position="none") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank(),
        legend.margin=margin(c(0,5,5,5))) +
  labs(x="Task frequency", y="Encoding accuracy")

ggsave("embers_0504_pigenc_freq.pdf", width=4, height=4, dpi=100)



ggplot(data=pig_df, aes(x=Frequency, y=Accuracy, color=Model, shape=Model)) + 
  geom_point(size=5) + 
  geom_line(size=1.5) +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  ylim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position=c(0.70, 0.8)) +
  theme(legend.position="top") +
  guides(color=guide_legend(nrow=3,byrow=TRUE)) +
  guides(shape=guide_legend(nrow=3,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank(),
        legend.margin=margin(c(0,5,5,5))) +
  labs(x="Task frequency", y="Encoding accuracy")

ggsave("embers_0504_pigenc_freq_topkey.pdf", width=4, height=5.3, dpi=100)






# Decoding
accs_gpt35 <- c(0.52,0.54,0.46,0.49,0.48)
accs_gpt4 <- c(0.87,0.84,0.78,0.77,0.80)
accs_llama3 <- c(0.17, 0.22, 0.13, 0.14, 0.11)
accs_claude3 <- c(0.83, 0.83, 0.75, 0.81, 0.71)
accs_gemini <- c(0.39, 0.33, 0.33, 0.33, 0.17)
accs_olmo <- c(0.00, 0.00, 0.00, 0.00, 0.00)

pig_df <- data.frame(Frequency=rep(freqs,6),
                     Accuracy=c(accs_gpt35, accs_gpt4, accs_claude3, accs_llama3, accs_gemini, accs_olmo),
                     StandardError=my_se(c(accs_gpt35, accs_gpt4, accs_claude3, accs_llama3, accs_gemini, accs_olmo), 100),
                     Model=rep(c("GPT-3.5", "GPT-4",  "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"), each=5)
)

pig_df$Model <- factor(pig_df$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))


pig_df <- pig_df[ pig_df$Model != "OLMo", ]
ggplot(data=pig_df, aes(x=Frequency, y=Accuracy, color=Model, shape=Model)) + 
  geom_point(size=5) + 
  geom_line(size=1.3) +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  ylim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="right") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Task frequency", y="Decoding accuracy")

ggsave("embers_0504_pigdec_freq.pdf", width=6, height=4, dpi=100)



ggplot(data=pig_df, aes(x=Frequency, y=Accuracy, color=Model, shape=Model)) + 
  geom_point(size=5) + 
  geom_line(size=1.3) +
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  ylim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="none") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Task frequency", y="Decoding accuracy")

ggsave("embers_0504_pigdec_freq_nokey.pdf", width=4, height=4, dpi=100)


