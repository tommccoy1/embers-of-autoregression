

library(ggplot2)
library(ggh4x)


base_size <- 20
theme_set(theme_bw(base_size=base_size) +
            theme(#panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              axis.text.x=element_text()))



# DECRYPTING

# Low prob, medium prob, high prob

logprob_rev <- c(-144.54, -86.25, -58.38)
logprob_pig <- c(-132.26, -86.86, -62.54)
logprob_rot <- c(-144.54, -86.25, -58.38)
logprob_acronym <- c(-19.29,-17.14,-15.33,-13.98,-12.01)
logprob_swap <- c(-161.4, -101.7, -68.4)


accs_gpt35_rev <- c(0.28, 0.61, 0.74)
accs_gpt35_pig <- c(0.05, 0.26, 0.54)
accs_gpt35_rot <- c(0.04, 0.07, 0.21)
accs_gpt35_acronym <- c(0.181, 0.258, 0.272, 0.320, 0.391)
accs_gpt35_swap <- c(0.05, 0.43, 0.65)

accs_gpt4_rev <- c(0.53, 0.96, 0.97)
accs_gpt4_pig <- c(0.29, 0.70, 0.84)
accs_gpt4_rot <- c(0.13, 0.22, 0.51)
accs_gpt4_acronym <- c(0.670, 0.734, 0.744, 0.762, 0.762)
accs_gpt4_swap <- c(0.02, 0.53, 0.83)


accs_llama3_rev <- c(0.16, 0.36, 0.52)
accs_llama3_pig <- c(0.03, 0.10, 0.22)
accs_llama3_rot <- c(0.00, 0.01, 0.05)
accs_llama3_acronym <- c(0.432, 0.439, 0.488, 0.565, 0.544)
accs_llama3_swap <- c(0.01, 0.15, 0.26)

accs_claude3_rev <- c(0.11, 0.87, 0.91)
accs_claude3_pig <- c(0.38, 0.74, 0.83)
accs_claude3_rot <- c(0.86, 0.92, 0.98)
accs_claude3_acronym <- c(0.569, 0.566, 0.571, 0.591, 0.577)
accs_claude3_swap <- c(0.02, 0.26, 0.53)

accs_geminipro_rev <- c(0.05, 0.49, 0.61)
accs_geminipro_pig <- c(0.00, 0.09, 0.33)
accs_geminipro_rot <- c(0.00, 0.00, 0.00)
accs_geminipro_acronym <- c(0.523, 0.526, 0.559, 0.592, 0.547)
accs_geminipro_swap <- c(0.02, 0.33, 0.53)

accs_olmo_rev <- c(0.00, 0.00, 0.01)
accs_olmo_pig <- c(0.00, 0.00, 0.00)
accs_olmo_rot <- c(0.00, 0.00, 0.00)
accs_olmo_acronym <- c(0.003, 0.005, 0.002, 0.000,0.001)
accs_olmo_swap <- c(0.00, 0.05, 0.09)

decoding_df <- data.frame(Logprob=rep(c(logprob_rev,logprob_pig,logprob_rot,logprob_swap,logprob_acronym), 6),
                          Accuracy=c(accs_gpt4_rev, accs_gpt4_pig, accs_gpt4_rot,accs_gpt4_swap,accs_gpt4_acronym,
                                     accs_gpt35_rev, accs_gpt35_pig, accs_gpt35_rot,accs_gpt35_swap,accs_gpt35_acronym,
                                     accs_claude3_rev, accs_claude3_pig, accs_claude3_rot,accs_claude3_swap,accs_claude3_acronym,
                                     accs_llama3_rev, accs_llama3_pig, accs_llama3_rot,accs_llama3_swap,accs_llama3_acronym,
                                     accs_geminipro_rev, accs_geminipro_pig, accs_geminipro_rot,accs_geminipro_swap,accs_geminipro_acronym,
                                     accs_olmo_rev, accs_olmo_pig, accs_olmo_rot,accs_olmo_swap,accs_olmo_acronym),
                          StandardError=c(my_se(c(accs_gpt4_rev, accs_gpt4_pig, accs_gpt4_rot, accs_gpt4_swap), 100), my_se(accs_gpt4_acronym, 1000),
                                          my_se(c(accs_gpt35_rev, accs_gpt35_pig, accs_gpt35_rot, accs_gpt35_swap), 100), my_se(accs_gpt35_acronym, 1000), 
                                          my_se(c(accs_claude3_rev, accs_claude3_pig, accs_claude3_rot, accs_claude3_swap), 100), my_se(accs_claude3_acronym, 1000),
                                          my_se(c(accs_llama3_rev, accs_llama3_pig, accs_llama3_rot, accs_llama3_swap), 100), my_se(accs_llama3_acronym, 1000),
                                          my_se(c(accs_geminipro_rev, accs_geminipro_pig, accs_geminipro_rot, accs_geminipro_swap), 100), my_se(accs_geminipro_acronym, 1000),
                                          my_se(c(accs_olmo_rev, accs_olmo_pig, accs_olmo_rot, accs_olmo_swap), 100), my_se(accs_olmo_acronym, 1000)),
                          Model=rep(c("GPT-4", "GPT-3.5", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"), each=17),
                          Task=rep(c(rep(c("Reversal", "Pig Latin", "Shift cipher", "Article swapping"), each=3), c("Acronym", "Acronym", "Acronym", "Acronym", "Acronym")), 6)
)

decoding_df$Task <- factor(decoding_df$Task, levels=c("Shift cipher", "Pig Latin", "Acronym", "Article swapping", "Reversal"))
decoding_df$Model <- factor(decoding_df$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))

decoding_df <- decoding_df[decoding_df$Model != "OLMo", ]

ggplot(data=decoding_df, aes(x=Logprob, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point(size=5) + 
  geom_line(size=1.5) +
  ylim(0.0,1.0) +
  facet_grid(. ~ Task, scales="free") +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38"), labels=c("GPT-3.5           ", "GPT-4           ", "Claude 3           ", "Llama 3           ", "Gemini 1.0")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38"), labels=c("GPT-3.5           ", "GPT-4           ", "Claude 3           ", "Llama 3           ", "Gemini 1.0")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20), labels=c("GPT-3.5           ", "GPT-4           ", "Claude 3           ", "Llama 3           ", "Gemini 1.0")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.key.size = unit(0.8, 'cm')) +
  #theme(axis.text.x = element_text(size = 11)) +
  theme(legend.title=element_blank()) +
  #theme(legend.position=c(0.615, 0.75)) +
  #theme(legend.position="right") +
  theme(legend.position="top") +
  theme(axis.text.x = element_text(size = 10)) +
  theme(legend.box.spacing = unit(0, "pt"), legend.spacing.x = unit(0, "pt"), legend.spacing.y = unit(0, "pt")) +
  #theme(axis.text.x = element_text(angle = 45, vjust = 1.0, hjust=1)) +
  #ggh4x::facetted_pos_scales(x = scales) +
  labs(x="Output log probability", y="Accuracy")



ggsave(file.path("~", 'embers_decoding_4may2024.pdf'), width=10.5, height=4.3)


